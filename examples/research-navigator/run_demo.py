"""Run both delivered Research Navigators (Foundation-assisted and Control) on a generated sample corpus."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def create_sample_docx(path: Path) -> None:
    """Create a minimal valid .docx with body paragraphs and a 2x2 table using stdlib zipfile."""
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""
    document = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p>
      <w:pPr><w:pStyle w:val="Heading1"/></w:pPr>
      <w:r><w:t>Hierarchical Scaffolding Overview</w:t></w:r>
    </w:p>
    <w:p>
      <w:r><w:t>Materialized module boundaries keep each builder focused on a coherent responsibility while preserving the whole-project frame.</w:t></w:r>
    </w:p>
    <w:tbl>
      <w:tr>
        <w:tc><w:p><w:r><w:t>Dependency Edge</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:t>Operational Role</w:t></w:r></w:p></w:tc>
      </w:tr>
      <w:tr>
        <w:tc><w:p><w:r><w:t>depends_on</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:t>Tracks semantic provider snapshots and marks downstream deliveries stale when upstream contracts change.</w:t></w:r></w:p></w:tc>
      </w:tr>
    </w:tbl>
  </w:body>
</w:document>"""
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("word/document.xml", document)


def populate_sample_corpus(corpus_dir: Path) -> Path:
    corpus_dir.mkdir(parents=True, exist_ok=True)
    md1 = corpus_dir / "scaffolding-notes.md"
    md1.write_text(
        "# Project Framing Principles\n\n"
        "Stop decomposition at the largest coherent buildable module.\n\n"
        "## Three-Tier Context\n\n"
        "Provide the whole-project map, ancestor responsibilities, and direct semantic neighbors.\n",
        encoding="utf-8",
        newline="\n",
    )
    txt1 = corpus_dir / "reuse-checklist.txt"
    txt1.write_bytes(
        b"Reuse Evaluation Notes\r\n\r\n"
        b"Inspect existing reference implementations before writing new module stubs.\r\n"
        b"Preserve exact byte-level provenance and SHA-256 digests across exports.\r\n"
    )
    docx1 = corpus_dir / "Hierarchical Scaffolding Sample.docx"
    create_sample_docx(docx1)
    return corpus_dir


def run_navigator(label: str, script: Path, corpus_dir: Path, work_dir: Path) -> None:
    index_path = work_dir / f"{label}-index.json"
    report_path = work_dir / f"{label}-report.md"

    idx_cmd = [sys.executable, str(script), "index", "--source-dir", str(corpus_dir), "--index", str(index_path), "--json"]
    idx_res = json.loads(subprocess.check_output(idx_cmd, text=True, encoding="utf-8"))
    assert len(idx_res["sources"]) == 3, f"{label}: expected 3 indexed sources"

    search_cmd = [sys.executable, str(script), "search", "--index", str(index_path), "--query", "semantic provider snapshots", "--limit", "3", "--json"]
    search_res = json.loads(subprocess.check_output(search_cmd, text=True, encoding="utf-8"))
    assert search_res["matches"], f"{label}: expected search matches"
    top_pid = search_res["matches"][0]["id"]

    show_cmd = [sys.executable, str(script), "show", "--index", str(index_path), "--id", top_pid, "--json"]
    show_res = json.loads(subprocess.check_output(show_cmd, text=True, encoding="utf-8"))
    assert show_res["id"] == top_pid

    exp_cmd = [sys.executable, str(script), "export", "--index", str(index_path), "--query", "scaffolding", "--limit", "3", "--output", str(report_path)]
    subprocess.check_output(exp_cmd, text=True, encoding="utf-8")
    assert report_path.is_file() and report_path.stat().st_size > 0

    stat_cmd = [sys.executable, str(script), "status", "--index", str(index_path), "--json"]
    stat_res = json.loads(subprocess.check_output(stat_cmd, text=True, encoding="utf-8"))
    statuses = [s["status"] for s in stat_res["sources"]]
    assert all(st == "current" for st in statuses), f"{label}: expected all sources current, got {statuses}"

    print(
        f"[OK] {label:10s} | indexed={len(idx_res['sources'])} docs "
        f"| top_hit={top_pid} | statuses={statuses}"
    )


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="fluid-nav-demo-") as tmp:
        tmp_path = Path(tmp)
        corpus_dir = populate_sample_corpus(tmp_path / "corpus")
        run_navigator("foundation", HERE / "runs/foundation/navigator.py", corpus_dir, tmp_path)
        run_navigator("control", HERE / "runs/control/navigator.py", corpus_dir, tmp_path)


if __name__ == "__main__":
    main()
