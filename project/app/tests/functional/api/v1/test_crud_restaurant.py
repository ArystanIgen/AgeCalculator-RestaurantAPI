from random import randint

from fastapi.testclient import TestClient

from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from app.models import RestaurantModel


def test_restaurant_create(
        client: TestClient,
        test_restaurant_to_create: RestaurantCreate,
) -> None:
    response = client.post(
        url="/v1/restaurants",
        json=test_restaurant_to_create.dict()
    )
    assert response.status_code == 201

    created_restaurant = response.json()
    assert created_restaurant['name'] == test_restaurant_to_create.name
    assert created_restaurant['address'] == test_restaurant_to_create.address


def test_restaurant_create_with_existing_name(
        client: TestClient,
        test_restaurant_to_create: RestaurantCreate,
        created_restaurant: RestaurantModel
) -> None:
    response = client.post(
        url="/v1/restaurants",
        json=test_restaurant_to_create.dict()
    )
    assert response.status_code == 409


def test_restaurant_create_with_not_enough_data(
        client: TestClient,
        test_restaurant_to_create: RestaurantCreate
) -> None:
    del test_restaurant_to_create.address
    response = client.post(
        url="/v1/restaurants",
        json=test_restaurant_to_create.dict()
    )
    assert response.status_code == 400


def test_restaurants_get(
        client: TestClient,
) -> None:
    response = client.get(
        url="/v1/restaurants"
    )
    assert response.status_code == 200


def test_restaurant_get_by_id(
        client: TestClient,
        created_restaurant: RestaurantModel
) -> None:
    response = client.get(
        url=f"/v1/restaurants/{created_restaurant.uuid}"
    )
    assert response.status_code == 200

    received_restaurant = response.json()
    assert received_restaurant['name'] == created_restaurant.name
    assert received_restaurant['address'] == created_restaurant.address


def test_restaurant_get_by_not_existing_one(
        client: TestClient
) -> None:
    invalid_code = randint(100, 999)
    response = client.get(
        url=f"/v1/restaurants/{invalid_code}"
    )
    assert response.status_code == 404


def test_restaurant_update(
        client: TestClient,
        created_restaurant: RestaurantModel
) -> None:
    updated_restaurant = RestaurantUpdate(name=str(randint(1111, 9999)))
    response = client.patch(
        url=f"/v1/restaurants/{created_restaurant.uuid}",
        json=updated_restaurant.dict()
    )
    assert response.status_code == 200


def test_restaurant_update_by_not_existing_one(
        client: TestClient,
) -> None:
    updated_restaurant = RestaurantUpdate(name=str(randint(1111, 9999)))
    response = client.patch(
        url="/v1/restaurants/111111",
        json=updated_restaurant.dict()
    )
    assert response.status_code == 404


def test_restaurant_delete(
        client: TestClient,
        created_restaurant: RestaurantModel
) -> None:
    response = client.delete(
        url=f"/v1/restaurants/{created_restaurant.uuid}",
    )
    assert response.status_code == 204


def test_restaurant_delete_not_existing_one(
        client: TestClient,
) -> None:
    response = client.delete(
        url=f"/v1/restaurants/111111",
    )
    assert response.status_code == 404
