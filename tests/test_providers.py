import json

from app.providers import _strip_json_code_fence


def test_strip_json_code_fence_keeps_plain_json_parseable() -> None:
    content = '{"fit_score": 80}'

    assert json.loads(_strip_json_code_fence(content)) == {"fit_score": 80}


def test_strip_json_code_fence_removes_json_fence() -> None:
    content = '```json\n{"fit_score": 80}\n```'

    assert _strip_json_code_fence(content) == '{"fit_score": 80}'


def test_strip_json_code_fence_removes_plain_fence() -> None:
    content = '```\n{"fit_score": 80}\n```'

    assert _strip_json_code_fence(content) == '{"fit_score": 80}'
