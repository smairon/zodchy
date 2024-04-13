import collections.abc
import dataclasses
import re
import datetime
import typing
import types

import dateutil.parser
import functools

from .. import codex

FieldName = str
FieldType = type


@dataclasses.dataclass
class ParsingSchema:
    order_by: str = 'order_by'
    limit: str = 'limit'
    offset: str = 'offset'
    fieldset: str = 'fieldset'


default_casting_map = types.MappingProxyType({
    datetime.datetime: dateutil.parser.parse
})

interval_types = (
    datetime.datetime,
    datetime.date,
    int,
    float
)


class Parser:
    def __init__(
        self,
        types_map: collections.abc.Mapping[FieldName, FieldType],
        casting_map: collections.abc.Mapping[
            FieldType,
            collections.abc.Callable[[str], typing.Any]
        ] = default_casting_map,
        parsing_schema: ParsingSchema = ParsingSchema()
    ):
        self._types_map = types_map
        self._casting_map = casting_map
        self._parsing_schema = parsing_schema

    def __call__(
        self,
        query: str | collections.abc.Mapping[str, str]
    ) -> collections.abc.Generator[codex.query.Param, None, None]:
        if isinstance(query, str):
            if '=' not in query:
                raise ValueError('You have to specify name for parameter value')
            query = (pairs.split('=') for pairs in query.split('&'))
        elif isinstance(query, collections.abc.Mapping):
            query = query.items()
        else:
            raise ValueError('Query mast be string or mapping')
        yield from self._parse(query)

    def _parse(self, query: collections.abc.Iterable[tuple[str, str]]):
        for pair in query:
            k, v = pair
            if v is None:
                continue
            if k == self._parsing_schema.order_by:
                yield from self._parse_order_param(v)
            elif k == self._parsing_schema.limit:
                yield codex.query.Param(
                    name=self._parsing_schema.limit,
                    value=codex.query.Limit(int(v))
                )
            elif k == self._parsing_schema.offset:
                yield codex.query.Param(
                    name=self._parsing_schema.offset,
                    value=codex.query.Offset(int(v))
                )
            else:
                yield self._parse_filter_param(k, v.strip())

    @staticmethod
    def _parse_order_param(
        names: FieldName
    ) -> collections.abc.Generator[codex.query.Param, None, None]:
        priority = 0
        for name in names.split(','):
            direction = codex.query.ASC
            if name.startswith('-'):
                direction = codex.query.DESC
                name = name[1:]
            yield codex.query.Param(
                name=name,
                value=direction(priority)
            )
            priority += 1

    def _parse_filter_param(self, name: FieldName, value: str):
        if name not in self._types_map:
            raise Exception(f'Type of parameter {name} must be defined in types map')

        for pattern, handler in self._pattern_handler_map.items():
            if mo := pattern.search(value):
                return handler(name, mo.group(1))

    def _interval(
        self,
        field_name: str,
        field_value: str,
        operations: tuple[
            type[codex.query.GT | codex.query.GE],
            type[codex.query.LT | codex.query.LE]
        ]
    ) -> codex.query.Param:
        if self._types_map[field_name] not in interval_types:
            raise TypeError(
                f'Interval cannot be calculated for type {self._types_map[field_name]} for field {field_name}')

        _data = field_value.split(',')
        if len(_data) != 2:
            raise ValueError(f'Range must contain strictly two members for field {field_name}')

        left = None
        right = None
        if _data[0]:
            left = operations[0](self._cast(_data[0], self._types_map[field_name]))
        if _data[1]:
            right = operations[1](self._cast(_data[1], self._types_map[field_name]))
        value = codex.query.RANGE(left, right)

        return codex.query.Param(name=field_name, value=value)

    def _multitude(
        self,
        field_name: str,
        field_value: str,
        inversion: bool = False
    ):
        field_value = codex.query.SET(
            *(
                self._cast(v, self._types_map[field_name])
                for v in field_value.split(',')
                if v
            )
        )

        if inversion:
            field_value = codex.query.NOT(field_value)

        return codex.query.Param(
            name=field_name,
            value=field_value
        )

    def _literal(
        self,
        field_name: str,
        field_value: str,
        operation: type[codex.query.FilterBit],
        inversion: bool = False
    ):
        field_value = operation(self._cast(field_value, self._types_map[field_name]))

        if inversion:
            field_value = codex.query.NOT(field_value)

        return codex.query.Param(
            name=field_name,
            value=field_value,
        )

    def _cast(self, value: str, type_: type):
        if cast := self._casting_map.get(type_):
            return cast(value)
        return type_(value)

    @functools.cached_property
    def _pattern_handler_map(self):
        return {
            re.compile('^(null)$'): lambda x, y: codex.query.IS(None),
            re.compile('^(!null)$'): lambda x, y: codex.query.NOT(codex.query.IS(None)),
            re.compile(r'^\(([\d\-,.]+)\)$'): functools.partial(
                self._interval,
                operations=(codex.query.GT, codex.query.LT)
            ),
            re.compile(r'^\[([\d\-,.]+)\)$'): functools.partial(
                self._interval,
                operations=(codex.query.GE, codex.query.LT)
            ),
            re.compile(r'^\(([\d\-,.]+)]$'): functools.partial(
                self._interval,
                operations=(codex.query.GT, codex.query.LE)
            ),
            re.compile(r'^\[([\d\-,.]+)]$'): functools.partial(
                self._interval,
                operations=(codex.query.GE, codex.query.LE)
            ),
            re.compile(r'^!{(.*)}$'): functools.partial(
                self._multitude,
                inversion=True
            ),
            re.compile(r'^{(.*)}$'): self._multitude,
            re.compile(r'^~{2}(.*)$'): functools.partial(
                self._literal,
                operation=codex.query.LIKE
            ),
            re.compile(r'^![~]{2}(.*)$'): functools.partial(
                self._literal,
                operation=codex.query.LIKE,
                inversion=True
            ),
            re.compile(r'^~(.*)$'): functools.partial(
                self._literal,
                operation=functools.partial(
                    codex.query.LIKE,
                    case_sensitive=True
                )
            ),
            re.compile(r'^!~(.*)$'): functools.partial(
                self._literal,
                operation=functools.partial(
                    codex.query.LIKE,
                    case_sensitive=True
                ),
                inversion=True
            ),
            re.compile(r'^!(.*)$'): functools.partial(
                self._literal,
                operation=codex.query.EQ,
                inversion=True
            ),
            re.compile(r'(.*)'): functools.partial(
                self._literal,
                operation=codex.query.EQ
            )
        }
