import datetime
import typing
import uuid

import pytest

from zodchy import codex

references = {
    "datetime": (
        "2024-04-04T11:04:02",
        datetime.datetime(2024, 4, 4, 11, 4, 2)
    ),
    "date": (
        "2024-04-04",
        datetime.date(2024, 4, 4)
    ),
    "uuid": (
        "744f7c52-5405-4087-ad0a-2dbb1d512a68",
        uuid.UUID("744f7c52-5405-4087-ad0a-2dbb1d512a68")
    ),
    "int": (
        "12",
        12
    ),
    "float": (
        "12.23",
        12.23
    ),
    "str": (
        "хорошо сидим",
        "хорошо сидим"
    ),
    "bool_positive": (
        "true",
        True
    ),
    "bool_negative": (
        "false",
        False
    )
}


@pytest.mark.parametrize(
    "data,value",
    [
        (
            f"item_id={references['uuid'][0]}",
            codex.query.EQ(references['uuid'][1])
        ),
        (
            f"amount={references['int'][0]}",
            codex.query.EQ(references['int'][1])
        ),
        (
            f"price={references['float'][0]}",
            codex.query.EQ(references['float'][1])
        ),
        (
            f"created_at={references['datetime'][0]}",
            codex.query.EQ(references['datetime'][1])
        ),
        (
            f"birthday={references['date'][0]}",
            codex.query.EQ(references['date'][1])
        ),
        (
            f"name={references['str'][0]}",
            codex.query.EQ(references['str'][1])
        ),
        (
            f"is_active={references['bool_positive'][0]}",
            codex.query.EQ(references['bool_positive'][1])
        ),
        (
            f"is_active={references['bool_negative'][0]}",
            codex.query.EQ(references['bool_negative'][1])
        ),
        (
            "item_id=null",
            codex.query.IS(None)
        ),
        (
            "created_at=!null",
            codex.query.NOT(codex.query.IS(None))
        ),
        (
            f"annotation=~{references['str'][0]}",
            codex.query.LIKE(references['str'][1], case_sensitive=True)
        ),
        (
            f"annotation=!~{references['str'][0]}",
            codex.query.NOT(codex.query.LIKE(references['str'][1], case_sensitive=True))
        ),
        (
            f"annotation=~~{references['str'][0]}",
            codex.query.LIKE(references['str'][1], case_sensitive=False)
        ),
        (
            f"annotation=!~~{references['str'][0]}",
            codex.query.NOT(codex.query.LIKE(references['str'][1], case_sensitive=False))
        )
    ]
)
def test_comparisons(
    parser: codex.query.NotationParser,
    data: str,
    value: typing.Any
):
    result = next(parser(data), None)
    assert result.value == value
