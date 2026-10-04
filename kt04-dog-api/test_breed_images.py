def test_breed_images_success(api):
    body = api.get("breed/hound/images").json()
    assert body["status"] == "success"
    assert len(body["message"]) > 0


def test_breed_images_belong_to_breed(api):
    images = api.get("breed/pug/images").json()["message"]
    assert all("/breeds/pug/" in url for url in images)


def test_breed_random_image(api):
    url = api.get("breed/husky/images/random").json()["message"]
    assert "/breeds/husky/" in url


def test_breed_random_images_count(api):
    images = api.get("breed/husky/images/random/4").json()["message"]
    assert len(images) == 4


def test_unknown_breed_404(api):
    response = api.get("breed/nosuchbreed/images", expected_status=404)
    assert response.status_code == 404
    assert response.json()["status"] == "error"
