"""Coordinator-only connected evaluation; uses the frozen CLI brief and real sources.

No builder implementation is imported or inspected. Each invocation records a new,
non-overwriting result and runs the actual entry point in independent subprocesses.
Use --oracle-only to check source expectations without running an implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from urllib.parse import unquote, urlsplit
from urllib.request import url2pathname
import xml.etree.ElementTree as ET
import zipfile


HERE = Path(__file__).resolve().parent
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


def utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized(text: str) -> str:
    return " ".join(text.split())


def passage_identity(hit: dict) -> dict:
    """Compare contract fields; optional telemetry is not a determinism oracle."""
    return {key: hit.get(key) for key in ("id", "source", "sha256", "status", "locator", "headings", "text")}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


class Blocked(Exception):
    """An explicit prerequisite or manual judgment remains unavailable."""


class SourceOracle:
    """Independent source bytes/XML; deliberately knows no index format."""

    def __init__(self, corpus: Path, expected: dict):
        self.corpus = corpus
        self.expected = expected
        self.data: dict[str, bytes] = {}
        self.units: dict[str, list[str]] = {}
        self.heading_rows: dict[str, list[tuple[int, int, str]]] = {}
        self.docx_paragraphs: dict[str, list] = {}
        self.docx_roots: dict[str, ET.Element] = {}
        for source in expected["sources"]:
            name = source["source"]
            data = (corpus / name).read_bytes()
            require(len(data) == source["bytes"], f"Source byte size differs: {name}")
            require(sha256(data) == source["sha256"], f"Source hash differs: {name}")
            self.data[name] = data
            self.heading_rows[name] = []
            if name.endswith(".docx"):
                with zipfile.ZipFile(corpus / name) as archive:
                    root = ET.fromstring(archive.read("word/document.xml"))
                paragraphs = root.findall(".//w:body//w:p", NS)
                self.docx_roots[name] = root
                self.docx_paragraphs[name] = paragraphs
                units = ["".join(t.text or "" for t in p.findall(".//w:t", NS)) for p in paragraphs]
                require(len(units) == source["body_paragraph_count"], f"Paragraph count: {name}")
                require(sum(bool(x.strip()) for x in units) == source["nonempty_body_paragraph_count"], f"Nonempty count: {name}")
                for number, paragraph in enumerate(paragraphs, 1):
                    style = paragraph.find("w:pPr/w:pStyle", NS)
                    value = style.get("{" + NS["w"] + "}val", "") if style is not None else ""
                    match = re.fullmatch(r"Heading([1-9])", value, re.I)
                    if match:
                        self.heading_rows[name].append((number, int(match[1]), units[number - 1]))
            else:
                units = data.decode("utf-8-sig").splitlines()
                require(len(units) == source["line_count"], f"Line count: {name}")
                if name.endswith(".md"):
                    in_fence = False
                    for number, line in enumerate(units, 1):
                        if line.lstrip().startswith(("```", "~~~")):
                            in_fence = not in_fence
                        match = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
                        if match and not in_fence:
                            self.heading_rows[name].append((number, len(match[1]), match[2]))
            self.units[name] = units
        for anchor in expected["anchors"]:
            name = anchor["source"]
            text = "\n".join(self.units[name][anchor["start"] - 1:anchor["end"]])
            require(text == anchor["text"], f"Frozen anchor differs: {name}:{anchor['start']}")
            require(sha256(text.encode("utf-8")) == anchor["text_sha256"], "Frozen anchor hash differs")
            if anchor.get("inside_table"):
                target = self.docx_paragraphs[name][anchor["start"] - 1]
                require(any(target is p for table in self.docx_roots[name].findall(".//w:tbl", NS) for p in table.findall(".//w:p", NS)), "DOCX table anchor is not in a table")

    def headings_at(self, source: str, number: int) -> list[str]:
        stack: list[tuple[int, str]] = []
        for location, level, text in self.heading_rows[source]:
            if location > number:
                break
            stack = [(old_level, old_text) for old_level, old_text in stack if old_level < level]
            stack.append((level, text))
        return [text for _, text in stack]

    def assert_unchanged(self) -> None:
        for name, data in self.data.items():
            require((self.corpus / name).read_bytes() == data, f"Original arm corpus changed: {name}")

    def no_match_query(self) -> str:
        candidate = self.expected["sources"][0]["sha256"]
        require(all(candidate.casefold() not in normalized("\n".join(units)).casefold() for units in self.units.values()), "Chosen source-hash query unexpectedly appears in source text")
        return candidate


class Evaluation:
    def __init__(self, arm: Path, output: Path, timeout: int, expected: dict):
        self.arm = arm
        self.output = output
        self.timeout = timeout
        self.expected = expected
        self.entry = arm / "navigator.py"
        self.original = SourceOracle(arm / "corpus", expected)
        self.runtime = Path(tempfile.mkdtemp(prefix=f"evaluation-{arm.name}-", dir=output.parent))
        self.corpus = self.runtime / "actual corpus"
        self.corpus.mkdir()
        for source in expected["sources"]:
            shutil.copy2(arm / "corpus" / source["source"], self.corpus / source["source"])
        self.oracle = SourceOracle(self.corpus, expected)
        self.index = self.runtime / "new index parent" / "research.index"
        self.hits: dict[str, dict] = {}
        self.clean = False
        self.case: dict | None = None
        self.report = {
            "schema_version": 1,
            "started_utc": utc(),
            "arm": str(arm),
            "entry_point": str(self.entry),
            "runtime": str(self.runtime),
            "python": sys.version,
            "per_command_timeout_seconds": timeout,
            "brief_sha256": sha256((HERE / "TASK_BRIEF.md").read_bytes()),
            "expectations_sha256": sha256((HERE / "SOURCE_EXPECTATIONS.json").read_bytes()),
            "evaluator_sha256": sha256(Path(__file__).read_bytes()),
            "cases": [],
            "commands": [],
            "fault_injection_disclosure": "Only private byte-identical corpus copies are changed: one same-length case edit with original mtime restored, one temporary source move, and one DOCX truncation. Originals are checked unchanged.",
            "limitations": [
                "One descriptive example; no statistical or causal generalization.",
                "Native token counts, tool-call costs, and dollar costs are not measured.",
                "The evaluator does not sandbox filesystem or network access.",
                "No implementation source is imported or inspected; generic parsing and delivery honesty require manual review.",
                "CLI failure or blocked checks are retained; result files are never overwritten.",
            ],
        }

    def observe(self, **values) -> None:
        assert self.case is not None
        self.case["observations"].append(values)

    def command(self, *args: str, expected_success=True, json_output=True) -> dict | list | str:
        argv = [sys.executable, str(self.entry), *map(str, args)]
        record = {"id": len(self.report["commands"]) + 1, "argv": argv, "cwd": str(self.arm), "started_utc": utc()}
        started = time.monotonic()
        try:
            env = dict(os.environ)
            env["PYTHONUTF8"] = "1"
            result = subprocess.run(argv, cwd=self.arm, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=self.timeout, env=env)
            record.update(returncode=result.returncode, stdout=result.stdout, stderr=result.stderr)
        except subprocess.TimeoutExpired as exc:
            def decoded(value):
                return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else (value or "")
            record.update(returncode=None, timed_out=True, stdout=decoded(exc.stdout), stderr=decoded(exc.stderr))
        except OSError as exc:
            record.update(returncode=None, launch_error=str(exc), stdout="", stderr="")
        record.update(ended_utc=utc(), elapsed_seconds=round(time.monotonic() - started, 4))
        self.report["commands"].append(record)
        with (self.runtime / "commands.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        assert self.case is not None
        self.case["command_ids"].append(record["id"])
        require(record["returncode"] is not None, f"Command {record['id']} did not complete: {record}")
        if not expected_success:
            require(record["returncode"] != 0, f"Command {record['id']} unexpectedly succeeded")
            require(bool(record["stderr"].strip()), f"Command {record['id']} failed without a stderr diagnostic")
            return record["stdout"]
        require(record["returncode"] == 0, f"Command {record['id']} exited {record['returncode']}: {record['stderr'][:1200]}")
        if json_output:
            try:
                return json.loads(record["stdout"])
            except ValueError as exc:
                raise AssertionError(f"Command {record['id']} stdout is not exactly one JSON value: {exc}") from exc
        return record["stdout"]

    def run_case(self, name: str, function) -> None:
        self.case = {"name": name, "started_utc": utc(), "command_ids": [], "observations": []}
        started = time.monotonic()
        try:
            function()
            self.case["status"] = "pass"
        except Blocked as exc:
            self.case.update(status="blocked", reason=str(exc))
        except Exception as exc:
            self.case.update(status="fail", reason=f"{type(exc).__name__}: {exc}")
        self.case.update(ended_utc=utc(), elapsed_seconds=round(time.monotonic() - started, 4))
        self.report["cases"].append(self.case)
        with (self.runtime / "cases.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(self.case, ensure_ascii=False) + "\n")
        print(f"{self.case['name']}: {self.case['status']}", flush=True)
        self.case = None

    def need_index(self) -> None:
        if not self.clean:
            raise Blocked("Clean indexing did not succeed; this check requires its index.")

    def source_rows(self, payload, statuses=None, current_hashes=None) -> None:
        require(isinstance(payload, dict) and isinstance(payload.get("sources"), list), "Expected JSON sources list")
        rows = payload["sources"]
        names = [row.get("source") if isinstance(row, dict) else None for row in rows]
        expected_names = [source["source"] for source in self.expected["sources"]]
        require(len(names) == len(expected_names) and set(names) == set(expected_names), f"Indexed source names differ: {names}")
        for row in rows:
            name = row["source"]
            expected_status = (statuses or {}).get(name, "current")
            require(row.get("status") == expected_status, f"Source status {name}: expected {expected_status}, got {row.get('status')}")
            require(isinstance(row.get("sha256"), str) and HEX64.fullmatch(row["sha256"]) is not None, f"Invalid hash for {name}")
            if expected_status == "current":
                correct = (current_hashes or {}).get(name, sha256(self.oracle.data[name]))
                require(row["sha256"] == correct, f"Source hash differs for {name}")

    def index_command(self):
        return self.command("index", "--source-dir", str(self.corpus), "--index", str(self.index), "--json")

    def clean_indexing(self):
        payload = self.index_command()
        self.source_rows(payload)
        self.source_rows(self.command("status", "--index", str(self.index), "--json"))
        self.clean = True
        self.observe(source_count=len(payload["sources"]), corpus=str(self.corpus), index=str(self.index), corpus_hashes_verified=True)

    def search(self, query: str, limit=1000) -> list[dict]:
        payload = self.command("search", "--index", str(self.index), "--query", query, "--limit", str(limit), "--json")
        require(isinstance(payload, dict) and isinstance(payload.get("matches"), list), "Expected JSON matches list")
        require(len(payload["matches"]) <= limit, "Search exceeded requested limit")
        return payload["matches"]

    def passage(self, hit: dict, status="current", expected_hash=None) -> None:
        require(isinstance(hit, dict), "Passage is not an object")
        require(isinstance(hit.get("id"), str) and bool(hit["id"].strip()), "Missing stable passage ID")
        source = hit.get("source")
        require(source in self.oracle.units, f"Unknown passage source: {source}")
        require(hit.get("sha256") == (expected_hash or sha256(self.oracle.data[source])), f"Passage indexed source hash: {source}")
        require(hit.get("status") == status, f"Passage source status: expected {status}, got {hit.get('status')}")
        locator = hit.get("locator")
        require(isinstance(locator, dict), "Missing locator")
        require(locator.get("kind") == ("paragraphs" if source.endswith(".docx") else "lines"), "Wrong native locator kind")
        start, end = locator.get("start"), locator.get("end")
        require(type(start) is int and type(end) is int and 1 <= start <= end <= len(self.oracle.units[source]), f"Invalid native range: {locator}")
        require(isinstance(hit.get("text"), str) and bool(hit["text"].strip()), "Missing full passage text")
        raw = "\n".join(self.oracle.units[source][start - 1:end])
        require(normalized(hit["text"]) in normalized(raw), f"Passage text is not supported by stated native source range: {source}:{start}-{end}")
        headings = hit.get("headings")
        require(isinstance(headings, list) and all(isinstance(item, str) for item in headings), "Missing heading list")
        known_headings = [text for _, _, text in self.oracle.heading_rows[source]]
        require(all(normalized(heading) in [normalized(value) for value in known_headings] for heading in headings), "Reported heading is not a real source heading")

    def anchor_check(self, anchor: dict) -> None:
        self.need_index()
        matches = self.search(anchor["query"])
        candidates = [hit for hit in matches if isinstance(hit, dict) and hit.get("source") == anchor["source"] and anchor["text"] in hit.get("text", "")]
        require(bool(candidates), f"Missing real-source anchor {anchor['source']}:{anchor['start']}")
        hit = candidates[0]
        self.passage(hit)
        require(hit["locator"]["start"] <= anchor["start"] <= anchor["end"] <= hit["locator"]["end"], "Locator does not cover exact independent anchor")
        if anchor.get("heading"):
            require(anchor["heading"] in hit["headings"], f"Missing containing heading {anchor['heading']}")
        shown = self.command("show", "--index", str(self.index), "--id", hit["id"], "--json")
        self.passage(shown)
        for key in ("id", "source", "sha256", "locator", "headings", "text"):
            require(shown[key] == hit[key], f"show changed {key} from search")
        self.hits[anchor["query"]] = hit
        self.observe(source=hit["source"], locator=hit["locator"], passage_id=hit["id"], independent_anchor_text_sha256=anchor["text_sha256"], search_matches=len(matches))

    def navigation(self):
        self.need_index()
        if not self.hits:
            raise Blocked("No source-backed anchor passages available for navigation checks")
        for hit in self.hits.values():
            self.passage(hit)
            ancestors = self.oracle.headings_at(hit["source"], hit["locator"]["start"])
            if ancestors:
                require(any(heading in hit["headings"] for heading in ancestors), f"No containing heading for {hit['source']}:{hit['locator']['start']}")
        self.observe(independently_re_read_passages=len(self.hits))

    def persistence(self):
        self.need_index()
        anchor = self.expected["anchors"][0]
        before = self.search(anchor["query"])
        repeated = self.search(anchor["query"].upper())
        require(list(map(passage_identity, before)) == list(map(passage_identity, repeated)), "Case-insensitive query changed deterministic results")
        limited = self.search(anchor["query"], limit=1)
        require(list(map(passage_identity, limited)) == list(map(passage_identity, before[:1])), "Limit changed ordering or did not cap deterministic results")
        self.source_rows(self.index_command())
        after = self.search(anchor["query"])
        require(list(map(passage_identity, before)) == list(map(passage_identity, after)), "Re-indexing identical bytes changed passages/IDs")
        if before:
            hit = before[0]
            shown = self.command("show", "--index", str(self.index), "--id", hit["id"], "--json")
            require(shown["text"] == hit["text"] and shown["locator"] == hit["locator"], "New-process show changed source passage")
        self.original.assert_unchanged()
        self.oracle.assert_unchanged()
        self.observe(identical_reindex_preserved_results=True, separate_processes=True, source_hashes_unchanged=True)

    def no_match_and_errors(self):
        self.need_index()
        query = self.oracle.no_match_query()
        require(self.search(query) == [], "Proven absent query produced a result")
        self.command("search", "--index", str(self.index), "--query", "", "--limit", "10", "--json", expected_success=False)
        self.command("search", "--index", str(self.index), "--query", self.expected["anchors"][0]["query"], "--limit", "0", "--json", expected_success=False)
        self.command("search", "--index", str(self.runtime / "does-not-exist.index"), "--query", query, "--limit", "10", "--json", expected_success=False)
        known_ids = {hit["id"] for hit in self.hits.values()}
        unknown = "invalid-passage-" + query
        require(unknown not in known_ids, "Invalid-ID oracle collision")
        self.command("show", "--index", str(self.index), "--id", unknown, "--json", expected_success=False)
        self.observe(no_match_query=query, independently_absent_from_all_source_text=True, invalid_input_commands=4)

    @staticmethod
    def linked_paths(report: Path, text: str) -> list[Path]:
        targets = []
        for match in re.finditer(r"\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\n)]+))\s*\)", text):
            target = (match[1] or match[2]).strip()
            if re.match(r"^[A-Za-z]:[/\\]", target):
                targets.append(Path(unquote(target.split("#", 1)[0])).resolve())
                continue
            parsed = urlsplit(target)
            if parsed.scheme == "file":
                location = url2pathname(parsed.path)
                if parsed.netloc and parsed.netloc.lower() != "localhost":
                    location = "//" + parsed.netloc + location
                targets.append(Path(location).resolve())
            elif not parsed.scheme:
                targets.append((report.parent / unquote(parsed.path)).resolve())
        return targets

    def export_one(self, anchor: dict, suffix: str, status="current") -> Path:
        report = self.runtime / "reports outside corpus" / f"{suffix}.md"
        report.parent.mkdir(exist_ok=True)
        self.command("export", "--index", str(self.index), "--query", anchor["query"], "--limit", "1000", "--output", str(report), json_output=False)
        require(report.is_file(), "Export reported success without creating report")
        text = report.read_text(encoding="utf-8-sig")
        require(anchor["query"].casefold() in text.casefold(), "Export lacks query")
        require(anchor["text"] in text, "Export lacks real complete anchor text")
        require(sha256(self.oracle.data[anchor["source"]]) in text, "Export lacks indexed source hash")
        require((self.corpus / anchor["source"]).resolve() in self.linked_paths(report, text), "Export source link does not resolve to original source from report directory")
        hit = self.hits.get(anchor["query"])
        if hit:
            kind = "paragraph" if hit["locator"]["kind"] == "paragraphs" else "line"
            locators = re.findall(rf"(?i){kind}s?[^\n]{{0,100}}", text)
            require(any(str(hit["locator"]["start"]) in location and str(hit["locator"]["end"]) in location for location in locators), "Export lacks native locator range")
            for heading in hit["headings"]:
                require(heading in text, "Export lacks heading context")
            require(hit["text"] in text, "Export omitted part of the selected complete passage")
        if status != "current":
            require(re.search(rf"\b{status}\b", text, re.I) is not None, f"Export does not expose {status} evidence")
        self.observe(export=str(report), source=anchor["source"], expected_status=status, linked_original=True)
        return report

    def exports(self):
        self.need_index()
        self.export_one(self.expected["anchors"][-1], "word-table-evidence")
        self.export_one(self.expected["anchors"][0], "markdown-evidence")

    def freshness(self):
        self.need_index()
        changed_anchor = self.expected["anchors"][2]
        missing_anchor = self.expected["anchors"][1]
        changed = self.corpus / changed_anchor["source"]
        missing = self.corpus / missing_anchor["source"]
        held = self.runtime / "temporarily held actual source.md"
        changed_stat = changed.stat()
        original_bytes = changed.read_bytes()
        original_word = b"Measure usable connected capabilities"
        altered_word = b"measure usable connected capabilities"
        require(original_bytes.count(original_word) == 1, "Same-length edit oracle is not unique")
        altered_bytes = original_bytes.replace(original_word, altered_word, 1)
        require(len(original_bytes) == len(altered_bytes) and altered_bytes != original_bytes, "Fault injection must change bytes without changing size")
        changed_hits = self.search(changed_anchor["query"])
        changed_hit = next((hit for hit in changed_hits if hit.get("source") == changed_anchor["source"] and changed_anchor["text"] in hit.get("text", "")), None)
        missing_hits = self.search(missing_anchor["query"])
        missing_hit = next((hit for hit in missing_hits if hit.get("source") == missing_anchor["source"] and missing_anchor["text"] in hit.get("text", "")), None)
        require(changed_hit is not None and missing_hit is not None, "Freshness requires both actual indexed source passages")
        self.hits[changed_anchor["query"]] = changed_hit
        self.hits[missing_anchor["query"]] = missing_hit
        try:
            changed.write_bytes(altered_bytes)
            os.utime(changed, ns=(changed_stat.st_atime_ns, changed_stat.st_mtime_ns))
            missing.rename(held)
            require(changed.stat().st_size == changed_stat.st_size and changed.stat().st_mtime_ns == changed_stat.st_mtime_ns, "Could not preserve size and mtime for hash-based freshness check")
            self.source_rows(self.command("status", "--index", str(self.index), "--json"), statuses={changed.name: "changed", missing.name: "missing"})
            for anchor, old_hit, state in [(changed_anchor, changed_hit, "changed"), (missing_anchor, missing_hit, "missing")]:
                rows = self.search(anchor["query"])
                hit = next((row for row in rows if row.get("id") == old_hit["id"]), None)
                require(hit is not None, f"Lost indexed passage for {state} source")
                self.passage(hit, status=state)
                require(hit["text"] == old_hit["text"], f"Indexed text mutated during {state} source lookup")
                shown = self.command("show", "--index", str(self.index), "--id", old_hit["id"], "--json")
                self.passage(shown, status=state)
                self.export_one(anchor, f"{state}-evidence", status=state)
            self.observe(fault="same-byte-length case edit with unchanged mtime", source=changed.name, indexed_sha256=sha256(original_bytes), current_sha256=sha256(altered_bytes), size=changed.stat().st_size, original_mtime_ns=changed_stat.st_mtime_ns)
        finally:
            changed.write_bytes(original_bytes)
            os.utime(changed, ns=(changed_stat.st_atime_ns, changed_stat.st_mtime_ns))
            if held.exists():
                held.rename(missing)
        self.source_rows(self.command("status", "--index", str(self.index), "--json"))
        try:
            changed.write_bytes(altered_bytes)
            self.source_rows(self.index_command(), current_hashes={changed.name: sha256(altered_bytes)})
            self.source_rows(self.command("status", "--index", str(self.index), "--json"), current_hashes={changed.name: sha256(altered_bytes)})
            rows = self.search(changed_anchor["query"])
            altered_text = changed_anchor["text"].replace("Measure", "measure", 1)
            fresh = [hit for hit in rows if hit.get("source") == changed.name and altered_text in hit.get("text", "")]
            require(bool(fresh) and fresh[0].get("sha256") == sha256(altered_bytes) and fresh[0].get("status") == "current", "Re-index did not refresh changed real source text/hash")
            self.observe(reindex_refreshed_actual_edited_source=True)
        finally:
            changed.write_bytes(original_bytes)
            os.utime(changed, ns=(changed_stat.st_atime_ns, changed_stat.st_mtime_ns))
            # Restore baseline through the public interface for the remaining case.
            self.source_rows(self.index_command())

    def failed_rebuild(self):
        self.need_index()
        path = self.corpus / self.expected["anchors"][-1]["source"]
        original_bytes = path.read_bytes()
        original_stat = path.stat()
        anchor = self.expected["anchors"][0]
        before = self.search(anchor["query"])
        require(bool(before), "Failed-rebuild check needs an existing retrievable passage")
        try:
            path.write_bytes(original_bytes[:100])
            self.command("index", "--source-dir", str(self.corpus), "--index", str(self.index), "--json", expected_success=False)
            error = self.report["commands"][-1]["stderr"]
            require(path.name in error, "Parse failure did not identify the corrupt source")
            after = self.search(anchor["query"])
            require(list(map(passage_identity, before)) == list(map(passage_identity, after)), "Failed rebuild destroyed or changed previous usable index")
            self.observe(fault="DOCX truncated from its existing bytes", source=path.name, original_bytes=len(original_bytes), truncated_bytes=100, previous_index_still_retrievable=True)
        finally:
            path.write_bytes(original_bytes)
            os.utime(path, ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns))

    def delivery(self):
        for command in (None, "index", "search", "show", "export", "status"):
            args = ([command] if command else []) + ["--help"]
            help_text = self.command(*args, json_output=False)
            require(bool(help_text.strip()), f"Empty help for {command or 'entry point'}")
        readmes = [str(path.relative_to(self.arm)) for path in self.arm.iterdir() if path.is_file() and path.name.lower().startswith("readme")]
        self.observe(readme_candidates=readmes, help_commands_succeeded=6)
        require(bool(readmes), "No README delivered at project root")
        raise Blocked("Manual delivery review still required: run README commands, identify build log and reconcile claims against real commands, inspect for hardcoded answers, confirm declared limitations and maintainable responsibilities. Automated CLI evidence cannot establish these judgments.")

    def run(self):
        self.run_case("clean_indexing", self.clean_indexing)
        names = ["markdown_retrieval_context", "second_markdown_source", "dense_text_input", "word_heading", "word_table_content"]
        for name, anchor in zip(names, self.expected["anchors"]):
            self.run_case(name, lambda anchor=anchor: self.anchor_check(anchor))
        for name, function in [
            ("usable_source_navigation", self.navigation),
            ("stable_persistence", self.persistence),
            ("no_match_and_input_errors", self.no_match_and_errors),
            ("export", self.exports),
            ("freshness", self.freshness),
            ("failed_rebuild_preserves_usable_work", self.failed_rebuild),
            ("delivery", self.delivery),
        ]:
            self.run_case(name, function)
        try:
            self.original.assert_unchanged()
            self.oracle.assert_unchanged()
            self.report["source_integrity_at_end"] = "unchanged"
        except Exception as exc:
            self.report["source_integrity_at_end"] = f"FAILED: {exc}"
        self.report["ended_utc"] = utc()
        self.report["summary"] = {status: sum(case["status"] == status for case in self.report["cases"]) for status in ("pass", "fail", "blocked")}
        # Exclusive creation preserves first-pass results even if callers reuse a path.
        with self.output.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(self.report, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        print(json.dumps({"output": str(self.output), "runtime": str(self.runtime), "summary": self.report["summary"]}))
        return 1 if self.report["summary"]["fail"] or self.report["source_integrity_at_end"] != "unchanged" else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arm", type=Path, help="Arm project directory; corpus is ARM/corpus")
    parser.add_argument("--output", type=Path, help="New JSON evidence file; existing files are never replaced")
    parser.add_argument("--timeout", type=int, default=120, help="Per CLI process timeout in seconds (default: 120)")
    parser.add_argument("--oracle-only", type=Path, metavar="CORPUS", help="Only validate frozen expectations against actual sources; no implementation runs or writes")
    args = parser.parse_args()
    expected = json.loads((HERE / "SOURCE_EXPECTATIONS.json").read_text(encoding="utf-8"))
    if args.oracle_only:
        oracle = SourceOracle(args.oracle_only.resolve(), expected)
        absent = oracle.no_match_query()
        print(json.dumps({"status": "pass", "sources": len(expected["sources"]), "anchors": len(expected["anchors"]), "no_match_query_verified": absent, "implementation_invoked": False}))
        return 0
    if args.arm is None or args.output is None:
        parser.error("--arm and --output are required unless --oracle-only is used")
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    arm, output = args.arm.resolve(), args.output.resolve()
    if output.exists():
        parser.error(f"Refusing to overwrite preserved evaluation result: {output}")
    if not (arm / "navigator.py").is_file():
        parser.error(f"Entry point missing: {arm / 'navigator.py'}")
    if arm == output.parent or arm in output.parents:
        parser.error("--output must be in coordinator space outside the arm")
    output.parent.mkdir(parents=True, exist_ok=True)
    evaluator = Evaluation(arm, output, args.timeout, expected)
    return evaluator.run()


if __name__ == "__main__":
    raise SystemExit(main())
