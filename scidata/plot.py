"""Visualization: scatter plot of experimental data with fitted line."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless backend: works in CI and over SSH
import matplotlib.pyplot as plt

from scidata.core import FitResult


def plot_fit(
    x: list[float],
    y: list[float],
    fit: FitResult,
    out: str | Path,
    xlabel: str = "x",
    ylabel: str = "y",
    title: str = "",
) -> Path:
    """Save a scatter plot of (x, y) with the fitted line to `out` (PNG). Returns the path."""
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(x, y, label="data", zorder=3)
    xs = [min(x), max(x)]
    ax.plot(
        xs,
        [fit.predict(v) for v in xs],
        color="crimson",
        label=f"fit: y = {fit.slope:.4g}·x + {fit.intercept:.4g} (R² = {fit.r_squared:.4f})",
    )
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()
    out = Path(out)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out
