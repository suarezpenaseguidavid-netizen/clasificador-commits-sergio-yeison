from fastapi.testclient import TestClient
from app.main import app, clasificar_eco

cliente = TestClient(app)


def test_health():
    r = cliente.get("/health")
    assert r.status_code == 200
    assert r.json()["estado"] == "ok"


def test_clasificar_eco():
    r = cliente.post(
        "/clasificar",
        json={"texto": "fix: corrige error en login", "motor": "eco"},
    )
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["tipo"] == "fix"
    assert cuerpo["latencia_ms"] >= 0


def test_motor_invalido():
    r = cliente.post(
        "/clasificar",
        json={"texto": "mensaje cualquiera", "motor": "inexistente"},
    )
    assert r.status_code == 400


def test_reglas_eco():
    assert clasificar_eco("agrega el endpoint de salud") == "feat"
    assert clasificar_eco("actualiza el readme") == "docs"
    assert clasificar_eco("agrega pruebas unitarias") == "test"


def test_inferencias_devuelve_lista():
    r = cliente.get("/inferencias?limite=5")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
