from fastapi.testclient import TestClient


def test_work_item_crud(client: TestClient) -> None:
    created = client.post(
        "/work-items",
        json={"title": "Ship tutorial", "description": "Write chapter one"},
    )
    assert created.status_code == 201
    item = created.json()
    assert item["title"] == "Ship tutorial"
    assert item["status"] == "open"

    item_id = item["id"]

    listed = client.get("/work-items")
    assert listed.status_code == 200
    assert [row["id"] for row in listed.json()] == [item_id]

    updated = client.patch(
        f"/work-items/{item_id}",
        json={"status": "in_progress"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "in_progress"

    deleted = client.delete(f"/work-items/{item_id}")
    assert deleted.status_code == 204

    missing = client.get(f"/work-items/{item_id}")
    assert missing.status_code == 404


def test_create_rejects_blank_title(client: TestClient) -> None:
    response = client.post("/work-items", json={"title": ""})

    assert response.status_code == 422
