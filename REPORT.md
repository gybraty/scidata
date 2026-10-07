# Software Development and Integration

**Analytical report**

Project repository: <https://github.com/gybraty/scidata>
CI/CD configuration: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)
CI runs: <https://github.com/gybraty/scidata/actions>

---

## Contents

1. [Introduction](#1-introduction)
2. [Stages and organization of the software development process](#2-stages-and-organization-of-the-software-development-process)
3. [Criteria for selecting technologies and tools](#3-criteria-for-selecting-technologies-and-tools)
4. [Version control systems: Git and GitHub](#4-version-control-systems-git-and-github)
5. [Continuous integration and continuous delivery (CI/CD)](#5-continuous-integration-and-continuous-delivery-cicd)
6. [Features of scientific software development](#6-features-of-scientific-software-development)
7. [Practical part: the `scidata` project](#7-practical-part-the-scidata-project)
8. [Conclusions and challenges](#8-conclusions-and-challenges)
9. [References](#9-references)

---

## 1. Introduction

Modern software is rarely written in a single sitting by a single person. It evolves over
time, is maintained by changing teams, and must keep working as its environment —
operating systems, libraries, data formats — changes underneath it. This makes the
*process* of development as important as the code itself: how work is organized, how
changes are tracked, how quality is verified, and how new versions reach their users.

This report covers the fundamentals of organizing the software development process,
criteria for a justified choice of technologies, version control with Git and GitHub,
and the practices of continuous integration and delivery (CI/CD), with particular
attention to the specifics of scientific software. The practical part is a small but
complete scientific tool, **scidata**, published on GitHub with a working CI pipeline
and an automated test suite.

## 2. Stages and organization of the software development process

### 2.1 The software development life cycle (SDLC)

Regardless of methodology, every software project passes through the same logical
stages, together known as the software development life cycle:

1. **Requirements analysis.** What must the software do, for whom, and under what
   constraints? The output is a set of functional requirements (features, inputs,
   outputs) and non-functional requirements (performance, portability, reliability).
2. **Design.** The architecture of the solution: decomposition into modules, choice of
   data structures and interfaces, selection of technologies. Good design minimizes
   coupling between components so they can be built and tested independently.
3. **Implementation.** Writing the code itself, following agreed conventions (style,
   naming, directory layout) so that the result is readable by others.
4. **Testing.** Verifying that the implementation meets the requirements: unit tests
   for individual functions, integration tests for component interaction, acceptance
   tests for end-to-end behavior.
5. **Deployment / release.** Packaging the software and delivering it to users —
   publishing a package, deploying a service, or releasing an installer.
6. **Maintenance.** Fixing defects, adapting to environment changes, and extending
   functionality. For long-lived software this stage dominates total cost.

### 2.2 Process models

How the stages are *arranged in time* defines the process model:

- **Waterfall** executes the stages strictly in sequence: all requirements first, then
  all design, then all coding, and so on. It is simple to plan and document, but
  fragile: an error discovered during testing may invalidate months of earlier work.
  It suits projects with stable, well-understood requirements (e.g., contractual or
  safety-critical work).
- **Iterative and incremental models** build the system as a series of small, complete
  cycles, each producing a working (if partial) product. Errors and requirement changes
  are discovered early, when they are cheap to fix.
- **Agile methodologies** (Scrum, Kanban, Extreme Programming) are the dominant modern
  family of iterative approaches. Scrum organizes work into fixed-length *sprints*
  (typically 1–4 weeks) with a prioritized backlog, daily stand-up meetings, and a
  review/retrospective at the end of each sprint. Kanban instead limits *work in
  progress* and visualizes flow on a board, which suits continuous maintenance work.
  Agile values working software, short feedback loops, and responsiveness to change
  over exhaustive upfront planning.

In practice most teams use a hybrid: an agile day-to-day process inside a longer-term
roadmap, supported by the engineering practices described later in this report
(version control, code review, CI/CD).

### 2.3 Supporting activities

Three activities run across all stages and are essential to an organized process:

- **Version control** — every change to the code is recorded, attributable, and
  reversible (Section 4).
- **Code review** — a second person reads each change before it is merged, catching
  defects and spreading knowledge of the codebase. On GitHub this is built around
  *pull requests*.
- **Automation** — building, testing, and releasing are performed by machines, not by
  hand, so they are repeatable and cannot be forgotten (Section 5).

## 3. Criteria for selecting technologies and tools

Choosing a language, framework, or library is an engineering decision that should be
justified against explicit criteria rather than fashion. The main criteria are:

1. **Fitness for the task.** Does the technology directly solve the problem class?
   A numerical-computing task points to Python/NumPy, R, or Julia; a low-latency
   system service points to C++, Rust, or Go; a browser UI points to JavaScript or
   TypeScript.
2. **Ecosystem and libraries.** Mature, maintained libraries can replace months of
   custom development. The size and health of the package ecosystem (PyPI, npm,
   crates.io) is a direct productivity factor.
3. **Team expertise and learning curve.** A technically "better" tool that nobody on
   the team knows carries real cost and risk. Familiarity shortens development time
   and reduces defect rates.
4. **Community, documentation, and longevity.** Active development, good documentation,
   a large user community, and a credible maintenance story (foundation backing,
   multiple maintainers) reduce the risk of the dependency being abandoned.
5. **Licensing.** The license must be compatible with the intended use. Permissive
   licenses (MIT, BSD, Apache-2.0) allow nearly any use; copyleft licenses (GPL)
   impose obligations on derivative works.
6. **Portability and deployment constraints.** Target platforms, installation
   complexity, and resource requirements. A tool that only its author can install
   will not be used.
7. **Performance — when it matters.** Performance requirements should be stated and
   measured, not assumed. Choosing a harder, faster technology for a workload that a
   simpler one handles comfortably is a common and costly mistake.
8. **Minimal sufficient complexity.** Every added dependency is code that must be
   trusted, updated, and secured. A standard-library solution is preferable to a
   third-party package that does the same job ("use the platform first").

A useful discipline is to write the justification down (as done for `scidata` in
Section 7.2): if a choice cannot be defended in a paragraph, it is probably not a
deliberate choice.

## 4. Version control systems: Git and GitHub

### 4.1 Why version control

A version control system (VCS) records the history of a set of files as a sequence of
*commits* — snapshots with an author, a timestamp, and a message. This provides:

- a complete, attributable **history** of every change (who, when, why);
- safe **experimentation** via branches, isolated from the stable code;
- **collaboration** without overwriting each other's work, with explicit merging;
- the ability to **reproduce any past state** of the project — crucial in science,
  where a published result must be traceable to the exact code that produced it.

### 4.2 Generations of VCS and why Git won

Centralized systems (CVS, Subversion) store history on a single server; developers
check out a working copy and commit over the network. This creates a single point of
failure and makes branching and offline work awkward.

**Distributed** systems (Git, Mercurial) give every developer a full local copy of the
repository, including all history. Commits, branches, diffs, and history inspection are
local and fast; synchronization between repositories (`push`/`pull`) is a separate,
explicit step. Git — created by Linus Torvalds in 2005 for Linux kernel development —
became the de facto standard due to its speed, its very cheap branching model, and the
network effect of GitHub. Mercurial is conceptually similar and arguably friendlier,
but its ecosystem is now marginal by comparison.

Key Git concepts used in this project:

| Concept | Meaning |
|---|---|
| repository | the project directory plus its full history (`.git`) |
| commit | an immutable snapshot with message, author, and parent(s) |
| branch | a movable pointer to a commit; enables parallel lines of work |
| merge / rebase | ways to combine divergent branches |
| remote | another copy of the repository (e.g., on GitHub) to push/pull |
| tag | a permanent label on a commit, typically a release version |

### 4.3 Git hosting platforms: GitHub and alternatives

Git itself is only the version control engine. *Hosting platforms* add collaboration
on top of it:

- **GitHub** — the largest platform (over 100 million repositories). Provides pull
  requests with code review, an issue tracker, project boards, releases, GitHub Pages
  for documentation, and **GitHub Actions** for CI/CD. Free for public and private
  repositories; the default home of open-source and much of scientific software.
- **GitLab** — a close functional equivalent with a strong built-in CI system
  (GitLab CI); can be self-hosted, which enterprises and universities use for data
  sovereignty.
- **Bitbucket** — integrates tightly with Atlassian tools (Jira); less prominent in
  open source.

For this assignment GitHub was chosen because it combines hosting, review, issues, and
CI in one free platform and is the standard venue for sharing scientific code.

### 4.4 Typical workflow

The workflow used in practice (and in this project) is:

```
git init / git clone      # create or copy a repository
git add … ; git commit    # record a logical unit of change locally
git push origin main      # publish to GitHub
# for team work: create a branch, open a pull request,
# pass review and CI, then merge into main
```

Commit messages follow the convention of a short imperative summary line
(optionally typed, e.g. `feat: …`, `fix: …`, `docs: …`), which keeps the history
readable and machine-processable.

## 5. Continuous integration and continuous delivery (CI/CD)

### 5.1 Continuous integration

**Continuous integration (CI)** is the practice of merging all developers' work into a
shared mainline frequently — at least daily — with every merge verified by an
**automated build and test run**. The goal is to detect integration problems within
minutes of their introduction, instead of during a painful "integration phase" weeks
later. Core elements:

- a single source of truth (the repository on GitHub);
- an automated, reproducible build (here: `pip install -e ".[dev]"`);
- an automated test suite that gates every change (here: `pytest` + `ruff`);
- a CI server that runs the pipeline on every push and pull request and reports
  pass/fail status visibly (the green check / red cross on GitHub).

The social contract matters as much as the tooling: a red main branch is everyone's
top priority, and changes are kept small so failures are easy to localize.

### 5.2 Continuous delivery and deployment

**Continuous delivery (CD)** extends CI so that every change that passes the pipeline
produces a *releasable* artifact — a package, container image, or installer — and the
decision to release is a business decision, not a technical scramble. **Continuous
deployment** goes one step further: every passing change is released to production
automatically. The progression is:

```
commit → build → automated tests → artifact → (manual approve) → release
                 └────────── CI ──────────┘  └──────── CD ────────┘
```

### 5.3 Tooling

| Tool | Model | Notes |
|---|---|---|
| **GitHub Actions** | YAML workflows in the repo, hosted runners | zero setup for GitHub projects; free for public repos; large marketplace of reusable actions |
| GitLab CI | `.gitlab-ci.yml`, hosted or own runners | excellent if the code is already on GitLab |
| Jenkins | self-hosted server, plugin-based | maximally flexible, but must be installed, secured, and maintained |

GitHub Actions was chosen for this project: the pipeline lives in the repository
(versioned together with the code it tests), requires no server administration, and
runs free of charge for a public repository.

### 5.4 The pipeline of this project

The workflow [`ci.yml`](.github/workflows/ci.yml) triggers on every push and pull
request to `main` and runs a **matrix** of three Python versions (3.10, 3.12, 3.13).
Each job: checks out the code → installs the package with its dev dependencies →
runs the `ruff` linter → runs the `pytest` suite. A failure in any cell of the matrix
marks the commit red, which blocks merging in a protected-branch setup. The README
displays a live status badge.

## 6. Features of scientific software development

Scientific software differs from commercial software in its purpose — producing
*correct, reproducible results* rather than serving customers — and this changes the
requirements and best practices:

1. **Reproducibility is the primary requirement.** A published result must be
   re-creatable from the exact code version and environment that produced it. This
   demands version control for code *and* pinned, declared dependencies
   (`pyproject.toml`, `requirements.txt`, Conda environments, or containers), and
   tagging the exact commit used for a paper.
2. **Correctness is hard to see.** Unlike a crashing web app, a subtly wrong
   numerical routine produces plausible-looking wrong science. Automated tests with
   known analytical answers (as in `tests/test_core.py`, where a fit against an exact
   line must return slope 2, intercept 1, R² = 1) are the main defense, together with
   validation against published reference results.
3. **Environments are heterogeneous.** The same code runs on a laptop, a departmental
   server, and an HPC cluster. Portability argues for widely available languages and
   for isolating dependencies in virtual environments (`venv`, Conda) or containers
   (Docker, Apptainer/Singularity).
4. **The ecosystem is the platform.** Scientific computing concentrates in a few
   stacks: Python (NumPy, SciPy, pandas, matplotlib, scikit-learn), R for statistics,
   Julia for high-performance numerics, and C/C++/Fortran kernels underneath. Choosing
   inside these ecosystems gives validated algorithms instead of hand-rolled ones.
5. **Developers are domain scientists first.** Code is often written by researchers
   without formal software engineering training, and it outlives its authors
   (students graduate). This raises the value of simplicity, documentation
   (a README that lets a stranger run the code in five minutes), and CI that catches
   regressions after the author has left.
6. **Openness and licensing.** Journals and funders increasingly require published
   code and data. Public repositories with permissive licenses (MIT, BSD, Apache-2.0)
   and citable archives (Zenodo DOIs for tagged releases) are the norm.

Best practice distills to: keep it simple, put everything in Git, declare the
environment, test against known answers, automate the checks, and document how to run
it. The practical project below applies each of these points.

## 7. Practical part: the `scidata` project

### 7.1 What it does

**scidata** (<https://github.com/gybraty/scidata>) is a small Python toolkit for a
routine scientific task: processing tabular experimental data. It loads numeric
columns from a CSV file, computes descriptive statistics (n, mean, standard deviation,
min, median, max), fits a least-squares line *y = a·x + b* with the coefficient of
determination R², and renders a scatter plot with the fitted line. It is usable both
as a library (`from scidata import Dataset, describe, linfit`) and from the command
line:

```bash
python -m scidata examples/thermistor.csv temperature_c resistance_ohm -o fit.png
```

The repository includes an example dataset (`examples/thermistor.csv` — resistance of
a sensor vs. temperature), for which the tool reports a linear fit with R² ≈ 0.9999.

### 7.2 Justification of technology choices

Applying the criteria of Section 3:

- **Language: Python 3.** The lingua franca of scientific computing (criterion:
  fitness for task + ecosystem); runs identically on Linux/macOS/Windows and on every
  CI runner (portability); minimal learning curve for scientists.
- **Statistics: the standard library `statistics` module.** Since Python 3.10 it
  provides `fmean`, `stdev`, `median`, and `linear_regression`. Using it instead of
  NumPy removes a heavyweight dependency that this task does not need (criterion:
  minimal sufficient complexity). R² is computed directly from its definition in a
  few lines.
- **Visualization: matplotlib.** The de facto standard plotting library in science;
  the only runtime dependency. The headless `Agg` backend is selected explicitly so
  that plotting works in CI and on servers without a display.
- **Testing: pytest.** The standard Python test framework: plain `assert` syntax,
  fixtures such as `tmp_path` for file-based tests, and precise floating-point
  comparison with `pytest.approx`.
- **Linting: ruff.** A single fast tool that replaces the flake8/isort/pyupgrade
  stack; keeps style and common bug patterns in check in CI.
- **Packaging: `pyproject.toml` + setuptools.** The current Python packaging
  standard; one file declares metadata, dependencies, and tool configuration, making
  the environment reproducible with a single `pip install -e ".[dev]"`.
- **License: MIT** — the permissive default for scientific code, imposing no
  restrictions on reuse.

### 7.3 Git and GitHub usage

The project was developed in Git from the first commit, with small, typed commit
messages (`feat:`, `test:`, `docs:`, `ci:`). It is published as a public GitHub
repository containing:

- `README.md` with a status badge, installation, usage, and layout documentation;
- `LICENSE` (MIT);
- `.gitignore` excluding environments, caches, and build artifacts;
- this report (`REPORT.md`);
- the Issues tracker enabled for defect reports and feature requests.

### 7.4 CI pipeline and automated testing

Every push and pull request runs the GitHub Actions workflow described in
Section 5.4: lint (`ruff check .`) and the full test suite (`pytest`) on Python 3.10,
3.12, and 3.13. The suite contains 14 tests covering:

- descriptive statistics, including the single-value and empty-input edge cases;
- the linear fit against an exact analytical answer, noisy data, constant *y*
  (degenerate R²), mismatched lengths, and insufficient points;
- CSV loading, including rejection of non-numeric cells (with line/column in the
  error message) and empty files;
- the CLI end-to-end: correct output on valid data, non-zero exit code and a clear
  `stderr` message on a missing file, and actual production of a PNG plot file.

All tests pass locally and in CI; the live status is visible at
<https://github.com/gybraty/scidata/actions>.

## 8. Conclusions and challenges

### Conclusions

This work covered the full minimal loop of modern software development: organizing
work in stages, choosing technologies against explicit criteria, tracking every change
in Git, publishing on GitHub, and gating every change with an automated CI pipeline.
The practical outcome is a small but genuinely complete scientific tool — documented,
licensed, tested on three Python versions on every push, and reproducible by anyone
with `git clone` and `pip install`.

The main lesson is that the engineering practices scale *down* well: even a
few-hundred-line scientific script benefits visibly from version control, declared
dependencies, a handful of tests with known answers, and a CI badge that proves the
code still works.

### Challenges encountered

- **Keeping the dependency set minimal** required resisting the reflex to add NumPy;
  verifying that the standard library `statistics.linear_regression` (Python ≥ 3.10)
  suffices shaped the minimum supported Python version.
- **Headless plotting in CI**: matplotlib defaults to a GUI backend, which fails on
  CI runners without a display; the fix is selecting the `Agg` backend explicitly
  before the first plot.
- **Degenerate numerical cases**: R² is undefined when *y* is constant (division by
  zero in the textbook formula); the implementation defines it as 1.0 for an exact
  fit and this behavior is pinned by a dedicated test.
- **Linter strictness**: ruff flagged stylistic issues (unsorted `__all__`, quoted
  type annotations) that were auto-fixed — a small demonstration of why automated
  style checks belong in the pipeline rather than in code review discussions.

## 9. References

1. Sommerville, I. *Software Engineering*, 10th ed. Pearson, 2015.
2. Beck, K. et al. *Manifesto for Agile Software Development*, 2001. <https://agilemanifesto.org>
3. Chacon, S., Straub, B. *Pro Git*, 2nd ed. Apress, 2014. <https://git-scm.com/book>
4. Fowler, M. *Continuous Integration*, 2024. <https://martinfowler.com/articles/continuousIntegration.html>
5. GitHub Docs: *GitHub Actions*. <https://docs.github.com/actions>
6. Wilson, G. et al. "Best Practices for Scientific Computing." *PLOS Biology* 12(1), 2014.
7. Wilson, G. et al. "Good Enough Practices in Scientific Computing." *PLOS Computational Biology* 13(6), 2017.
8. Python documentation: the `statistics` module. <https://docs.python.org/3/library/statistics.html>
