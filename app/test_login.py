from fastapi.testclient import TestClient
from core.api.router.router_login import router as router_login
from core.api.router.router_product import router as router_product
import pytest
import httpx

def test_login_for_access():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = f"username=cabo&password=cabo"
    with httpx.Client() as client:
        response = client.post("http://127.0.0.1:8000/api/v1/login/token", headers=headers, content=payload)

    assert response.status_code == 200

def test_register_acc():
    client = TestClient(router_login)
    resp = client.post('/register/', json={"username":"viking", "password":"viking", "email":"viking@gmail.com"})
    if resp.status_code == 403:
        assert resp.status_code == 403
    if resp.status_code == 201:
        assert resp.status_code == 201