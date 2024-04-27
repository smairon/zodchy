import typing
import abc

T = typing.TypeVar("T")


class ClauseBit(typing.Generic[T]):
    def __init__(self, *data: typing.Self):
        self._data = data

    @property
    def value(self):
        return self._data

    def __add__(self, other: type[typing.Self]):
        if type(self) is ClauseBit:
            self._data = list(self._data)
            self._data.append(other)
            return self

        else:
            return ClauseBit(*(self, other))


class SliceBit(ClauseBit):
    def __init__(self, value: int):
        super().__init__()
        self._data = value

    @property
    def value(self):
        return self._data


class Limit(SliceBit):
    pass


class Offset(SliceBit):
    pass


class FilterBit(abc.ABC, ClauseBit[T]):
    def __init__(self, value: T):
        super().__init__()
        self._data = value

    @property
    def value(self):
        return self._data

    def __eq__(self, other: T):
        return self._data == other


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


class NOT(FilterBit):
    def __init__(self, value: FilterBit):
        super().__init__(value)
        self._value = value

    def __eq__(self, other):
        if other is None:
            return super().__eq__(other)
        else:
            return super().__eq__(other.value)


class OrderBit(abc.ABC, ClauseBit):
    def __init__(self, priority: int = 0):
        super().__init__()
        self._data = priority

    @property
    def value(self):
        return self._data


class ASC(OrderBit):
    pass


class DESC(OrderBit):
    pass
