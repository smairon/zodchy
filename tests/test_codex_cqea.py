"""
Tests for the codex.cqea module.
"""

from zodchy.codex.cqea import (
    Message,
    Task,
    Command,
    Query,
    Event,
    Error,
    View,
)
from zodchy.codex.operator import ClauseStream


class TestTask:
    """Test class for Task base class."""

    def test_task_inherits_from_message(self):
        """Test that Task inherits from Message."""
        assert issubclass(Task, Message)


class TestCommand:
    """Test class for Command base class."""

    # type: ignore

    def test_command_inherits_from_task(self):
        """Test that Command inherits from Task."""
        assert issubclass(Command, Task)

    def test_command_inherits_from_message(self):
        """Test that Command inherits from Message."""
        assert issubclass(Command, Message)


class TestQuery:
    """Test class for Query base class."""

    def test_query_inherits_from_task(self):
        """Test that Query inherits from Task."""
        assert issubclass(Query, Task)

    def test_query_inherits_from_message(self):
        """Test that Query inherits from Message."""
        assert issubclass(Query, Message)

    def test_query_has_iter_method(self):
        """Test that Query has __iter__ method defined."""
        assert hasattr(Query, "__iter__")

    def test_query_iter_is_abstract(self):
        """Test that Query.__iter__ is abstract."""

        class ConcreteQuery(Query):
            def __iter__(self) -> ClauseStream:
                return iter([])

        query = ConcreteQuery()
        result = list(query)
        assert result == []


class TestEvent:
    """Test class for Event base class."""

    def test_event_inherits_from_message(self):
        """Test that Event inherits from Message."""
        assert issubclass(Event, Message)


class TestError:
    """Test class for Error base class."""


    def test_error_inherits_from_message(self):
        """Test that Error inherits from Message."""
        assert issubclass(Error, Message)


class TestView:
    """Test class for View base class."""

    def test_view_inherits_from_event(self):
        """Test that View inherits from Event."""
        assert issubclass(View, Event)

    def test_view_inherits_from_message(self):
        """Test that View inherits from Message."""
        assert issubclass(View, Message)

    def test_view_has_data_method(self):
        """Test that View has data method defined."""
        assert hasattr(View, "data")

    def test_view_data_is_abstract(self):
        """Test that View.data is abstract."""
        class ConcreteView(View):
            def data(self):
                return {"key": "value"}

        view = ConcreteView()
        assert view.data() == {"key": "value"}

    def test_view_has_meta_method(self):
        """Test that View has meta method defined."""
        assert hasattr(View, "meta")

    def test_view_meta_default_returns_none(self):
        """Test that View.meta default implementation returns None."""
        class ConcreteView(View):
            def data(self):
                return {"key": "value"}

        view = ConcreteView()
        assert view.meta() is None

    def test_view_meta_can_be_overridden(self):
        """Test that View.meta can be overridden."""
        class ConcreteView(View):
            def data(self):
                return {"key": "value"}

            def meta(self):
                return {"version": "1.0"}

        view = ConcreteView()
        assert view.meta() == {"version": "1.0"}


class TestCQEAHierarchy:
    """Test class for CQEA class hierarchy."""

    def test_task_is_message(self):
        """Test that Task is a Message."""
        assert issubclass(Task, Message)

    def test_command_is_task(self):
        """Test that Command is a Task."""
        assert issubclass(Command, Task)

    def test_query_is_task(self):
        """Test that Query is a Task."""
        assert issubclass(Query, Task)

    def test_event_is_message(self):
        """Test that Event is a Message."""
        assert issubclass(Event, Message)

    def test_view_is_event(self):
        """Test that View is an Event."""
        assert issubclass(View, Event)

    def test_view_is_message(self):
        """Test that View is a Message."""
        assert issubclass(View, Message)

    def test_concrete_implementations(self):
        """Test that concrete implementations work correctly."""

        class MyCommand(Command):
            pass

        class MyQuery(Query):
            def __iter__(self) -> ClauseStream:
                return iter([])

        class MyEvent(Event):
            pass

        class MyError(Error):
            pass

        class MyView(View):
            def data(self):
                return {"result": "data"}

        # Should be able to instantiate concrete classes
        command = MyCommand()
        assert isinstance(command, Command)
        assert isinstance(command, Task)
        assert isinstance(command, Message)

        query = MyQuery()
        assert isinstance(query, Query)
        assert isinstance(query, Task)
        assert isinstance(query, Message)
        assert list(query) == []

        event = MyEvent()
        assert isinstance(event, Event)
        assert isinstance(event, Message)

        error = MyError()
        assert isinstance(error, Error)
        assert isinstance(error, Message)

        view = MyView()
        assert isinstance(view, View)
        assert isinstance(view, Event)
        assert isinstance(view, Message)
        assert view.data() == {"result": "data"}
        assert view.meta() is None
