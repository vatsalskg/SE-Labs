import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator


def test_emergency_holds_doors():
    assert door_action(100, False, True) == "hold_open"


def test_idle_with_no_requests():
    assert next_direction(3, "idle", []) == "idle"


# next_direction tests
def test_continue_up_when_requests_above():
    assert next_direction(3, "up", [5, 7]) == "up"


def test_change_to_down_when_no_above_but_below():
    assert next_direction(5, "up", [2]) == "down"


def test_up_becomes_idle_when_no_requests():
    assert next_direction(5, "up", []) == "idle"


def test_continue_down_when_requests_below():
    assert next_direction(5, "down", [2, 1]) == "down"


def test_change_to_up_when_no_below_but_above():
    assert next_direction(5, "down", [7]) == "up"


def test_down_becomes_idle_when_no_requests():
    assert next_direction(5, "down", []) == "idle"


def test_idle_goes_up_if_request_above():
    assert next_direction(3, "idle", [5]) == "up"


def test_idle_goes_down_if_request_below():
    assert next_direction(3, "idle", [1]) == "down"


# door_action tests
def test_overload_condition():
    assert door_action(700, False, False) == "overload"


def test_blocked_door_reopens():
    assert door_action(100, True, False) == "reopen"


def test_normal_close():
    assert door_action(100, False, False) == "close"


# pick_elevator tests
def test_pick_closest_idle_elevator():
    cars = [
        ("A", 2, True),
        ("B", 8, True),
    ]
    assert pick_elevator(cars, 3) == "A"


def test_pick_closest_when_busy_penalty_applied():
    cars = [
        ("A", 2, False),
        ("B", 4, True),
    ]
    assert pick_elevator(cars, 3) == "B"


def test_pick_first_best_match():
    cars = [
        ("A", 5, True),
        ("B", 5, True),
    ]
    assert pick_elevator(cars, 5) == "A"