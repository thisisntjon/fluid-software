"""Offline Research Navigator commands and source-linked Markdown reports."""
import argparse
import json
from pathlib import Path
import re
import sys
from .contracts import NavigatorError
from .parsing import parse_corpus
from .storage import load_index, write_index, source_statuses, atomic_write_text, protect_sources
from .query import search, show


def _parser():
    parser = argparse.ArgumentParser(description='Search local research documents and export source-linked evidence.')
    commands = parser.add_subparsers(dest='command', required=True)
    for name, help_text in (
        ('index', 'Build or atomically replace an index from Markdown, text, and DOCX files.'),
        ('search', 'Find a case-insensitive literal phrase, normalizing whitespace.'),
        ('show', 'Read one complete indexed passage by its stable ID.'),
        ('export', 'Export complete matching passages and provenance as Markdown.'),
        ('status', 'Hash current files and report current, changed, or missing sources.')):
        command = commands.add_parser(name, help=help_text, description=help_text)
        command.add_argument('--index', type=Path, required=True, help='Path to the JSON index file.')
        command.add_argument('--json', action='store_true', help='Print exactly one JSON value to stdout.')
        if name == 'index':
            command.add_argument('--source-dir', type=Path, required=True, help='Directory to scan recursively.')
        elif name in ('search', 'export'):
            command.add_argument('--query', required=True, help='Literal phrase (quote phrases containing spaces).')
            command.add_argument('--limit', type=int, default=10, help='Maximum matching passages; positive integer (default: 10).')
            if name == 'export':
                command.add_argument('--output', type=Path, required=True, help='Markdown report path; missing parent folders are created.')
        elif name == 'show':
            command.add_argument('--id', required=True, help='Passage ID returned by search.')
    return parser


def _sources(index):
    statuses = source_statuses(index)
    return {'sources': [{**source, 'status': statuses[source['source']]} for source in index['sources']],
            'source_dir': index['source_dir'], 'passage_count': len(index['passages'])}


def _escape(text):
    return re.sub(r'([\\`*{}\[\]()<>#!|_])', r'\\\1', text).replace('\n', ' ')


def _fenced(text):
    longest = max((len(run) for run in re.findall(r'`+', text)), default=0)
    fence = '`' * max(3, longest + 1)
    return fence + 'text\n' + text + '\n' + fence


def _report(index, query, matches):
    parts = ['# Research Navigator evidence', '', 'Query:', '', _fenced(query), '',
             f'Matching passages selected: {len(matches)}.', '',
             'Text below is the indexed source text. Status reflects source bytes checked at export time; '
             'the source link opens the current file. Research claims are reproduced without endorsement.', '']
    for n, passage in enumerate(matches, 1):
        source_path = (Path(index['source_dir']) / passage['source']).resolve()
        locator = passage['locator']
        headings = ' > '.join(passage['headings']) or '(unheaded)'
        parts += [f'## Passage {n}', '',
                  f'Source: [{_escape(passage["source"])}](<{source_path.as_uri()}>)', '',
                  f'Location: {locator["kind"]} {locator["start"]}-{locator["end"]} (inclusive, 1-based).', '',
                  f'Heading context: {_escape(headings)}', '',
                  f'Source status: **{passage["status"]}**', '',
                  f'Indexed SHA-256: `{passage["sha256"]}`', '',
                  f'Passage ID: `{passage["id"]}`', '', _fenced(passage['text']), '']
    if not matches:
        parts += ['No matching passages.', '']
    return '\n'.join(parts)


def _print_human(result, command):
    if command in ('index', 'status'):
        for source in result['sources']:
            print(f'{source["status"]:7}  {source["source"]}  {source["sha256"]}')
        print(f'{result["passage_count"]} indexed passages.')
    elif command == 'export':
        print(f'Exported {result["match_count"]} passages to {result["output"]}')
    else:
        passages = result['matches'] if command == 'search' else [result]
        if not passages:
            print('No matching passages.')
        for passage in passages:
            loc = passage['locator']
            print(f'[{passage["status"]}] {passage["source"]}: {loc["kind"]} {loc["start"]}-{loc["end"]}')
            print('ID: ' + passage['id'])
            print('Headings: ' + (' > '.join(passage['headings']) or '(unheaded)'))
            print(passage['text'])
            print()


def main(argv=None) -> int:
    # UTF-8 also preserves non-ASCII source text when redirected on Windows.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.command == 'index':
            index = parse_corpus(args.source_dir)
            write_index(index, args.index)
            result = _sources(index)
        else:
            index = load_index(args.index)
            if args.command == 'status':
                result = _sources(index)
            elif args.command == 'show':
                result = show(index, args.id)
            else:
                matches = search(index, args.query, args.limit)
                if args.command == 'search':
                    result = {'matches': matches}
                else:
                    if args.output.resolve() == args.index.resolve():
                        raise NavigatorError('Report output would overwrite the index')
                    protect_sources(index, args.output)
                    atomic_write_text(args.output, _report(index, args.query, matches))
                    result = {'output': str(args.output.resolve()), 'match_count': len(matches),
                              'sources': [{key: passage[key] for key in ('source', 'sha256', 'status')}
                                          for passage in matches]}
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            _print_human(result, args.command)
        return 0
    except (NavigatorError, OSError, UnicodeError) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
