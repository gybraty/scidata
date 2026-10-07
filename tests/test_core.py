import math

import pytest

from scidata.core import Dataset, describe, linfit


def test_describe_basic():
    stats = describe([1.0, 2.0, 3.0, 4.0])
    assert stats["n"] == 4
    assert stats["mean"] == pytest.approx(2.5)
    assert stats["median"] == pytest.approx(2.5)
    assert stats["min"] == 1.0
    assert stats["max"] == 4.0
    assert stats["std"] == pytest.approx(math.sqrt(5 / 3))


def test_describe_single_value_has_zero_std():
    assert describe([7.0])["std"] == 0.0


def test_describe_empty_raises():
    with pytest.raises(ValueError):
        describe([])


def test_linfit_exact_line():
    x = [0.0, 1.0, 2.0, 3.0]
    y = [1.0, 3.0, 5.0, 7.0]  # y = 2x + 1
    fit = linfit(x, y)
    assert fit.slope == pytest.approx(2.0)
    assert fit.intercept == pytest.approx(1.0)
    assert fit.r_squared == pytest.approx(1.0)
    assert fit.predict(10.0) == pytest.approx(21.0)


def test_linfit_noisy_data_r_squared_below_one():
    x = [0.0, 1.0, 2.0, 3.0, 4.0]
    y = [0.1, 0.9, 2.2, 2.8, 4.1]
    fit = linfit(x, y)
    assert 0.9 < fit.r_squared < 1.0


def test_linfit_constant_y():
    fit = linfit([0.0, 1.0, 2.0], [5.0, 5.0, 5.0])
    assert fit.slope == pytest.approx(0.0)
    assert fit.r_squared == 1.0


def test_linfit_length_mismatch():
    with pytest.raises(ValueError):
        linfit([1.0, 2.0], [1.0])


def test_linfit_too_few_points():
    with pytest.raises(ValueError):
        linfit([1.0], [1.0])


def test_dataset_from_csv(tmp_path):
    p = tmp_path / "data.csv"
    p.write_text("t,v\n0,1.5\n1,2.5\n2,3.5\n", encoding="utf-8")
    ds = Dataset.from_csv(p)
    assert len(ds) == 3
    assert ds["t"] == [0.0, 1.0, 2.0]
    assert ds["v"] == [1.5, 2.5, 3.5]


def test_dataset_rejects_non_numeric(tmp_path):
    p = tmp_path / "bad.csv"
    p.write_text("a,b\n1,x\n", encoding="utf-8")
    with pytest.raises(ValueError, match="line 2"):
        Dataset.from_csv(p)


def test_dataset_rejects_empty_file(tmp_path):
    p = tmp_path / "empty.csv"
    p.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        Dataset.from_csv(p)
