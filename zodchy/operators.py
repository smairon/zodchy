import typing
from .codex.query.bits import FilterBit, OrderBit, SliceBit

T = typing.TypeVar("T")


class EQ(FilterBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__(value)


class NE(FilterBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__(value)


class LE(FilterBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__(value)


class GE(FilterBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__(value)


class LT(FilterBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__(value)


class GT(FilterBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__(value)


class IS(FilterBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__(value)


class LIKE(FilterBit, typing.Generic[T]):
    def __init__(self, value: T, case_sensitive: bool = False):
        super().__init__(value)
        self._case_sensitive = case_sensitive

    def __eq__(self, other: object):
        if not isinstance(other, type(self)):
            raise NotImplemented
        return (
            self._data == other.value and
            self._case_sensitive == other.case_sensitive
        )

    @property
    def case_sensitive(self) -> bool:
        return self._case_sensitive


class SET(FilterBit, typing.Generic[T]):
    def __init__(self, *value: T):
        super().__init__(set(value))


class RANGE(FilterBit, typing.Generic[T]):
    def __init__(self, left: GE[T] | GT[T] | None, right: LE[T] | LT[T] | None):
        super().__init__((left, right))


class NOT(FilterBit, typing.Generic[T]):
    def __init__(
        self,
        value: EQ[T] | LE[T] | GE[T] | LT[T] | GT[T] | IS[T] | LIKE[T] | SET[T] | RANGE[T]
    ):
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
