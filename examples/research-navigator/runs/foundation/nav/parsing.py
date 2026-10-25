"""Parse original bytes into deterministic, heading-aware native passages."""
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
from zipfile import ZipFile, BadZipFile
import xml.etree.ElementTree as ET
from .contracts import NavigatorError

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
SUPPORTED = {'.md', '.txt', '.docx'}
TARGET_CHARS = 3000


def _passage(source, digest, kind, start, end, headings, text):
    identity = json.dumps([source, digest, kind, start, end, text], ensure_ascii=False)
    return {'id': sha256(identity.encode('utf-8')).hexdigest(), 'source': source,
            'sha256': digest, 'locator': {'kind': kind, 'start': start, 'end': end},
            'headings': list(headings), 'text': text}


def _heading(stack, level, title):
    while stack and stack[-1][0] >= level:
        stack.pop()
    stack.append((level, title))
    return [title for _, title in stack]


def _text_passages(data, source, digest, markdown):
    # Native line boundaries survive; only the BOM and final line terminator are omitted.
    lines = data.decode('utf-8-sig').splitlines(keepends=True)
    stack, context, blocks = [], [], []
    start = None
    block_context = []
    fence = None
    for i, line in enumerate(lines):
        clean = line.rstrip('\r\n')
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', clean) if markdown else None
        heading = None
        if markdown and fence is None:
            heading = re.match(r'^ {0,3}(#{1,6})(?:[ \t]+(.*?)|[ \t]*)$', clean)
        if not markdown and clean.strip():
            blocks.append((i, i, []))
            continue
        if heading:
            if start is not None:
                blocks.append((start, i - 1, block_context))
            title = re.sub(r'[ \t]+#+[ \t]*$', '', heading.group(2) or '').strip()
            context = _heading(stack, len(heading.group(1)), title)
            blocks.append((i, i, list(context)))
            start = None
        elif not clean.strip() and fence is None:
            if start is not None:
                blocks.append((start, i - 1, block_context))
                start = None
        elif start is None:
            start, block_context = i, list(context)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
    if start is not None:
        blocks.append((start, len(lines) - 1, block_context))
    pending = None
    passages = []
    for start, end, headings in blocks:
        if pending and (pending[2] != headings or
                        len(''.join(lines[pending[0]:end + 1])) > TARGET_CHARS):
            a, b, h = pending
            passages.append(_passage(source, digest, 'lines', a + 1, b + 1, h,
                                     ''.join(lines[a:b + 1]).rstrip('\r\n')))
            pending = None
        pending = (pending[0] if pending else start, end, headings)
    if pending:
        a, b, h = pending
        passages.append(_passage(source, digest, 'lines', a + 1, b + 1, h,
                                 ''.join(lines[a:b + 1]).rstrip('\r\n')))
    return passages


def _paragraph_text(paragraph):
    values = []
    for node in paragraph.iter():
        if node.tag == W + 't':
            values.append(node.text or '')
        elif node.tag == W + 'tab':
            values.append('\t')
        elif node.tag in (W + 'br', W + 'cr'):
            values.append('\n')
        elif node.tag == W + 'noBreakHyphen':
            values.append('\u2011')
        elif node.tag == W + 'softHyphen':
            values.append('\u00ad')
    return ''.join(values)


def _docx_passages(data, source, digest):
    with ZipFile(BytesIO(data)) as archive:
        root = ET.fromstring(archive.read('word/document.xml'))
        body = root.find(W + 'body')
        if body is None:
            raise NavigatorError('DOCX has no Word document body')
        styles = {}
        if 'word/styles.xml' in archive.namelist():
            for style in ET.fromstring(archive.read('word/styles.xml')).findall(W + 'style'):
                styles[style.get(W + 'styleId')] = style
        def outline(properties, seen=None):
            if properties is None:
                return None
            explicit = properties.find(W + 'outlineLvl')
            if explicit is not None:
                value = int(explicit.get(W + 'val', '9'))
                return value + 1 if value < 9 else None
            ref = properties.find(W + 'pStyle')
            return style_level(ref.get(W + 'val'), seen or set()) if ref is not None else None
        def style_level(style_id, seen):
            if style_id in seen:
                return None
            seen.add(style_id)
            style = styles.get(style_id)
            if style is not None:
                value = outline(style.find(W + 'pPr'), seen)
                if value:
                    return value
                name = style.find(W + 'name')
                label = name.get(W + 'val', '') if name is not None else ''
                match = re.fullmatch(r'heading[ _-]*([1-9])', label, re.I)
                if match:
                    return int(match.group(1))
                parent = style.find(W + 'basedOn')
                if parent is not None:
                    return style_level(parent.get(W + 'val'), seen)
            match = re.fullmatch(r'heading([1-9])', style_id or '', re.I)
            return int(match.group(1)) if match else None
        paragraphs = list(body.iter(W + 'p'))
        texts = [_paragraph_text(p) for p in paragraphs]
        stack, context, passages = [], [], []
        start = end = None
        length = 0
        def emit():
            if start is not None:
                passages.append(_passage(source, digest, 'paragraphs', start + 1, end + 1,
                                         context, '\n'.join(texts[start:end + 1])))
        for i, paragraph in enumerate(paragraphs):
            text = texts[i]
            level = outline(paragraph.find(W + 'pPr'))
            if level:
                emit()
                start = end = None
                length = 0
                context = _heading(stack, level, text)
            if not text.strip():
                continue
            if start is not None and length + len(text) + (i - end) > TARGET_CHARS:
                emit()
                start = end = None
                length = 0
            if start is None:
                start = i
            end = i
            length = len('\n'.join(texts[start:end + 1]))
        emit()
        return passages


def parse_corpus(source_dir: Path) -> dict:
    source_dir = Path(source_dir).resolve()
    if not source_dir.is_dir():
        raise NavigatorError(f'Source directory does not exist: {source_dir}')
    try:
        paths = sorted((p for p in source_dir.rglob('*') if p.is_file()
                        and p.suffix.lower() in SUPPORTED),
                       key=lambda p: (p.relative_to(source_dir).as_posix().casefold(),
                                      p.relative_to(source_dir).as_posix()))
        if not paths:
            raise NavigatorError(f'No supported source files in {source_dir}')
        index = {'schema_version': 1, 'source_dir': str(source_dir), 'sources': [], 'passages': []}
        for path in paths:
            source = path.relative_to(source_dir).as_posix()
            try:
                data = path.read_bytes()
                digest = sha256(data).hexdigest()
                passages = (_docx_passages(data, source, digest) if path.suffix.lower() == '.docx'
                            else _text_passages(data, source, digest, path.suffix.lower() == '.md'))
            except (OSError, UnicodeError, BadZipFile, ET.ParseError, KeyError, ValueError) as exc:
                raise NavigatorError(f'Cannot parse {source}: {exc}') from exc
            index['sources'].append({'source': source, 'sha256': digest})
            index['passages'].extend(passages)
        return index
    except OSError as exc:
        raise NavigatorError(f'Cannot read source directory: {exc}') from exc
