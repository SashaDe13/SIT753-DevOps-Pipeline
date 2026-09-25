import pytest
import app as app_module

@pytest.fixture()
def client():
    app_module.app.config.update(TESTING=True)
    app_module.tasks.clear()
    app_module.next_id = 1
    with app_module.app.test_client() as client:
        yield client

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200 and r.get_json()["status"] == "ok"

def test_create_and_list(client):
    assert client.post("/tasks", json={"title":"Jenkins demo"}).status_code == 201
    assert len(client.get("/tasks").get_json()) == 1

def test_empty_title(client):
    assert client.post("/tasks", json={"title":" "}).status_code == 400

def test_update(client):
    i = client.post("/tasks", json={"title":"A"}).get_json()["id"]
    r = client.put(f"/tasks/{i}", json={"title":"B","completed":True})
    assert r.status_code == 200 and r.get_json()["completed"] is True

def test_delete(client):
    i = client.post("/tasks", json={"title":"A"}).get_json()["id"]
    assert client.delete(f"/tasks/{i}").status_code == 204

def test_missing_update(client):
    assert client.put("/tasks/999", json={"completed":True}).status_code == 404
