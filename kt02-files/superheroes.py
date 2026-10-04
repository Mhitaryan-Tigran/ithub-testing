import json
from pathlib import Path

HERE = Path(__file__).parent
NEW = [
    {"name": "Byte Knight", "age": 19, "secretIdentity": "Tigran Mkhitaryan", "powers": ["Debugging at light speed", "Infinite coffee", "Git rebase"]},
    {"name": "Captain Cache", "age": 34, "secretIdentity": "Anna Petrova", "powers": ["Instant recall", "Memory compression"]},
    {"name": "Null Pointer", "age": 25, "secretIdentity": "Unknown", "powers": ["Vanishing", "Crashing systems"]},
]


def build(src=HERE / "SuperHero.json", dst=HERE / "superhero_new.json"):
    squad = json.loads(Path(src).read_text())
    names = {m["name"] for m in squad["members"]}
    squad["members"] += [m for m in NEW if m["name"] not in names]
    squad["members"].sort(key=lambda m: m["age"])
    Path(dst).write_text(json.dumps(squad, ensure_ascii=False, indent=2))
    return squad


if __name__ == "__main__":
    for m in build()["members"]:
        print(f"{m['age']:>8}  {m['name']}")
