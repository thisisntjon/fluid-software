"""Literal, case-insensitive retrieval over complete indexed passages."""
from .contracts import NavigatorError
from .storage import source_statuses


def normalize(text: str) -> str:
    return ' '.join(text.casefold().split())


def search(index: dict, query: str, limit: int) -> list[dict]:
    phrase = normalize(query)
    if not phrase:
        raise NavigatorError('Query must contain non-whitespace text')
    if type(limit) is not int or limit <= 0:
        raise NavigatorError('Limit must be a positive integer')
    statuses = source_statuses(index)
    matches = []
    for passage in index['passages']:
        if phrase in normalize(passage['text']):
            matches.append({**passage, 'status': statuses[passage['source']]})
            if len(matches) == limit:
                break
    return matches


def show(index: dict, passage_id: str) -> dict:
    for passage in index['passages']:
        if passage['id'] == passage_id:
            statuses = source_statuses(index)
            return {**passage, 'status': statuses[passage['source']]}
    raise NavigatorError(f'Unknown passage id: {passage_id}')
