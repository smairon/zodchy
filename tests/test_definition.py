import pytest
from zodchy import operators


@pytest.mark.parametrize(
    "v, type_",
    [
        (1, int),
        ('string', str)
    ]
)
def test_comparative(v: int | str, type_: type):
    op = operators.EQ[type_](v)
    assert op.value == v
    op = operators.NE[type_](v)
    assert op.value == v
    op = operators.LE[type_](v)
    assert op.value == v
    op = operators.LT[type_](v)
    assert op.value == v
    op = operators.GE[type_](v)
    assert op.value == v
    op = operators.GT[type_](v)
    assert op.value == v
    op = operators.IS[type_](v)
    assert op.value == v
    op = operators.IS[type_](None)
    assert op.value is None


def test_likes():
    op = operators.LIKE[str]('string')
    assert op.case_sensitive is False
    op = operators.LIKE[str]('string', case_sensitive=True)
    assert op.case_sensitive is True


def test_set():
    op = operators.SET[int](1, 2, 3)
    assert op.value == {1, 2, 3}


@pytest.mark.parametrize(
    'left,right', [
        (operators.GE[int](1), operators.LE[int](2)),
        (operators.GE[int](1), operators.LT[int](2)),
        (operators.GT[int](1), operators.LE[int](2)),
        (operators.GT[int](1), operators.LT[int](2)),
    ]
)
def test_range(left, right):
    op = operators.RANGE[int](left, right)
    assert op.value == (left, right)


@pytest.mark.parametrize(
    'value,type_', [
        (operators.EQ[int](1), int),
        (operators.GE[int](1), int),
        (operators.GT[int](1), int),
        (operators.LE[int](1), int),
        (operators.LT[int](1), int),
        (operators.IS[int](1), int),
        (operators.LIKE[str]('ddd'), str),
        (operators.SET[int](1, 2, 3), int),
        (operators.RANGE[int](operators.GE[int](1), operators.LE[int](2)), int),
    ]
)
def test_not(value, type_):
    op = operators.NOT[type_](value)
    assert op.value == value
