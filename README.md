# scidata

[![CI](https://github.com/gybraty/scidata/actions/workflows/ci.yml/badge.svg)](https://github.com/gybraty/scidata/actions/workflows/ci.yml)

A small toolkit for processing and visualizing tabular experimental data:
load numeric CSV columns, compute descriptive statistics, fit a least-squares
line `y = a·x + b` with R², and plot the result.

Built as the practical part of the assignment *"Software Development and
Integration"*: it demonstrates Git/GitHub usage, a CI/CD pipeline with
GitHub Actions, automated testing with pytest, and documented technology
choices (see [REPORT.md](REPORT.md)).

## Installation

```bash
git clone https://github.com/gybraty/scidata.git
cd scidata
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

Requires Python ≥ 3.10. The only runtime dependency is `matplotlib`
(statistics and regression use the standard library `statistics` module).

## Usage

### Command line

```bash
python -m scidata examples/thermistor.csv temperature_c resistance_ohm -o fit.png
```

Output:

```
temperature_c: n=13  mean=40  std=19.4722  min=10  median=40  max=70
resistance_ohm: n=13  mean=97.8231  std=9.3407  min=83.5  median=97.8  max=112.3
fit: resistance_ohm = -0.47967 * temperature_c + 117.01
R² = 0.999902
plot saved to fit.png
```

### As a library

```python
from scidata import Dataset, describe, linfit

ds = Dataset.from_csv("examples/thermistor.csv")
print(describe(ds["resistance_ohm"]))
fit = linfit(ds["temperature_c"], ds["resistance_ohm"])
print(fit.slope, fit.intercept, fit.r_squared)
print(fit.predict(42.0))
```

## Development

```bash
pytest          # run the test suite
ruff check .    # lint
```

Every push and pull request to `main` runs lint + tests on Python 3.10,
3.12 and 3.13 via [GitHub Actions](.github/workflows/ci.yml).

## Project layout

```
scidata/
├── scidata/            # package: core.py (stats, fit), plot.py, __main__.py (CLI)
├── tests/              # pytest suite (unit + CLI tests)
├── examples/           # sample experimental dataset
├── .github/workflows/  # CI pipeline
├── REPORT.md           # theoretical report for the assignment
└── pyproject.toml      # metadata, dependencies, tool config
```

## License

[MIT](LICENSE)
