def test_sub_breed_list_success(api):
    body = api.get("breed/hound/list").json()
    assert body["status"] == "success"
    assert "afghan" in body["message"]


def test_sub_breed_list_matches_list_all(api, all_breeds):
    assert sorted(api.get("breed/hound/list").json()["message"]) == sorted(all_breeds["hound"])


def test_breed_without_sub_breeds_is_empty(api):
    assert api.get("breed/pug/list").json()["message"] == []


def test_unknown_breed_sub_list_404(api):
    assert api.get("breed/nosuchbreed/list", expected_status=404).status_code == 404


def test_every_sub_breed_has_images(api, all_breeds):
    for sub in all_breeds["retriever"]:
        assert len(api.get(f"breed/retriever/{sub}/images").json()["message"]) > 0
