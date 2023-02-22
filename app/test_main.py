from fastapi.testclient import TestClient
from core.api.router.router_product import router as router_product
from secrets import token_hex
import random

client = TestClient(router_product)

code = token_hex(5)
cost = random.randint(1, 1000)
sale = random.randint(1000, 15000)
stock = random.randint(1, 150)
prendas = ["Polera", "Short", "Pantalon", "Zapato", "Sombrero"]
marca = ["Adidas", "Nike", "Umbro", "Puma", "Rebook"]
years = random.randint(2020, 2024)

headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjYWJvIiwiaXNfYWRtaW4iOnRydWUsImV4cF9kYXRlIjoiMjAyMy0wMi0yNiIsImFwaV9rZXkiOiJ2dWYyNkNZZTZqSnNXcXNsX3NsRER3IiwiaXNfcHJlbWl1bSI6dHJ1ZSwiZXhwIjoxNjc3NTUwMDIzfQ.q_pEJnzmE0HgUQJtmJV2T1i0nsANGaF8wonCqCDwLY8",
        "Cookie": 'access_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjYWJvIiwiaXNfYWRtaW4iOnRydWUsImV4cF9kYXRlIjoiMjAyMy0wMi0yNiIsImFwaV9rZXkiOiJ2dWYyNkNZZTZqSnNXcXNsX3NsRER3IiwiaXNfcHJlbWl1bSI6dHJ1ZSwiZXhwIjoxNjc3NTUwNjEwfQ.Q1Qv2F8RUbhJBzSpke85hiG6eXU12xaFYXDah-M7OH0"',
    }
def test_add_product():
    
    resp = client.post(
        "/add",
        json={
            "code": f"{code}",
            "description": f"Genial {random.choice(prendas)} verano {years}",
            "name": f"{random.choice(prendas)} {random.choice(marca)}",
            "sale": sale,
            "cost": cost,
            "stock": stock,
            "brand": random.choice(marca),
            "images": ["www.image_1.cl", "www.image_2.cl"],
        }, headers=headers
    )
    assert resp.status_code == 201


def test_add_product_403():
    resp = client.post(
        "/add",
        json={
            "code": "4352cb7ae6",
            "description": "Una genial polera verano 2023",
            "name": "Polera Adidas",
            "sale": 1500,
            "cost": 570,
            "stock": 50,
            "brand": "Adidas",
            "images": ["www.image_1.cl", "www.image_2.cl"],
        }, headers=headers
    )
    assert resp.status_code == 403


def test_list_products():
    resp = client.get("/products_free")
    assert resp.status_code == 200


def test_retrive_product():
    """
    /products/code_product
    """
    resp = client.get("/product/26b1347bf1")
    assert resp.status_code == 200
    assert isinstance(resp.json(), dict)


def test_retrive_product_404():
    resp = client.get("/product/a1da26b1347bf1sdas")
    assert resp.status_code == 404


def test_list_products_premium():
    resp = client.get("/products_premium", headers=headers)
    assert resp.status_code == 200


def test_remove_product():
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjYWJvIiwiaXNfYWRtaW4iOnRydWUsImV4cF9kYXRlIjoiMjAyMy0wMi0yNiIsImFwaV9rZXkiOiJ2dWYyNkNZZTZqSnNXcXNsX3NsRER3IiwiaXNfcHJlbWl1bSI6dHJ1ZSwiZXhwIjoxNjc3NTUwMDIzfQ.q_pEJnzmE0HgUQJtmJV2T1i0nsANGaF8wonCqCDwLY8",
        "Cookie": 'access_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjYWJvIiwiaXNfYWRtaW4iOnRydWUsImV4cF9kYXRlIjoiMjAyMy0wMi0yNiIsImFwaV9rZXkiOiJ2dWYyNkNZZTZqSnNXcXNsX3NsRER3IiwiaXNfcHJlbWl1bSI6dHJ1ZSwiZXhwIjoxNjc3NTUwNjEwfQ.Q1Qv2F8RUbhJBzSpke85hiG6eXU12xaFYXDah-M7OH0"',
    }

    resp = client.delete("/delete/63f2e69ac705d8c05e6e96", headers=headers)

    if resp.status_code == 200:
        assert resp.json() == {"msg": "Product Removed"}
    elif resp.status_code == 404:
        assert resp.json() == {"msg": "product does not exist"}
    elif resp.status_code == 403:
        assert resp.json() == {"msg": "You don't have the permissions for this action"}


def test_pagination():
    resp = client.get("/pagination?skip=1&limit=10")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_patch_product():
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjYWJvIiwiaXNfYWRtaW4iOnRydWUsImV4cF9kYXRlIjoiMjAyMy0wMi0yNiIsImFwaV9rZXkiOiJ2dWYyNkNZZTZqSnNXcXNsX3NsRER3IiwiaXNfcHJlbWl1bSI6dHJ1ZSwiZXhwIjoxNjc3NTUwMDIzfQ.q_pEJnzmE0HgUQJtmJV2T1i0nsANGaF8wonCqCDwLY8",
        "Cookie": 'access_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjYWJvIiwiaXNfYWRtaW4iOnRydWUsImV4cF9kYXRlIjoiMjAyMy0wMi0yNiIsImFwaV9rZXkiOiJ2dWYyNkNZZTZqSnNXcXNsX3NsRER3IiwiaXNfcHJlbWl1bSI6dHJ1ZSwiZXhwIjoxNjc3NTUwNjEwfQ.Q1Qv2F8RUbhJBzSpke85hiG6eXU12xaFYXDah-M7OH0"',
    }
    resp = client.patch(
        "/update/63f2ba6f1c8ae34c3eb9fe07",
        json={
            "description": f"Genial {random.choice(prendas)} verano {years}",
            "name": f"{random.choice(prendas)} {random.choice(marca)}",
            "sale": sale,
            "cost": cost,
            "stock": stock,
            "brand": random.choice(marca),
            "images": ["www.image_1.cl", "www.image_2.cl"],
        }, headers=headers
    )
    if resp.status_code == 200:
        assert resp.json() == {"msg":"Modified product"}
    elif resp.status_code == 404:
        assert resp.json() == {"msg":"Producto not found"}
    elif resp.status_code == 403:
        assert resp.json() == {"msg":"You don't have the permissions for this action"}


