"""Append-only adjudication of an evaluator CRLF/LF false failure.

Uses the frozen evaluator unchanged as a library, overriding only export text
reading to retain its actual byte-level newlines. Runs the entire original
freshness procedure on a byte-verified execution copy of a frozen delivery.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import time

import evaluate


class BytePreservingExports(evaluate.Evaluation):
    def export_one(self, anchor: dict, suffix: str, status="current") -> Path:
        report = self.runtime / "reports outside corpus" / f"{suffix}.md"
        report.parent.mkdir(exist_ok=True)
        self.command("export", "--index", str(self.index), "--query", anchor["query"], "--limit", "1000", "--output", str(report), json_output=False)
        evaluate.require(report.is_file(), "Export reported success without creating report")
        # The only correction to the frozen export oracle: do not translate CRLF.
        raw_bytes = report.read_bytes()
        text = raw_bytes.decode("utf-8-sig")
        evaluate.require(anchor["query"].casefold() in text.casefold(), "Export lacks query")
        evaluate.require(anchor["text"] in text, "Export lacks real complete anchor text")
        evaluate.require(evaluate.sha256(self.oracle.data[anchor["source"]]) in text, "Export lacks indexed source hash")
        evaluate.require((self.corpus / anchor["source"]).resolve() in self.linked_paths(report, text), "Export source link does not resolve to original source from report directory")
        hit = self.hits.get(anchor["query"])
        if hit:
            kind = "paragraph" if hit["locator"]["kind"] == "paragraphs" else "line"
            locators = re.findall(rf"(?i){kind}s?[^\n]{{0,100}}", text)
            evaluate.require(any(str(hit["locator"]["start"]) in location and str(hit["locator"]["end"]) in location for location in locators), "Export lacks native locator range")
            for heading in hit["headings"]:
                evaluate.require(heading in text, "Export lacks heading context")
            evaluate.require(hit["text"] in text, "Export omitted part of the selected complete passage")
        if status != "current":
            evaluate.require(re.search(rf"\b{status}\b", text, re.I) is not None, f"Export does not expose {status} evidence")
        # Record separately that status occurs in an explicit metadata line,
        # rather than granting credit for a word found only in research prose.
        explicit_status = bool(re.search(rf"(?im)^Source status:\s*\*\*{status}\*\*\s*$", text))
        evaluate.require(explicit_status, f"Expected explicit source-status metadata for {status}")
        self.observe(export=str(report), source=anchor["source"], expected_status=status,
                     linked_original=True, explicit_status_metadata=explicit_status,
                     report_sha256=evaluate.sha256(raw_bytes), crlf_pairs=text.count("\r\n"),
                     exact_full_passage_bytes_preserved=hit is not None and hit["text"].encode("utf-8") in raw_bytes)
        return report


def verify_snapshot(snapshot: Path, manifest: dict):
    checked = {}
    for relative, digest in manifest["files"].items():
        actual = evaluate.sha256((snapshot / relative).read_bytes())
        evaluate.require(actual == digest, f"Frozen snapshot changed: {relative}")
        checked[relative] = actual
    return checked


def prove_original_mismatch(original: dict):
    case = next(case for case in original["cases"] if case["name"] == "freshness")
    evaluate.require(case["status"] == "fail" and "Export omitted part of the selected complete passage" in case.get("reason", ""), "Original result is not the identified complete-passage failure")
    commands = [command for command in original["commands"] if command["id"] in case["command_ids"]]
    export = next(command for command in reversed(commands) if command["argv"][2] == "export")
    argv = export["argv"]
    report = Path(argv[argv.index("--output") + 1])
    query = argv[argv.index("--query") + 1]
    search = next(command for command in reversed(commands) if command["argv"][2] == "search" and command["argv"][command["argv"].index("--query") + 1] == query)
    hits = json.loads(search["stdout"])["matches"]
    raw_bytes = report.read_bytes()
    raw_text = raw_bytes.decode("utf-8-sig")
    translated = report.read_text(encoding="utf-8-sig")
    candidates = [hit for hit in hits if "\r\n" in hit["text"] and hit["text"] in raw_text and hit["text"] not in translated]
    evaluate.require(bool(candidates), "The original failure is not established as CRLF translation only")
    hit = candidates[0]
    evaluate.require(hit["text"].replace("\r\n", "\n") in translated, "Newline normalization does not recover the complete passage")
    return {
        "original_case": case["name"], "original_status": case["status"], "original_reason": case["reason"],
        "search_command_id": search["id"], "export_command_id": export["id"],
        "report_path": str(report), "report_sha256": evaluate.sha256(raw_bytes),
        "source": hit["source"], "locator": hit["locator"], "passage_id": hit["id"],
        "indexed_source_sha256": hit["sha256"], "indexed_status": hit["status"],
        "passage_crlf_pairs": hit["text"].count("\r\n"),
        "raw_report_crlf_pairs": raw_text.count("\r\n"),
        "translated_report_crlf_pairs": translated.count("\r\n"),
        "exact_passage_bytes_present": hit["text"].encode("utf-8") in raw_bytes,
        "exact_text_present_after_universal_newline_translation": False,
        "complete_text_present_after_matching_newline_normalization": True,
        "explicit_status_metadata": bool(re.search(rf"(?im)^Source status:\s*\*\*{hit['status']}\*\*\s*$", raw_text)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--snapshot-manifest", type=Path, required=True)
    parser.add_argument("--original-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started_utc, started = evaluate.utc(), time.monotonic()
    snapshot, corpus, output = args.snapshot.resolve(), args.corpus.resolve(), args.output.resolve()
    evaluate.require(not output.exists(), "Refusing to overwrite adjudication evidence")
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(args.snapshot_manifest.read_text(encoding="utf-8"))
    original_bytes = args.original_result.read_bytes()
    original = json.loads(original_bytes)
    evaluator_bytes = (evaluate.HERE / "evaluate.py").read_bytes()
    evaluate.require(evaluate.sha256(evaluator_bytes) == original["evaluator_sha256"], "Frozen evaluator differs from original run")
    snapshot_before = verify_snapshot(snapshot, manifest)
    diagnosis = prove_original_mismatch(original)
    expected = json.loads((evaluate.HERE / "SOURCE_EXPECTATIONS.json").read_text(encoding="utf-8"))
    source_oracle = evaluate.SourceOracle(corpus, expected)
    stage = Path(tempfile.mkdtemp(prefix="adjudication-execution-", dir=output.parent))
    execution_copy = stage / "unchanged product"
    shutil.copytree(snapshot, execution_copy)
    verify_snapshot(execution_copy, manifest)
    (execution_copy / "corpus").mkdir()
    for name in source_oracle.data:
        shutil.copy2(corpus / name, execution_copy / "corpus" / name)
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    evaluator = BytePreservingExports(execution_copy, output, 120, expected)
    evaluator.run_case("clean_indexing", evaluator.clean_indexing)
    evaluator.run_case("freshness", evaluator.freshness)
    evaluator.original.assert_unchanged()
    evaluator.oracle.assert_unchanged()
    source_oracle.assert_unchanged()
    evaluate.require(verify_snapshot(snapshot, manifest) == snapshot_before, "Frozen snapshot changed during review")
    verify_snapshot(execution_copy, manifest)
    evaluate.require(args.original_result.read_bytes() == original_bytes, "Original result changed")
    evaluate.require((evaluate.HERE / "evaluate.py").read_bytes() == evaluator_bytes, "Frozen evaluator changed")
    evaluate.require(evaluate.sha256(Path(diagnosis["report_path"]).read_bytes()) == diagnosis["report_sha256"], "Original report evidence changed")
    evaluator.report.update({
        "record_type": "supplemental_adjudication_not_replacement",
        "review_started_utc": started_utc,
        "ended_utc": evaluate.utc(),
        "elapsed_seconds": round(time.monotonic() - started, 4),
        "snapshot": str(snapshot),
        "snapshot_manifest_sha256": evaluate.sha256(args.snapshot_manifest.read_bytes()),
        "snapshot_files_checked_before_and_after": len(snapshot_before),
        "original_result": str(args.original_result.resolve()),
        "original_result_sha256": evaluate.sha256(original_bytes),
        "adjudicator_sha256": evaluate.sha256(Path(__file__).read_bytes()),
        "diagnosis": diagnosis,
        "adjudication": "Evaluator newline-normalization false failure; complete original report text was preserved. Entire frozen freshness sequence rerun on unchanged product with byte-preserving report reads.",
        "product_changes": 0,
        "builder_repair_opportunities_consumed": 0,
        "original_artifacts_preserved": True,
        "source_integrity_at_end": "unchanged",
        "summary": {status: sum(case["status"] == status for case in evaluator.report["cases"]) for status in ("pass", "fail", "blocked")},
    })
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(evaluator.report, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({"output": str(output), "summary": evaluator.report["summary"], "elapsed_seconds": evaluator.report["elapsed_seconds"], "snapshot_unchanged": True}))
    return 1 if evaluator.report["summary"]["fail"] or evaluator.report["summary"]["blocked"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
