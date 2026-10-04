import json

from superheroes import HERE, NEW, build


def test_new_heroes_added():
    squad = build()
    names = [m["name"] for m in squad["members"]]
    assert len(squad["members"]) == 3 + len(NEW)
    for hero in NEW:
        assert hero["name"] in names


def test_sorted_by_age():
    ages = [m["age"] for m in build()["members"]]
    assert ages == sorted(ages)


def test_file_written():
    build()
    data = json.loads((HERE / "superhero_new.json").read_text())
    assert data["squadName"] == "Super hero squad"
    assert [m["age"] for m in data["members"]] == sorted(m["age"] for m in data["members"])


def test_idempotent():
    build()
    assert len(build()["members"]) == 3 + len(NEW)
