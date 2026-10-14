# Reflection

The handout refers to four reflection questions but does not include them in the supplied three pages. The prompts and answers below are synthesized from the handout's objective and learning outcomes.

## 1. What does static code analysis contribute?

Static analysis checks source code without running it. It surfaced a high-risk shell call, unsafe temporary-file creation, a shared mutable default, and several readability and formatting problems before those issues caused failures in normal use. It complements running the program because it can flag risky patterns even when a helper is not exercised by the demo.

## 2. How did Pylint, Bandit, and Flake8 differ?

Pylint gave the broadest feedback about maintainability and Python conventions. Bandit focused on security-sensitive APIs and reported the shell call, hard-coded password, weak random source, and temporary-file helper. Flake8 gave short, precise PEP 8 whitespace findings. Running all three exposed different classes of problems in the same small file.

## 3. Which finding mattered most, and how was it fixed?

The high-severity `os.system` call was the most serious because it incorporated a server value into a shell command. The helper was unused by the scoreboard demo, so I removed it instead of retaining an unnecessary remote-publishing feature. I also replaced `tempfile.mktemp` with `NamedTemporaryFile`, removed the unused hard-coded password, and switched the toss to `secrets.choice`. Bandit reported no findings after these changes.

## 4. What are the limits of static analysis, and how would you use it?

Tools report patterns and need human judgment to determine whether a finding matters in the program's context. For example, the weak-randomness finding was low severity for a game-like toss, while the shell helper was unused and could be removed altogether. Static analysis also does not prove the program's behavior is correct. I would run these tools during development or in continuous integration, review the findings, and still run the program's expected workflows.

## Results

The demo still prints the same four-team standings and reports four matches. Pylint improved from 4.75/10 to 10.00/10; Bandit and Flake8 finish without findings. The reports were generated with Pylint 4.1.3, Bandit 1.9.4, and Flake8 7.4.1.
