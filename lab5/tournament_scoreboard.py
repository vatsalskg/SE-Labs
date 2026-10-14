"""Track match results and display a small sports tournament scoreboard."""

import secrets
import tempfile

POINTS = {"win": 3, "draw": 1, "loss": 0}
TEAMS = {}
MATCHES = []


def add_team(team_name, players=None):
    """Register a team with empty league statistics and its player list."""
    TEAMS[team_name] = {
        "played": 0,
        "won": 0,
        "drawn": 0,
        "lost": 0,
        "gf": 0,
        "ga": 0,
        "players": list(players) if players is not None else [],
    }


def match_result(home_goals, away_goals):
    """Return which side won a match, or ``draw`` when scores are equal."""
    if home_goals > away_goals:
        return "home"
    if home_goals < away_goals:
        return "away"
    return "draw"


def record_match(home, away, home_goals, away_goals):
    """Record a match and update both teams' statistics."""
    if home not in TEAMS or away not in TEAMS:
        raise ValueError("both teams must be registered before a match")
    if home == away:
        raise ValueError("a team cannot play against itself")
    if not all(
        isinstance(goals, int) and goals >= 0
        for goals in (home_goals, away_goals)
    ):
        raise ValueError("goal counts must be non-negative integers")

    result = match_result(home_goals, away_goals)
    sides = ((home, home_goals, away_goals), (away, away_goals, home_goals))
    for team, scored, conceded in sides:
        TEAMS[team]["played"] += 1
        TEAMS[team]["gf"] += scored
        TEAMS[team]["ga"] += conceded
    if result == "draw":
        TEAMS[home]["drawn"] += 1
        TEAMS[away]["drawn"] += 1
    else:
        winner, loser = (home, away) if result == "home" else (away, home)
        TEAMS[winner]["won"] += 1
        TEAMS[loser]["lost"] += 1
    MATCHES.append((home, away, home_goals, away_goals))


def points(team_name):
    """Return a team's league points."""
    stats = TEAMS[team_name]
    return stats["won"] * POINTS["win"] + stats["drawn"] * POINTS["draw"]


def goal_difference(team_name):
    """Return goals scored minus goals conceded for a team."""
    return TEAMS[team_name]["gf"] - TEAMS[team_name]["ga"]


def league_table():
    """Return team names ordered by points and then goal difference."""
    return sorted(
        TEAMS,
        key=lambda team_name: (points(team_name), goal_difference(team_name)),
        reverse=True,
    )


def is_top_two(team_name):
    """Return whether a team is among the first two in the current table."""
    return team_name in league_table()[:2]


def toss_coin():
    """Return a cryptographically strong random coin toss result."""
    return secrets.choice(["Heads", "Tails"])


def table_file_path():
    """Create and return a unique temporary JSON path for table output."""
    with tempfile.NamedTemporaryFile(
        suffix=".json", delete=False
    ) as temp_file:
        return temp_file.name


def main():
    """Run the scoreboard demonstration."""
    for name in ["Royal Strikers", "City Rovers", "Lake United"]:
        add_team(name)
    add_team("Hill Warriors")
    print("Toss:", toss_coin())
    record_match("Royal Strikers", "City Rovers", 2, 1)
    record_match("Lake United", "Hill Warriors", 0, 0)
    record_match("City Rovers", "Lake United", 3, 2)
    record_match("Hill Warriors", "Royal Strikers", 1, 1)
    print("Pos Team Played Won Drawn Lost Pts")
    for pos, name in enumerate(league_table(), 1):
        stats = TEAMS[name]
        print(
            pos,
            name,
            stats["played"],
            stats["won"],
            stats["drawn"],
            stats["lost"],
            points(name),
        )
    print(
        "Is City Rovers in the top two?",
        is_top_two("City Rovers"),
    )
    print("Matches played:", len(MATCHES))


if __name__ == "__main__":
    main()
