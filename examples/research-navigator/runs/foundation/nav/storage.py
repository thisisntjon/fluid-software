"""Validated JSON snapshots, atomic replacement, and byte-based freshness."""
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile
from .contracts import NavigatorError


def atomic_write_text(path: Path, text: str) -> None:
    path = Path(path).resolve()
    temporary = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='',
                                         dir=path.parent, prefix='.' + path.name + '.',
                                         suffix='.tmp', delete=False) as output:
            temporary = Path(output.name)
            output.write(text)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    except (OSError, UnicodeError) as exc:
        raise NavigatorError(f'Cannot write {path}: {exc}') from exc
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def protect_sources(index: dict, output: Path) -> None:
    output = Path(output).resolve()
    for source in index['sources']:
        if output == (Path(index['source_dir']) / source['source']).resolve():
            raise NavigatorError(f'Output would overwrite indexed source: {source["source"]}')


def _validate(index):
    def require(condition, message):
        if not condition:
            raise NavigatorError('Invalid index: ' + message)
    require(isinstance(index, dict), 'root must be an object')
    require(index.get('schema_version') == 1, 'unsupported schema version')
    require(isinstance(index.get('source_dir'), str) and Path(index['source_dir']).is_absolute(),
            'source_dir must be absolute')
    require(isinstance(index.get('sources'), list), 'sources must be a list')
    require(isinstance(index.get('passages'), list), 'passages must be a list')
    sources = {}
    for item in index['sources']:
        require(isinstance(item, dict), 'source entry must be an object')
        name, digest = item.get('source'), item.get('sha256')
        require(isinstance(name, str) and bool(name), 'source filename missing')
        require(not Path(name).is_absolute() and not PurePosixPath(name).is_absolute()
                and '..' not in PurePosixPath(name.replace('\\', '/')).parts
                and ':' not in name, 'source filename must be relative')
        require(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest) is not None,
                'invalid source hash')
        require(name not in sources, 'duplicate source filename')
        sources[name] = digest
    ids = set()
    for passage in index['passages']:
        require(isinstance(passage, dict), 'passage entry must be an object')
        pid = passage.get('id')
        require(isinstance(pid, str) and bool(pid) and pid not in ids, 'missing or duplicate passage id')
        ids.add(pid)
        source = passage.get('source')
        require(isinstance(source, str) and source in sources, 'passage source is unknown')
        require(passage.get('sha256') == sources[source], 'passage hash differs from source')
        require(isinstance(passage.get('text'), str), 'passage text missing')
        headings = passage.get('headings')
        require(isinstance(headings, list) and all(isinstance(h, str) for h in headings),
                'headings must be a list of strings')
        locator = passage.get('locator')
        require(isinstance(locator, dict), 'locator missing')
        require(locator.get('kind') in ('lines', 'paragraphs'), 'unknown locator kind')
        require(type(locator.get('start')) is int and type(locator.get('end')) is int
                and 1 <= locator['start'] <= locator['end'], 'invalid native location range')
    return index


def write_index(index: dict, path: Path) -> None:
    _validate(index)
    protect_sources(index, path)
    atomic_write_text(path, json.dumps(index, ensure_ascii=False, indent=2) + '\n')


def load_index(path: Path) -> dict:
    try:
        with Path(path).open('r', encoding='utf-8-sig') as source:
            return _validate(json.load(source))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise NavigatorError(f'Cannot load index {path}: {exc}') from exc


def source_statuses(index: dict) -> dict[str, str]:
    statuses = {}
    for source in index['sources']:
        name = source['source']
        path = Path(index['source_dir']) / name
        try:
            with path.open('rb') as file:
                digest = sha256()
                for chunk in iter(lambda: file.read(1024 * 1024), b''):
                    digest.update(chunk)
        except (FileNotFoundError, NotADirectoryError, IsADirectoryError):
            statuses[name] = 'missing'
            continue
        except OSError as exc:
            raise NavigatorError(f'Cannot check source {name}: {exc}') from exc
        statuses[name] = 'current' if digest.hexdigest() == source['sha256'] else 'changed'
    return statuses
