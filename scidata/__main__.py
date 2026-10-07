"""Command-line interface: python -m scidata data.csv x_column y_column [-o plot.png]"""

from __future__ import annotations

import argparse
import sys

from scidata.core import Dataset, describe, linfit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="scidata",
        description="Describe two numeric CSV columns, fit a line y = a*x + b, "
        "and optionally save a plot.",
    )
    parser.add_argument("csv_file", help="input CSV file with a header row")
    parser.add_argument("x_column", help="name of the independent-variable column")
    parser.add_argument("y_column", help="name of the dependent-variable column")
    parser.add_argument("-o", "--plot", metavar="PNG", help="save a scatter+fit plot to this file")
    args = parser.parse_args(argv)

    try:
        ds = Dataset.from_csv(args.csv_file)
        x, y = ds[args.x_column], ds[args.y_column]
    except (OSError, ValueError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    for name, values in ((args.x_column, x), (args.y_column, y)):
        stats = describe(values)
        print(f"{name}: " + "  ".join(f"{k}={v:.6g}" for k, v in stats.items()))

    fit = linfit(x, y)
    print(f"fit: {args.y_column} = {fit.slope:.6g} * {args.x_column} + {fit.intercept:.6g}")
    print(f"R² = {fit.r_squared:.6f}")

    if args.plot:
        from scidata.plot import plot_fit

        path = plot_fit(x, y, fit, args.plot, xlabel=args.x_column, ylabel=args.y_column)
        print(f"plot saved to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
