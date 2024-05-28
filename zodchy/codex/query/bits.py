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


class FilterBit(abc.ABC, ClauseBit[T]):
    def __init__(self, value: T):
        super().__init__()
        self._data = value

    @property
    def value(self):
        return self._data

    def __eq__(self, other: T):
        return self._data == other


class OrderBit(abc.ABC, ClauseBit):
    def __init__(self, priority: int = 0):
        super().__init__()
        self._data = priority

    @property
    def value(self):
        return self._data
