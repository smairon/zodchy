import datetime
import uuid

import pytest

from zodchy.notations import math


@pytest.fixture()
def parser():
    return math.Parser(
        types_map=dict(
            item_id=uuid.UUID,
            amount=int,
            created_at=datetime.datetime,
            birthday=datetime.date,
            price=float,
            annotation=str,
            name=str,
            is_active=bool
        )
    )
