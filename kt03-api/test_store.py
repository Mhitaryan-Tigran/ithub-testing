def make_order(order_id, quantity=2):
    return {"id": order_id, "petId": 1, "quantity": quantity, "shipDate": "2026-10-04T12:00:00.000Z", "status": "placed", "complete": False}


def test_inventory(api):
    response = api.get("store/inventory")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert all(isinstance(v, int) for v in body.values())


def test_place_order(api, order_id):
    response = api.post("store/order", make_order(order_id, 3))
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == order_id
    assert body["quantity"] == 3
    assert body["status"] == "placed"


def test_get_order(api, order_id):
    api.post("store/order", make_order(order_id))
    body = api.eventually(f"store/order/{order_id}", lambda b: b.get("id") == order_id)
    assert body["id"] == order_id


def test_delete_order(api, order_id):
    api.post("store/order", make_order(order_id))
    assert api.delete(f"store/order/{order_id}").status_code == 200
    assert api.get(f"store/order/{order_id}", expected_status=404).status_code == 404
