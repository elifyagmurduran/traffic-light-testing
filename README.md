# Verification & Reliability — Traffic Light System

A complete software-testing pipeline built around a single small system under test (a traffic-light controller), taking it from informal requirements all the way to automatically-discovered test inputs. Each of the four tasks applies a different verification technique to the *same* code, so the repository reads as one continuous story rather than four disconnected exercises.

> **Course:** Verification & Reliability — M.Sc. Software Engineering, Free University of Bozen-Bolzano (UNIBZ)
> **Assignment 1:** Tasks 1–4, presented through a Python notebook.

---

## Why a traffic light?

A traffic light is the perfect teaching system for *dependability*: it is small enough to read in one sitting, but it has one absolute, life-or-death rule —

> **Two crossing directions (North–South vs East–West) must NEVER both be Green at the same instant.**

Everything in the project is organised around proving that this and the system's other guarantees actually hold. The system is modelled as a single `TrafficLight` class with string colours (`GREEN`, `YELLOW`, `RED`, `FLASHING_RED`), two streets (`NS`, `EW`), configurable phase durations, and a fail-safe that forces all-Red when an unsafe state is detected.

---

## The pipeline at a glance

```
Task 1 — say what the system SHOULD do        user stories  ->  acceptance tests (labelled by dependability)
Task 2 — build it and test it from OUTSIDE     AI-generated code  +  category-partition (black-box) tests
Task 3 — test it from the INSIDE               branch coverage (white-box) + coverage.py
Task 4 — let an ALGORITHM find the inputs       search-based software testing (SBST)
```

Tasks 2, 3, and 4 all target the **same two methods**, chosen once in Task 2 and reused throughout, so the three testing philosophies can be compared directly on identical code.

| Method | Cyclomatic complexity | Loop type | Role |
|---|---|---|---|
| `execute_cycle` | 7 | `for` | the automatic cycle (CC > 3 method) |
| `apply_manual_override(commands)` | 7 | `while` | the human takeover (CC > 2 method, different loop) |
| `is_safe_state` | 5 | nested `for` | bonus method (CC > 4) for the SA-vs-GA comparison |

---

## Repository structure

```
.
├── README.md                         <- you are here
├── docs/                             <- original assignment materials (provided, unmodified)
│   ├── Assignment_Directives          .. the task brief
│   ├── UserStories.txt                .. original (happy-path) user stories
│   ├── acceptance_test_generator.py   .. starter Ollama script we were given
│   └── UsefulCommands.txt             .. lab setup commands
│
├── task1/                            <- requirements: stories -> acceptance tests
│   ├── task1_generate_ats.ipynb
│   ├── UserStories_improved.txt       .. explicit, testable, dependability-labelled stories
│   ├── acceptance_tests_output.txt    .. 8 generated ATs (with timing + model metadata)
│   └── Task1_Comprehensive_Learning_Report.md
│
├── task2/                            <- black-box: AI-generated code + category partition
│   ├── task2_generate_code.ipynb
│   ├── src/traffic_light.py           .. the TrafficLight production class
│   ├── tests/test_traffic_light.py    .. 9 category-partition tests (pytest)
│   ├── radon.md                       .. cyclomatic-complexity measurements
│   └── Task2_Comprehensive_Learning_Report.md
│
├── task3/                            <- white-box: branch coverage
│   ├── task3_whitebox.ipynb
│   ├── src/traffic_light.py           .. self-contained copy of the code under test
│   ├── tests/test_traffic_light_whitebox.py   .. 10 branch-coverage tests
│   ├── tests/_generated_draft_whitebox.py     .. raw Ollama output (process evidence)
│   ├── coverage.md                    .. coverage.py results + interpretation
│   └── Task3_Comprehensive_Learning_Report.md
│
└── task4/                            <- search-based testing (SBST)
    ├── task4_sbst.ipynb               .. search engine + 3 goals + bonus + convergence plot
    ├── src/traffic_light.py           .. self-contained copy of the code under test
    ├── results.md                     .. measured results (fixed seeds, reproducible)
    └── Task4_Comprehensive_Learning_Report.md
```

Each task folder is **self-contained** — it carries its own copy of `traffic_light.py` and its own notebook — so any task can be run and graded in isolation.

---

## Task 1 — Acceptance tests for dependability properties

**Goal.** Turn vague, happy-path user stories into explicit, testable ones, then generate acceptance tests (ATs) that verify the system's *dependability*.

**Four dependability properties** are used as the organising framework:

- **Correctness** — does exactly what the spec says (right colours, order, timing).
- **Reliability** — keeps doing it correctly over time.
- **Robustness** — copes with bad / unexpected situations without breaking.
- **Safety** — never causes a disaster (never two crossing Greens).

Each of the 8 original stories was rewritten to add three things the originals left implicit: a clear **guarantee**, **concrete example values** so tests can actually check them (Green = 30 s, Yellow = 4 s, All-Red = 2 s), and an **invalid case** stating what the system must *refuse* to do. Each story was then labelled with one property, giving a balanced **2 Safety / 2 Correctness / 2 Reliability / 2 Robustness** spread.

**Tooling.** A Jupyter notebook parses the improved stories, extracts each story's name and dependability label, and sends them **one at a time** to a locally-run LLM (**Ollama / llama3**) with the label embedded in the prompt — a deliberate improvement over the provided starter script, which sent the whole file as one undifferentiated blob. Output is written to a structured file with a timestamp, the model name, and the generation time.

**Result.** 8 acceptance tests, one per story, each with a valid and an invalid case. Total generation time **≈ 49.7 s** (~6.2 s/story).

---

## Task 2 — Black-box test design (category partition)

**Goal.** Generate the production code from the ATs, then design optimised test cases for two non-trivial methods.

1. **Code generation.** The whole `TrafficLight` class is generated in a single Ollama prompt (methods share state and call one another, so piecemeal generation produces inconsistent fragments). The only manual fix was adding an omitted `import time` — recorded honestly as a one-line correction.
2. **Complexity measurement.** `radon` measured the cyclomatic complexity of every method objectively (not guessed), driving the choice of `execute_cycle` (CC 7, `for`) and `apply_manual_override` (CC 7, `while`).
3. **Testability refactor.** `apply_manual_override` originally called `input()`, which would hang an automated test forever. It was refactored to take a `commands` list — preserving the `while` loop and the cyclomatic complexity while making it unit-testable. This is standard "separate I/O from logic" practice.
4. **Category partition.** Inputs were grouped into equivalence partitions, one representative tested per partition, and **redundant / infeasible partitions removed** — including the "unsynchronised green" partition, which is infeasible because two greens is already an *unsafe* state caught earlier.

**Result.** **9 non-redundant tests** (4 for `execute_cycle`, 5 for `apply_manual_override`), all passing under `pytest`. Durations are zeroed in the test helper so the suite is fast and deterministic. A safety-logic quirk was logged as a finding for Task 3 (see below).

---

## Task 3 — White-box test design (branch coverage)

**Goal.** Test the same two methods from the *inside*, exercising their control-flow structure.

**Technique chosen: branch coverage**, with a justification rather than a default. Condition coverage sits at the top of the course's coverage ladder (`method < statement < branch < condition`), but it only adds tests over branch coverage when a decision is *compound* (`if a and b`). Neither target method contains an `and`/`or` in its own body, so condition coverage **collapses into** branch coverage here — making branch coverage the strongest *meaningful* criterion, which also **subsumes** statement and method coverage. That subsumption is proven objectively with `coverage.py --branch`, not merely asserted.

Each method's decisions were enumerated by hand, and the minimal set of inputs that flips every reachable decision both True and False was designed manually (the graded reasoning), then turned into pytest code with Ollama and verified.

**Headline finding — an infeasible branch.** In `execute_cycle`, the `else` arm of the synchronisation check (`set_all_red(); return`) is **dead code under the safety precondition**: reaching it would require two crossing greens, which the earlier safety check has already rejected. `coverage.py` reporting that branch as "missed" is therefore the tool *confirming* the analysis, not a gap — the white-box twin of the infeasible partition removed in Task 2.

**Result.** **10 tests** (4 + 6), all passing. `apply_manual_override` reaches 100 % statement and branch coverage; `execute_cycle` covers every *feasible* branch.

---

## Task 4 — Search-based software testing (SBST)

**Goal.** Let search algorithms find test inputs automatically, for three coverage goals on the same two methods, plus a bonus comparison.

SBST is framed as an optimisation problem with three ingredients: a **representation** (how a candidate input is encoded), a **fitness function** (lower is better, 0 = goal met), and a **search algorithm**. Because the methods take object *state* (`execute_cycle`) and *command sequences* (`apply_manual_override`) rather than numbers, custom encodings and tweak/crossover/mutation operators were designed for each. A lightweight coverage probe (via `sys.settrace`) records which lines each run executes, and fitness uses **approach level** + **branch distance** to give the search a gradient instead of blind hit/miss.

The search engine is built **from scratch** (random search, hill climbing with restarts, simulated annealing, genetic algorithm) for full transparency. Three goals were pursued:

- **Branch coverage** via greedy set-cover — rediscovers the Task 3 branch set (9/9 feasible for `execute_cycle` with a 4-input suite; 10/10 for `apply_manual_override` with 5).
- **Target node** reachability — all reachable targets hit, while the infeasible D5 branch **provably stalls at cost 1**, *empirically* confirming the Task 3 dead-code finding by an independent method.
- **Path coverage** — both chosen paths fully matched.

**Bonus — Simulated Annealing vs Genetic Algorithm** on `is_safe_state` (CC 5), using the *same* branch-distance fitness `|code_NS − code_EW|` for a fair comparison:

| Algorithm | Solved | Mean evaluations (30 runs) |
|---|---|---|
| Simulated Annealing | 30/30 | 201 |
| Genetic Algorithm | 30/30 | 252 |

Both always succeed; SA is more efficient on this small, smooth landscape, with the honest caveat that the ranking would likely reverse on larger, rugged, multi-modal spaces where the GA's broader exploration pays off.

---

## Techniques & tools demonstrated

| Area | What's shown |
|---|---|
| Requirements engineering | rewriting stories into explicit guarantees + invalid cases, dependability labelling |
| AI-assisted generation | local LLM (Ollama / llama3) for ATs, production code, and test code — with honest logging of manual fixes |
| Complexity analysis | `radon` cyclomatic complexity to drive objective method selection |
| Black-box testing | category partition with redundant/infeasible-case removal |
| White-box testing | branch coverage, the coverage ladder, subsumption, dead-code detection, `coverage.py` |
| Search-based testing | fitness design, approach level + branch distance, hill climbing / SA / GA from scratch |
| Test discipline | testing code *as written* (logging quirks), deterministic suites, reproducible seeds |

---

## Running it locally

**Prerequisites:** Python 3, [Ollama](https://ollama.com) with the `llama3` model, and Jupyter.

```bash
# 1. Install and start Ollama, then pull the model
ollama serve            # leave running in its own terminal
ollama pull llama3      # served at http://localhost:11434

# 2. Set up a Python environment
python3 -m venv venv
source venv/bin/activate
pip install requests radon coverage pytest notebook ipykernel jupytext

# 3. Register the kernel for the notebooks
python -m ipykernel install --user --name=venv --display-name "Python (venv)"
```

**Run a task's notebook:**

```bash
jupyter notebook task1/task1_generate_ats.ipynb
```

**Run the test suites:**

```bash
# Task 2 — category-partition tests
pytest task2/tests/ -v

# Task 3 — white-box tests, with branch coverage
coverage run --branch -m pytest task3/tests/
coverage report -m --include="*traffic_light.py"

# Measure complexity (Task 2 method selection)
python -m radon cc task2/src/traffic_light.py -s -a
```

> **Note:** the AI-generation steps require Ollama to be running. The test suites and coverage/complexity measurements do not — they run against the committed `traffic_light.py` in each task folder.

---

## A note on dependability findings

Two findings recur through the project and are worth calling out, because they show the testing *worked*:

1. **The infeasible branch** in `execute_cycle` — discovered analytically in Task 3 (white-box), then confirmed empirically in Task 4 (search stalls and never reaches it). Two independent methods reaching the same conclusion.
2. **The "all-Red is flagged unsafe" quirk** — `is_safe_state` treats *any* two equal colours as unsafe, so even all-Red is reported unsafe. Rather than silently "fixing" the generated code, every later test was designed around the code's *actual* behaviour and the quirk was documented — honest testing discipline that then shaped the SBST inputs in Task 4.

---

## Deliverables & process

Each task produces a notebook (the demonstrable artifact for the presentation), a one-page report, and its code/test artifacts. The full teaching write-ups — `TaskN_Comprehensive_Learning_Report.md` in each folder — explain the *why* behind every decision and are the source material the one-page reports were condensed from.

Process followed per task: implement → verify → open a tracking issue → close it on completion.