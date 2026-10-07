"""Core data processing: CSV loading, descriptive statistics, linear regression."""

from __future__ import annotations

import csv
import math
import statistics
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FitResult:
    """Result of a least-squares linear fit y = slope * x + intercept."""

    slope: float
    intercept: float
    r_squared: float

    def predict(self, x: float) -> float:
        return self.slope * x + self.intercept


class Dataset:
    """Numeric columns loaded from a CSV file with a header row."""

    def __init__(self, columns: dict[str, list[float]]):
        if not columns:
            raise ValueError("Dataset needs at least one column")
        lengths = {len(v) for v in columns.values()}
        if len(lengths) != 1:
            raise ValueError("All columns must have the same length")
        self.columns = columns

    @classmethod
    def from_csv(cls, path: str | Path, delimiter: str = ",") -> Dataset:
        """Load numeric columns from a CSV file. Non-numeric cells raise ValueError."""
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            if reader.fieldnames is None:
                raise ValueError(f"{path}: empty file or missing header row")
            columns: dict[str, list[float]] = {name: [] for name in reader.fieldnames}
            for i, row in enumerate(reader, start=2):
                for name in reader.fieldnames:
                    cell = (row[name] or "").strip()
                    try:
                        columns[name].append(float(cell))
                    except ValueError:
                        raise ValueError(
                            f"{path}, line {i}, column {name!r}: not a number: {cell!r}"
                        ) from None
        return cls(columns)

    def __getitem__(self, name: str) -> list[float]:
        return self.columns[name]

    def __len__(self) -> int:
        return len(next(iter(self.columns.values())))


def describe(values: list[float]) -> dict[str, float]:
    """Descriptive statistics for a sample: n, mean, std, min, median, max."""
    if not values:
        raise ValueError("describe() needs a non-empty sample")
    return {
        "n": len(values),
        "mean": statistics.fmean(values),
        "std": statistics.stdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "median": statistics.median(values),
        "max": max(values),
    }


def linfit(x: list[float], y: list[float]) -> FitResult:
    """Least-squares linear fit y = a*x + b with coefficient of determination R²."""
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    if len(x) < 2:
        raise ValueError("linfit() needs at least two points")
    slope, intercept = statistics.linear_regression(x, y)
    y_mean = statistics.fmean(y)
    ss_tot = sum((yi - y_mean) ** 2 for yi in y)
    ss_res = sum((yi - (slope * xi + intercept)) ** 2 for xi, yi in zip(x, y))
    # ponytail: ss_tot == 0 means y is constant; fit is exact, define R² = 1
    r_squared = 1.0 if math.isclose(ss_tot, 0.0) else 1.0 - ss_res / ss_tot
    return FitResult(slope=slope, intercept=intercept, r_squared=r_squared)
