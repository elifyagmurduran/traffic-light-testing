# Coverage Measurement

Measured with coverage.py (branch mode) over the 10 white-box tests.
Run from inside task3/ with the venv active:

    coverage run --branch -m pytest tests/
    coverage report -m --include="*traffic_light.py"

Output:

    Name                   Stmts   Miss Branch BrPart  Cover   Missing
    ------------------------------------------------------------------
    src\traffic_light.py      94     22     52      5    75%   22-23, 32, 36-37, 42, 47, 53-57, 60-62, 65-69, 72, 119
    ------------------------------------------------------------------
    TOTAL                     94     22     52      5    75%

Only the two target methods matter here:

- execute_cycle: the only missed lines are 22-23, which is the else branch under
  check_synchronization. That branch needs two greens at once, but two greens is
  unsafe and already caught earlier at D2 — so it can never run. Every reachable
  branch is covered.
- apply_manual_override: nothing missed. 100% statement and branch coverage.

The 75% file total is low only because the file has other methods this task doesn't
target (manual_override, power_failure_recovery, the setters). Their lines are
expected to be uncovered.

# Results

Test code generation (Ollama / llama3): 32.4s (3356 chars)
Test suite: 10 passed in 0.05s

  4 tests for execute_cycle (branch coverage, for-loop)
  6 tests for apply_manual_override (branch coverage, while-loop)

Coverage details are in coverage.md.