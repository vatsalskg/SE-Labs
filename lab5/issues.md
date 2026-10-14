# Static analysis findings

The first three issues below are ordered by analyzer severity. Line numbers refer to the original `tournament_scoreboard.py`.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection risk (`B605`) | Security — High | 69–71 | `publishTable` passed a caller-controlled server string to `os.system`, which invokes a shell. | Removed the unused publishing helper. The demo had no publish workflow, and retaining a shell-based helper created an avoidable injection risk. |
| Unsafe temporary filename (`B306`) | Security — Medium | 64–66 | `tempfile.mktemp` selected a path without safely creating the file, leaving a race window. | Replaced it with `NamedTemporaryFile(suffix=".json", delete=False)` and return the securely created file's path. |
| Shared mutable default (`W0102`) | Correctness — Pylint warning | 11 | The default `players=[]` object was shared across calls, so changes through one team's list could affect another. | Changed the default to `None` and create a new list for each team. |
| Hard-coded password (`B105`) | Security — Low | 6 | An unused referee password was embedded in source. | Removed the unused constant; no credential is needed by the scoreboard demo. |
| Non-cryptographic random source (`B311`) | Security — Low | 60–61 | `random.choice` is not suitable when a coin toss must be unpredictable. | Used `secrets.choice` for the toss. |
| Unsafe top-two indexing | Correctness — code review | 56–58 | Indexing `table[0]` and `table[1]` raises `IndexError` when fewer than two teams are registered. | Check membership in `league_table()[:2]`, which also handles an empty table. |
| Unnecessary branch and comparisons (`R1705`, `R1714`) | Maintainability — Pylint refactor | 17–18, 58 | The result function used `elif`/`else` after returns, and the top-two check compared two values separately. | Returned directly from each score comparison and used membership in the first two table entries. |
| PEP 8 whitespace | Style — Flake8 | 5, 60, 79, 87 | The points dictionary, function spacing, match call, and inline comment had whitespace violations. | Applied Flake8 formatting and wrapped long lines. |
| Missing documentation and non-snake-case names | Maintainability — Pylint | 1, 11–74 | The module and functions lacked docstrings, and several function and parameter names used camelCase. | Added a module docstring and function docstrings; renamed functions and parameters to snake_case. |

## Verification

- Pylint before: **4.75/10**; after: **10.00/10**.
- Bandit before: **1 high, 1 medium, 2 low** findings; after: **no findings**.
- Flake8 before: **4** findings; after: **no findings**.
- The before and after tool reports are included in this folder.
