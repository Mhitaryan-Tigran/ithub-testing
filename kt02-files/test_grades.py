import pytest

from grades import SCORES, average, letter, read

HEADER, ROWS = read()
VALID = [r for r in ROWS if r["ok"]]


def test_letter_scale():
    assert letter(95) == "A"
    assert letter(90) == "A-"
    assert letter(59.9) == "F"


def test_average():
    assert average({"Test1": "100", "Test2": "80", "Test3": "60", "Test4": "40", "Final": "20"}) == 60


@pytest.mark.parametrize("row", ROWS, ids=lambda r: f"line{r['line']}")
def test_row_has_all_columns(row):
    assert row["ok"], f"в строке {len(row['raw'])} полей вместо {len(HEADER)}: {row['raw']}"


@pytest.mark.parametrize("row", VALID, ids=lambda r: r["Last name"])
def test_scores_in_range(row):
    for name in SCORES:
        assert 0 <= float(row[name]) <= 100, f"{name} = {row[name]}"


@pytest.mark.parametrize("row", VALID, ids=lambda r: r["Last name"])
def test_grade_matches_average(row):
    avg = average(row)
    assert row["Grade"] == letter(avg), f"среднее {avg:.2f} соответствует {letter(avg)}, а в файле {row['Grade']}"
