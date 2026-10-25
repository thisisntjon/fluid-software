"""Decode actual sources, retaining native locations and heading context."""
from __future__ import annotations

import hashlib
import io
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

SUPPORTED = {".md", ".txt", ".docx"}
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def heading_stack(stack: list, level: int, title: str) -> list:
    return [(depth, text) for depth, text in stack if depth < level] + [(level, title)]


def markdown_context(lines: list[str]) -> list[list[str]]:
    contexts, stack = [], []
    fence = None
    for i, line in enumerate(lines):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
        elif fence is None:
            atx = re.match(r"^ {0,3}(#{1,6})(?:[ \t]+|$)(.*)$", line)
            if atx:
                title = re.sub(r"[ \t]+#+[ \t]*$", "", atx.group(2)).strip()
                stack = heading_stack(stack, len(atx.group(1)), title)
            elif line.strip() and i + 1 < len(lines):
                underline = re.fullmatch(r" {0,3}(=+|-+)[ \t]*", lines[i + 1])
                if underline:
                    stack = heading_stack(stack, 1 if underline.group(1)[0] == "=" else 2, line.strip())
        contexts.append([title for _, title in stack])
    return contexts


def docx_units(data: bytes) -> tuple[list[str], list[list[str]]]:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        body = document.find(W + "body")
        if body is None:
            raise ValueError("Word document has no w:body")
        styles = {}
        if "word/styles.xml" in archive.namelist():
            for style in ET.fromstring(archive.read("word/styles.xml")).findall(W + "style"):
                styles[style.get(W + "styleId")] = style

    def outline_level(properties, seen=None):
        if properties is None:
            return None
        outline = properties.find(W + "outlineLvl")
        if outline is not None:
            value = int(outline.get(W + "val", "9"))
            return value + 1 if 0 <= value < 9 else None
        style_ref = properties.find(W + "pStyle")
        return style_level(style_ref.get(W + "val"), seen or set()) if style_ref is not None else None

    def style_level(style_id, seen):
        if style_id in seen:
            return None
        seen.add(style_id)
        style = styles.get(style_id)
        if style is None:
            match = re.fullmatch(r"heading\s*([1-9])", style_id or "", re.I)
            return int(match.group(1)) if match else None
        level = outline_level(style.find(W + "pPr"), seen)
        if level is not None:
            return level
        name = style.find(W + "name")
        match = re.fullmatch(r"heading\s*([1-9])", name.get(W + "val", "") if name is not None else style_id, re.I)
        if match:
            return int(match.group(1))
        based = style.find(W + "basedOn")
        return style_level(based.get(W + "val"), seen) if based is not None else None

    def paragraph_text(paragraph):
        pieces = []

        def visit(element):
            for child in element:
                if child.tag == W + "p":
                    # A nested text-box paragraph has its own native ordinal.
                    continue
                if child.tag == W + "t":
                    pieces.append(child.text or "")
                elif child.tag == W + "tab":
                    pieces.append("\t")
                elif child.tag in {W + "br", W + "cr"}:
                    pieces.append("\n")
                elif child.tag == W + "noBreakHyphen":
                    pieces.append("\u2011")
                elif child.tag == W + "softHyphen":
                    pieces.append("\u00ad")
                else:
                    visit(child)
        visit(paragraph)
        return "".join(pieces)

    texts, contexts, stack = [], [], []
    for paragraph in body.iter(W + "p"):
        text = paragraph_text(paragraph)
        level = outline_level(paragraph.find(W + "pPr"))
        if level is not None and text.strip():
            stack = heading_stack(stack, level, text.strip())
        texts.append(text)
        contexts.append([title for _, title in stack])
    return texts, contexts


def passage_ranges(text: str, units: list[dict], target: int = 2400) -> list[list[int]]:
    """Partition at headings and nearby paragraph/line/sentence boundaries.

    Search can join adjacent ranges, so partitioning cannot hide a phrase.
    """
    if not text:
        return []
    sections = [0]
    for previous, unit in zip(units, units[1:]):
        if previous["headings"] != unit["headings"] and unit["start"] > sections[-1]:
            sections.append(unit["start"])
    sections.append(len(text))
    ranges = []
    for section_start, section_end in zip(sections, sections[1:]):
        start = section_start
        while section_end - start > target * 1.5:
            lo, hi = start + target // 2, min(section_end, start + target)
            end = None
            for pattern in (r"\n[ \t]*\n", r"\n", r"[.!?][\s]+", r"\s+"):
                candidates = list(re.finditer(pattern, text[lo:hi]))
                if candidates:
                    end = lo + candidates[-1].end()
                    break
            end = end or hi
            ranges.append([start, end])
            start = end
        if start < section_end:
            ranges.append([start, section_end])
    return ranges


def parse_source(path: Path, source: str) -> dict:
    data = path.read_bytes()
    digest = sha256(data)
    if path.suffix.lower() == ".docx":
        texts, contexts = docx_units(data)
        text = "\n".join(texts)
        kind = "paragraphs"
    else:
        text = data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
        texts = text.split("\n")
        # A terminal newline terminates the last line; it adds no source line.
        if texts and texts[-1] == "" and text.endswith("\n"):
            texts.pop()
        contexts = markdown_context(texts) if path.suffix.lower() == ".md" else [[] for _ in texts]
        kind = "lines"
    units, offset = [], 0
    for ordinal, (unit_text, headings) in enumerate(zip(texts, contexts), 1):
        units.append({"start": offset, "end": offset + len(unit_text), "ordinal": ordinal, "headings": headings})
        offset += len(unit_text) + 1
    return {
        "source": source,
        "sha256": digest,
        "key": sha256((source + "\0" + digest).encode("utf-8")),
        "kind": kind,
        "text": text,
        "units": units,
        "ranges": passage_ranges(text, units),
    }
