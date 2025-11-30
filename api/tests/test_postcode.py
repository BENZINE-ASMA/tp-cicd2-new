from app import create_app
from fastapi.testclient import TestClient


class DummyES:
    def __init__(self):
        self._ping = True

    def ping(self):
        return self._ping

    def search(self, index, query):
        return {"hits": {"hits": [{"_source": {"id": "72000", "label": "Le Mans"}}]}}


def test_postcode_ok(monkeypatch):
    # patch BEFORE create_app to avoid real connection
    monkeypatch.setattr(
        "app.Elasticsearch", lambda hosts, verify_certs=False: DummyES()
    )
    app = create_app("http://dummy:9200", "addresses")
    client = TestClient(app)
    r = client.get("/postcode/72000")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_health(monkeypatch):
    monkeypatch.setattr(
        "app.Elasticsearch", lambda hosts, verify_certs=False: DummyES()
    )
    app = create_app("http://dummy:9200", "addresses")
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["elastic_ok"] is True
