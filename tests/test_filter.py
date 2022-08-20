from pathlib import Path

import pytest
from fileswitch.filters import (
    ContentFilter,
    HelloWorldFilter,
    MatchAny,
    NotHelloWorldFilter,
    RegexFilter,
    SimpleTxtFileFilter,
)


@pytest.fixture
def files():
    file_1 = Path("file_1.txt")
    file_2 = Path("file_2.txt")
    hello_world_file = Path("Hello World.txt")
    return [file_1, file_2, hello_world_file]


@pytest.mark.usefixtures("files")
def test_hello_world_filter(files):

    file_1, file_2, hello_world_file = files
    hello_world_filter = HelloWorldFilter()
    assert not hello_world_filter.evaluate(file_1)
    assert not hello_world_filter.evaluate(file_2)
    assert hello_world_filter.evaluate(hello_world_file)


@pytest.mark.usefixtures("files")
def test_not_hello_world_filter(files):

    file_1, file_2, hello_world_file = files
    not_hello_world_filter = NotHelloWorldFilter()
    assert not_hello_world_filter.evaluate(file_1)
    assert not_hello_world_filter.evaluate(file_2)
    assert not not_hello_world_filter.evaluate(hello_world_file)


@pytest.mark.usefixtures("files")
def test_match_any(files):

    match_any = MatchAny()
    for f in files:
        assert match_any.evaluate(f)


def test_regex_filter():

    regex_filter = RegexFilter(
        r"(?<=abc)def", "Matches any characters between a-z or A-Z."
    )

    assert regex_filter.evaluate("abcdef")
    assert not regex_filter.evaluate("1565464")


def test_content_filter():
    scanner = SimpleTxtFileFilter(lambda: True, lambda: "Sample description")
    assert isinstance(scanner, ContentFilter)
    assert scanner.evaluate()
    assert scanner.description() == "Sample description"
