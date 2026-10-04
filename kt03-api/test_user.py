def make_user(username):
    return {"id": 0, "username": username, "firstName": "Tigran", "lastName": "Mkhitaryan", "email": f"{username}@example.com", "password": "qa-pass-123", "phone": "+70000000000", "userStatus": 1}


def test_create_user(api, username):
    response = api.post("user", make_user(username))
    assert response.status_code == 200
    assert response.json()["code"] == 200


def test_get_user(api, username):
    api.post("user", make_user(username))
    body = api.eventually(f"user/{username}", lambda b: b.get("username") == username)
    assert body["username"] == username
    assert body["email"] == f"{username}@example.com"


def test_update_user(api, username):
    api.post("user", make_user(username))
    user_id = api.eventually(f"user/{username}", lambda b: b.get("username") == username)["id"]
    changed = make_user(username) | {"id": user_id, "firstName": "Tiko", "phone": "+71111111111"}
    assert api.put(f"user/{username}", changed).status_code == 200
    body = api.eventually(f"user/{username}", lambda b: b.get("firstName") == "Tiko")
    assert body["firstName"] == "Tiko"
    assert body["phone"] == "+71111111111"


def test_delete_user(api, username):
    api.post("user", make_user(username))
    assert api.delete(f"user/{username}").status_code == 200
    assert api.get(f"user/{username}", expected_status=404).status_code == 404


def test_update_with_zero_id_does_not_change_user(api, username):
    api.post("user", make_user(username))
    original = api.eventually(f"user/{username}", lambda b: b.get("username") == username)
    response = api.put(f"user/{username}", make_user(username) | {"firstName": "Ghost"})
    assert response.status_code == 200
    assert response.json()["message"] != str(original["id"])
    assert api.get(f"user/{username}").json()["firstName"] == "Tigran"
