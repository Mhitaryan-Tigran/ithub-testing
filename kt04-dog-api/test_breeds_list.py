def test_list_all_success(api):
    response = api.get("breeds/list/all")
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_list_all_structure(all_breeds):
    assert isinstance(all_breeds, dict)
    assert all(isinstance(subs, list) for subs in all_breeds.values())


def test_list_all_contains_known_breeds(all_breeds):
    for breed in ("hound", "pug", "husky", "retriever"):
        assert breed in all_breeds


def test_list_matches_list_all(api, all_breeds):
    flat = api.get("breeds/list").json()["message"]
    assert sorted(flat) == sorted(all_breeds)


def test_breed_names_are_lowercase_words(all_breeds):
    assert all(name.isalpha() and name == name.lower() for name in all_breeds)
