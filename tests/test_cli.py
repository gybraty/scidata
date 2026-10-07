from scidata.__main__ import main


def test_cli_prints_stats_and_fit(tmp_path, capsys):
    p = tmp_path / "data.csv"
    p.write_text("x,y\n0,1\n1,3\n2,5\n", encoding="utf-8")
    assert main([str(p), "x", "y"]) == 0
    out = capsys.readouterr().out
    assert "fit: y = 2 * x + 1" in out
    assert "R² = 1.000000" in out


def test_cli_missing_file_returns_error(tmp_path, capsys):
    assert main([str(tmp_path / "nope.csv"), "x", "y"]) == 1
    assert "error:" in capsys.readouterr().err


def test_cli_saves_plot(tmp_path):
    p = tmp_path / "data.csv"
    p.write_text("x,y\n0,1\n1,3\n2,5\n", encoding="utf-8")
    png = tmp_path / "plot.png"
    assert main([str(p), "x", "y", "-o", str(png)]) == 0
    assert png.exists() and png.stat().st_size > 0
