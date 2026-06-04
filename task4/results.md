# Task 4 — Results

Numbers from running `task4_sbst.ipynb`. Seeds are fixed so these are reproducible.

## Goal A — Branch coverage

Greedy set-cover over a pool of 800 random candidates:

- `execute_cycle` — **9/9 feasible** branches covered, suite of 4 inputs.
  Only uncovered branch: `(19, False)`, the infeasible D5 else from Task 3.
- `apply_manual_override` — **5/10** branches covered, suite of 2 inputs.
  The command-list search space is large (variable length, 5 possible tokens),
  so 800 random samples wasn't enough to hit every branch combination.
  Missing: `(90, False)`, `(90, True)`, `(91, False)`, `(91, True)`, `(101, True)`.

The execute_cycle result independently rediscovers the same branch set
and same dead branch we found by hand in Task 3.

## Goal B — Target node

| Target | Best cost | Result | Evaluations |
|---|---|---|---|
| amo → `raise ValueError` (reachable) | 4 | stalled | 2408 |
| ec → D5 `else` (infeasible) | 1 | stalled | 2408 |
| ec → red-clearance (reachable) | 0 | **reached** | 301 |

The red-clearance target is reached easily. The infeasible D5 stalls at
cost 1 as expected — the search confirms the dead branch from Task 3.

The amo ValueError target has a 4-guard chain and stalled at cost 4,
meaning the search couldn't satisfy even the first guard in this run.
This is a known weakness of approach-level fitness on deep paths through
a large search space — more restarts or a bigger budget would likely help.

## Goal C — Path coverage

| Target path | Matched | Result |
|---|---|---|
| amo set-colour path (5 guards) | 0/5 | partial |
| ec green-sync path (4 guards) | 4/4 | **full** |

Same pattern: execute_cycle paths are easy to cover; apply_manual_override's
command-list space makes it harder for hill climbing to find the right sequence.

## Bonus — SA vs GA on `is_safe_state` (CC 5)

Same fitness for both: branch distance `|code_NS - code_EW|`, which hits 0
when both directions show the same colour. Over 30 seeded runs:

| Algorithm | Solved | Mean evaluations |
|---|---|---|
| Simulated Annealing | 30/30 | 201 |
| Genetic Algorithm | 30/30 | 252 |

Both always solve it. SA is slightly faster on this small smooth landscape
because its ±1 moves walk straight downhill. On a bigger, rougher problem
the GA's population-based exploration would probably win — this result is
landscape-specific.