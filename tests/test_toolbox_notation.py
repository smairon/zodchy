"""
Tests for the toolbox.notation module.
"""

import pytest
from collections.abc import Mapping
from zodchy.toolbox.notation import (
    ParserContract,
    ParamName,
    ParamValue,
)
from zodchy.codex.operator import ClauseStream


class TestParserContract:
    """Test class for ParserContract protocol."""

    def test_parser_contract_is_callable(self):
        """Test that ParserContract is a callable protocol."""
        assert hasattr(ParserContract, "__call__")

    def test_parser_implementation_with_string_query(self):
        """Test that a class can implement ParserContract with string query."""
        class SimpleParser:
            def __call__(
                self,
                query: str | Mapping[ParamName, ParamValue],
                types_map: Mapping[ParamName, type],
            ) -> ClauseStream:
                if isinstance(query, str):
                    # Simple parser that returns empty stream for string
                    return []
                # For mapping, return a simple clause stream
                result: ClauseStream = []
                for param_name, param_value in query.items():
                    param_type = types_map.get(param_name, str)
                    # Convert value to appropriate type
                    if param_type == int:
                        value = int(param_value)
                    elif param_type == float:
                        value = float(param_value)
                    else:
                        value = str(param_value)
                    from zodchy.codex.operator import EQ
                    result.append((param_name, EQ(value)))
                return result

        parser: ParserContract = SimpleParser()
        assert parser is not None

        # Test with string query
        result = parser("test query", {})
        assert isinstance(result, list)
        assert len(result) == 0

        # Test with mapping query
        query = {"id": "1", "name": "test"}
        types_map = {"id": int, "name": str}
        result = parser(query, types_map)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_parser_implementation_with_mapping_query(self):
        """Test that a class can implement ParserContract with mapping query."""
        class MappingParser:
            def __call__(
                self,
                query: str | Mapping[ParamName, ParamValue],
                types_map: Mapping[ParamName, type],
            ) -> ClauseStream:
                if isinstance(query, str):
                    # Parse string to mapping (simplified)
                    return []
                # Process mapping
                from zodchy.codex.operator import EQ, LIKE, GE, LE
                result: ClauseStream = []
                for param_name, param_value in query.items():
                    param_type = types_map.get(param_name, str)
                    if param_type == int:
                        value = int(param_value)
                        result.append((param_name, EQ(value)))
                    elif param_type == str:
                        if "%" in param_value or "_" in param_value:
                            result.append((param_name, LIKE(param_value)))
                        else:
                            result.append((param_name, EQ(param_value)))
                    else:
                        result.append((param_name, EQ(param_value)))
                return result

        parser: ParserContract = MappingParser()
        assert parser is not None

        # Test with mapping query
        query = {"id": "42", "name": "test%", "age": "25"}
        types_map = {"id": int, "name": str, "age": int}
        result = parser(query, types_map)
        assert isinstance(result, list)
        assert len(result) == 3

        # Verify the results
        result_dict = dict(result)
        assert "id" in result_dict
        assert "name" in result_dict
        assert "age" in result_dict

    def test_parser_with_complex_types(self):
        """Test parser with complex type mappings."""
        class ComplexParser:
            def __call__(
                self,
                query: str | Mapping[ParamName, ParamValue],
                types_map: Mapping[ParamName, type],
            ) -> ClauseStream:
                from zodchy.codex.operator import EQ, SET, RANGE, GE, LE
                result: ClauseStream = []
                if isinstance(query, str):
                    return result

                for param_name, param_value in query.items():
                    param_type = types_map.get(param_name, str)
                    if param_name.endswith("_range"):
                        # Handle range queries
                        parts = str(param_value).split("-")
                        if len(parts) == 2:
                            left = GE(int(parts[0])) if parts[0] else None
                            right = LE(int(parts[1])) if parts[1] else None
                            result.append((param_name.replace("_range", ""), RANGE(left, right)))
                    elif param_name.endswith("_in"):
                        # Handle set queries
                        values = [v.strip() for v in str(param_value).split(",")]
                        typed_values = [param_type(v) for v in values]
                        result.append((param_name.replace("_in", ""), SET(*typed_values)))
                    else:
                        # Regular equality
                        value = param_type(param_value)
                        result.append((param_name, EQ(value)))
                return result

        parser: ParserContract = ComplexParser()
        assert parser is not None

        query = {
            "id": "1",
            "age_range": "18-65",
            "status_in": "active,pending",
        }
        types_map = {"id": int, "age": int, "status": str}
        result = parser(query, types_map)
        assert isinstance(result, list)
        assert len(result) == 3


class TestParamTypes:
    """Test class for parameter type aliases."""

    def test_param_name_type(self):
        """Test ParamName type alias."""
        name: ParamName = "test_param"
        assert isinstance(name, str)

    def test_param_value_type(self):
        """Test ParamValue type alias."""
        value: ParamValue = "test_value"
        assert isinstance(value, str)

