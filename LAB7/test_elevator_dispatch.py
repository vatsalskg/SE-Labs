"""Property-based fuzz tests - Vatsal Gupta, PES1UG24CS702."""

from hypothesis import given, settings, strategies as st
from elevator_dispatch import parse_request, total_travel, load_percent

settings.register_profile("lab7", max_examples=500, derandomize=True, deadline=None)
settings.load_profile("lab7")

inputs = st.one_of(
    st.none(), st.text(max_size=500), st.integers(), st.floats(),
    st.booleans(), st.binary(max_size=100),
    st.lists(st.integers(), max_size=20),
    st.dictionaries(st.text(max_size=10), st.integers(), max_size=5),
)
floors = st.integers(min_value=-10**12, max_value=10**12)


@given(inputs)
def test_parse_request_no_crash(value):
    result = parse_request(value)
    assert result is None or (
        isinstance(result, tuple) and len(result) == 2
        and all(type(n) is int for n in result)
    )


@given(inputs)
def test_total_travel_no_crash(value):
    result = total_travel(value)
    assert result is None or (type(result) is int and result >= 0)


@given(inputs)
def test_load_percent_no_crash(value):
    result = load_percent(value)
    assert result is None or (type(result) is int and result >= 0)


@given(floors, floors)
def test_request_round_trip(start, end):
    assert parse_request(f"  {start} -> {end}  ") == (start, end)


@given(st.lists(floors, min_size=1, max_size=50))
def test_travel_matches_reference(route):
    expected = sum(abs(b - a) for a, b in zip(route, route[1:]))
    assert total_travel(",".join(map(str, route))) == expected
    assert total_travel(",".join(map(str, reversed(route)))) == expected


@given(st.integers(0, 10**12), st.integers(1, 10**12))
def test_load_matches_reference(load, capacity):
    assert load_percent(f" {load} of {capacity} ") == load * 100 // capacity


def test_invalid_request_regressions():
    for value in [None, "", "1", "1->2->3", "a->2", "1.5->2",
                  "1->", "\u00b2->3", "9" * 65 + "->1", " " * 10001]:
        assert parse_request(value) is None


def test_invalid_travel_regressions():
    for value in [None, "", "1,,3", "one,two", "1,", "1.5,2",
                  "9" * 65, "0," * 5001]:
        assert total_travel(value) is None
    assert total_travel("5") == 0
    assert total_travel("-2, 0, 3") == 5


def test_invalid_load_regressions():
    for value in [None, "", "450", "1 of 0", "-1 of 630", "1 of -2",
                  "one of two", "1 of 2 of 3", "1.5 of 2", "9" * 65 + " of 1"]:
        assert load_percent(value) is None
    assert load_percent("0 of 630") == 0
    assert load_percent("700 of 630") == 111
