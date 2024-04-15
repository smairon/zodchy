import datetime
import typing
import uuid

import pytest

from zodchy import codex


@pytest.mark.parametrize(
    "data,values",
    [
        (
            "item_id={744f7c52-5405-4087-ad0a-2dbb1d512a68,4cb72e04-9793-4a8a-85d1-97cf8a1c1d57}",
            {uuid.UUID("744f7c52-5405-4087-ad0a-2dbb1d512a68"), uuid.UUID("4cb72e04-9793-4a8a-85d1-97cf8a1c1d57")}
        ),
        (
            "amount={1,2,3,4}",
            {1, 2, 3, 4}
        ),
        (
            "price={1.01,2.2,3.1415926,4.45}",
            {1.01, 2.2, 3.1415926, 4.45}
        ),
        (
            "created_at={2024-04-04T11:04:02,2024-04-05T10:04:02}",
            {
                datetime.datetime(2024, 4, 4, 11, 4, 2),
                datetime.datetime(2024, 4, 5, 10, 4, 2),
            }
        ),
        (
            "birthday={2024-04-04,2024-04-05}",
            {
                datetime.date(2024, 4, 4),
                datetime.date(2024, 4, 5),
            }
        ),
        (
            "annotation={хорошо,плохо,так себе}",
            {"хорошо", "плохо", "так себе"}
        )
    ]
)
def test_set(
    parser: codex.query.NotationParser,
    data: str,
    values: set[typing.Any]
):
    param = next(parser(data), None)
    assert isinstance(param.value, codex.query.SET)
    assert param.value.value == values
