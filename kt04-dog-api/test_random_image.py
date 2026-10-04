import pytest
import requests


def test_random_image_success(api):
    body = api.get("breeds/image/random").json()
    assert body["status"] == "success"
    assert body["message"].startswith("https://images.dog.ceo/breeds/")


def test_random_image_is_jpg_or_png(api):
    url = api.get("breeds/image/random").json()["message"]
    assert url.lower().endswith((".jpg", ".jpeg", ".png"))


@pytest.mark.parametrize("count", [1, 3, 10])
def test_random_images_count(api, count):
    images = api.get(f"breeds/image/random/{count}").json()["message"]
    assert len(images) == count


def test_random_images_capped_at_50(api):
    images = api.get("breeds/image/random/60").json()["message"]
    assert len(images) == 50


def test_random_image_file_downloads(api):
    url = api.get("breeds/image/random").json()["message"]
    image = requests.get(url, timeout=15)
    assert image.status_code == 200
    assert image.headers["Content-Type"].startswith("image/")
