import csv
from pathlib import Path

SCORES = ["Test1", "Test2", "Test3", "Test4", "Final"]
SCALE = [(93, "A"), (90, "A-"), (87, "B+"), (83, "B"), (80, "B-"), (77, "C+"), (73, "C"), (70, "C-"), (67, "D+"), (63, "D"), (60, "D-"), (0, "F")]


def read(path=Path(__file__).with_name("grades.csv")):
    with open(path, newline="") as f:
        reader = csv.reader(f, skipinitialspace=True)
        header = [h.strip() for h in next(reader)]
        rows = []
        for line_no, raw in enumerate(reader, start=2):
            if not raw:
                continue
            rows.append({"line": line_no, "raw": raw, "ok": len(raw) == len(header), **dict(zip(header, [v.strip() for v in raw]))})
    return header, rows


def average(row):
    return sum(float(row[name]) for name in SCORES) / len(SCORES)


def letter(avg):
    return next(grade for limit, grade in SCALE if avg >= limit)


if __name__ == "__main__":
    _, rows = read()
    for row in rows:
        if not row["ok"]:
            print(f"строка {row['line']}: повреждена ({len(row['raw'])} полей вместо 9)")
            continue
        avg = average(row)
        print(f"{row['Last name']:<10} {avg:6.2f}  ожидается {letter(avg):<2}  в файле {row['Grade']}")
