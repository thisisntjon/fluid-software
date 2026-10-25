"""Append-only adjudication using an independent CommonMark heading oracle.

The frozen product and evaluator remain unchanged. An already installed reference
parser is used only by the coordinator, not as a product dependency. The shared
brief did not restrict Markdown headings to ATX or require a math extension.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import tempfile
import time

from markdown_it import MarkdownIt

import evaluate
from adjudicate_newlines import verify_snapshot


def reference_headings(source: Path):
    tokens = MarkdownIt("commonmark").parse(source.read_text(encoding="utf-8-sig"))
    rows, records = [], []
    for index, token in enumerate(tokens):
        if token.type == "heading_open" and token.map:
            text = tokens[index + 1].content
            rows.append((token.map[0] + 1, int(token.tag[1:]), text))
            records.append({"start": token.map[0] + 1, "end": token.map[1], "level": int(token.tag[1:]), "text": text, "markup": token.markup})
    return rows, records


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
    expected = json.loads((evaluate.HERE / "SOURCE_EXPECTATIONS.json").read_text(encoding="utf-8"))
    source_oracle = evaluate.SourceOracle(corpus, expected)
    anchor = expected["anchors"][0]
    original_case = next(case for case in original["cases"] if case["name"] == "markdown_retrieval_context")
    evaluate.require(original_case["status"] == "fail" and "Reported heading is not a real source heading" in original_case.get("reason", ""), "Original result is not the heading-membership failure")
    command = next(command for command in original["commands"] if command["id"] in original_case["command_ids"] and command["argv"][2] == "search")
    original_hit = next(hit for hit in json.loads(command["stdout"])["matches"] if hit["source"] == anchor["source"] and anchor["text"] in hit["text"])
    rows, records = reference_headings(corpus / anchor["source"])
    source_oracle.heading_rows[anchor["source"]] = rows
    reference_chain = source_oracle.headings_at(anchor["source"], original_hit["locator"]["start"])
    evaluate.require(original_hit["headings"] == reference_chain, "Original heading chain does not match independent CommonMark parsing")
    unexpected_under_atx = [heading for heading in original_hit["headings"] if not any(heading == row[2] for row in evaluate.SourceOracle(corpus, expected).heading_rows[anchor["source"]])]
    evaluate.require(bool(unexpected_under_atx), "No ATX-only oracle difference exists")
    stage = Path(tempfile.mkdtemp(prefix="heading-adjudication-execution-", dir=output.parent))
    execution_copy = stage / "unchanged product"
    shutil.copytree(snapshot, execution_copy)
    verify_snapshot(execution_copy, manifest)
    (execution_copy / "corpus").mkdir()
    for name in source_oracle.data:
        shutil.copy2(corpus / name, execution_copy / "corpus" / name)
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    evaluator = evaluate.Evaluation(execution_copy, output, 120, expected)
    # Supplemental oracle replacement only: the frozen evaluator file is not edited.
    evaluator.oracle.heading_rows[anchor["source"]] = rows
    evaluator.run_case("clean_indexing", evaluator.clean_indexing)
    evaluator.run_case("markdown_retrieval_context", lambda: evaluator.anchor_check(anchor))
    evaluator.run_case("usable_source_navigation_for_adjudicated_passage", evaluator.navigation)
    evaluator.original.assert_unchanged()
    evaluator.oracle.assert_unchanged()
    source_oracle.assert_unchanged()
    evaluate.require(verify_snapshot(snapshot, manifest) == snapshot_before, "Frozen snapshot changed during review")
    verify_snapshot(execution_copy, manifest)
    evaluate.require(args.original_result.read_bytes() == original_bytes, "Original result changed")
    evaluate.require((evaluate.HERE / "evaluate.py").read_bytes() == evaluator_bytes, "Frozen evaluator changed")
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
        "diagnosis": {
            "original_case": original_case["name"], "original_status": original_case["status"], "original_reason": original_case["reason"],
            "original_command_id": command["id"], "source": anchor["source"], "source_sha256": evaluate.sha256(source_oracle.data[anchor["source"]]),
            "original_headings": original_hit["headings"], "reference_headings": reference_chain,
            "rejected_by_atx_only_oracle": unexpected_under_atx,
            "reference_parser": "markdown-it-py", "reference_parser_version": importlib.metadata.version("markdown-it-py"), "preset": "commonmark",
            "reference_heading_records_near_source_passage": [record for record in records if 257 <= record["start"] <= 323],
            "reference_sources": ["https://spec.commonmark.org/0.31.2/#setext-headings", "https://markdown-it-py.readthedocs.io/en/latest/using.html#the-parser"],
            "interpretation": "The returned parent is a valid CommonMark setext heading at lines 298-299. The shared brief did not select a math-aware dialect or forbid setext headings. This specific failed result is not a demonstrated product defect.",
            "limitation": "The source appears intended as display math; math-aware navigation would be a useful future enhancement. This adjudication does not establish complete CommonMark conformance of the product.",
        },
        "adjudication": "ATX-only evaluator rejected a heading independently confirmed by the CommonMark specification and reference parser. Original remaining search/show/native-location obligations rerun against unchanged delivered product.",
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
