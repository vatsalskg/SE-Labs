"""Lab 7 - Vatsal Gupta, PES1UG24CS702.

Invalid inputs return None. Signed floors are allowed (including basements).
Loads must be nonnegative and capacities positive; overloads may exceed 100%.
Input length is bounded to avoid excessive parsing work.
"""

import re

MAX_INPUT_LENGTH = 10_000
MAX_INTEGER_DIGITS = 64


def _parts(text, separator, count=None):
    if not isinstance(text, str) or len(text) > MAX_INPUT_LENGTH:
        return None
    parts = text.split(separator)
    if count is not None and len(parts) != count:
        return None
    return parts


def _integer(token):
    token = token.strip()
    if not re.fullmatch(rf"[+-]?[0-9]{{1,{MAX_INTEGER_DIGITS}}}", token):
        return None
    return int(token)


def parse_request(text):
    """Return (start, end), or None for a malformed request."""
    parts = _parts(text, "->", 2)
    if parts is None:
        return None
    start, end = map(_integer, parts)
    return None if start is None or end is None else (start, end)


def total_travel(floors_csv):
    """Return total absolute travel; a single floor has zero travel."""
    parts = _parts(floors_csv, ",")
    if parts is None:
        return None
    floors = [_integer(part) for part in parts]
    if any(floor is None for floor in floors):
        return None
    return sum(abs(b - a) for a, b in zip(floors, floors[1:]))


def load_percent(text):
    """Return the integer percentage, or None for invalid load/capacity."""
    parts = _parts(text, " of ", 2)
    if parts is None:
        return None
    load, capacity = map(_integer, parts)
    if load is None or capacity is None or load < 0 or capacity <= 0:
        return None
    return load * 100 // capacity


def main():
    prompts = [
        ("parse_request", "Enter a request as FROM->TO (e.g. 5->9): ",
         parse_request, "From and To:"),
        ("total_travel", "Enter floors visited as CSV (e.g. 1,5,3,9): ",
         total_travel, "Floors Travelled:"),
        ("load_percent", "Enter load as 'X of Y' (e.g. 450 of 630): ",
         load_percent, "Load Percent:"),
    ]
    for name, prompt, function, label in prompts:
        print(f"==== Running {name} ====")
        try:
            result = function(input(prompt))
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled.")
            return
        print("Invalid input." if result is None else f"{label} {result}")
        print()


if __name__ == "__main__":
    main()
