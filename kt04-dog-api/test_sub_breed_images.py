def test_sub_breed_images_success(api):
    body = api.get("breed/hound/afghan/images").json()
    assert body["status"] == "success"
    assert len(body["message"]) > 0


def test_sub_breed_images_path(api):
    images = api.get("breed/hound/afghan/images").json()["message"]
    assert all("/breeds/hound-afghan/" in url for url in images)


def test_sub_breed_random_image(api):
    url = api.get("breed/hound/afghan/images/random").json()["message"]
    assert "/breeds/hound-afghan/" in url


def test_sub_breed_random_images_count(api):
    assert len(api.get("breed/hound/afghan/images/random/3").json()["message"]) == 3


def test_unknown_sub_breed_404(api):
    response = api.get("breed/hound/nosuchsub/images", expected_status=404)
    assert response.status_code == 404
    assert "not found" in response.json()["message"].lower()
