import typing
from .codex.query.bits import FilterBit, OrderBit, SliceBit, T


class EQ(FilterBit[T]):
    pass


class NE(FilterBit[T]):
    pass


class LE(FilterBit[T]):
    pass


class GE(FilterBit[T]):
    pass


class LT(FilterBit[T]):
    pass


class GT(FilterBit[T]):
    pass


class IS(FilterBit[T]):
    pass


class LIKE(FilterBit[T]):
    def __init__(self, value: T, case_sensitive: bool = False):
        super().__init__(value)
        self._case_sensitive = case_sensitive

    def __eq__(self, other: typing.Self):
        return (
            self._data == other.value and
            self._case_sensitive == other.case_sensitive
        )

    @property
    def case_sensitive(self) -> bool:
        return self._case_sensitive


class SET(FilterBit[T]):
    def __init__(self, *value: T):
        super().__init__(set(value))


class RANGE(FilterBit[T]):
    def __init__(self, left: GE | GT | None, right: LE | LT | None):
        super().__init__((left, right))


class NOT(FilterBit[T]):
    def __init__(self, value: FilterBit[T]):
        super().__init__(value)
        self._value = value

    def __eq__(self, other):
        if other is None:
            return super().__eq__(other)
        else:
            return super().__eq__(other.value)


class Limit(SliceBit):
    pass


class Offset(SliceBit):
    pass


class ASC(OrderBit):
    pass


class DESC(OrderBit):
    pass
