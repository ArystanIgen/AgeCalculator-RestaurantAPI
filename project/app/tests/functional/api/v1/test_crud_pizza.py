from random import randint

from fastapi.testclient import TestClient

from app.models import RestaurantModel, PizzaModel
from app.schemas.pizza import PizzaCreate, PizzaUpdate


def test_pizza_create(
        client: TestClient,
        created_restaurant: RestaurantModel,
        test_pizza_to_create: PizzaCreate,
) -> None:
    response = client.post(
        url=f"/v1/restaurants/{created_restaurant.uuid}/pizzas",
        json=test_pizza_to_create.dict(),
    )
    assert response.status_code == 201  # pragma: no cover


def test_pizza_create_with_not_existing_restaurant(
        client: TestClient,
        test_pizza_to_create: PizzaCreate,
) -> None:
    response = client.post(
        "/v1/restaurants/121212/pizzas",
        json=test_pizza_to_create.dict(),
    )
    assert response.status_code == 404  # pragma: no cover


def test_pizza_create_that_already_exists(
        client: TestClient,
        created_restaurant: RestaurantModel,
        created_pizza: PizzaModel,
        test_pizza_to_create: PizzaCreate,
) -> None:
    response = client.post(
        f"/v1/restaurants/{created_restaurant.uuid}/pizzas",
        json=test_pizza_to_create.dict(),
    )
    assert response.status_code == 409  # pragma: no cover


def test_pizza_create_with_invalid_input(
        client: TestClient,
        created_restaurant: RestaurantModel,
) -> None:
    response = client.post(
        f"/v1/restaurants/{created_restaurant.uuid}/pizzas",
        json={"name": "516789"},
    )
    assert response.status_code == 400


def test_pizza_create_with_not_enough_data(
        client: TestClient,
        created_restaurant: RestaurantModel,
        test_pizza_to_create: PizzaCreate,
) -> None:
    del test_pizza_to_create.name
    response = client.post(
        f"/v1/restaurants/{created_restaurant.uuid}/pizzas",
        json=test_pizza_to_create.dict()
    )
    assert response.status_code == 400


def test_pizzas_get(
        client: TestClient,
        created_restaurant: RestaurantModel,
) -> None:
    response = client.get(
        url=f"/v1/restaurants/{created_restaurant.uuid}/pizzas"
    )
    assert response.status_code == 200


def test_pizzas_get_with_not_existing_restaurant(
        client: TestClient
) -> None:
    response = client.get(
        url="/v1/restaurants/11111/pizzas"
    )
    assert response.status_code == 404


def test_pizza_get_by_uuid(
        client: TestClient,
        created_restaurant: RestaurantModel,
        created_pizza: PizzaModel
) -> None:
    response = client.get(
        url=f"/v1/restaurants/{created_restaurant.uuid}/pizzas/{created_pizza.uuid}"
    )
    assert response.status_code == 200


def test_pizza_get_by_invalid_uuid(
        client: TestClient,
        created_restaurant: RestaurantModel,
) -> None:
    response = client.get(
        url=f"/v1/restaurants/{created_restaurant.uuid}/pizzas/11111"
    )
    assert response.status_code == 404


def test_pizza_get_by_not_existing_restaurant(
        client: TestClient
) -> None:
    response = client.get(
        url=f"/v1/restaurants/12121212/pizzas/11111"
    )
    assert response.status_code == 404


def test_pizza_update(
        client: TestClient,
        created_restaurant: RestaurantModel,
        created_pizza: PizzaModel
) -> None:
    updated_pizza = PizzaUpdate(cheese_type=str(randint(11111, 99999)))
    response = client.patch(
        url=f"/v1/restaurants/{created_restaurant.uuid}/pizzas/{created_pizza.uuid}",
        json=updated_pizza.dict()
    )
    assert response.status_code == 200


def test_pizza_update_with_not_existing_restaurant(
        client: TestClient,
        created_pizza: PizzaModel
) -> None:
    updated_pizza = PizzaUpdate(cheese_type=str(randint(11111, 99999)))
    response = client.patch(
        url=f"/v1/restaurants/111111/pizzas/{created_pizza.uuid}",
        json=updated_pizza.dict()
    )
    assert response.status_code == 404


def test_pizza_update_by_invalid_uuid(
        client: TestClient,
        created_pizza: PizzaModel,
        created_restaurant: RestaurantModel
) -> None:
    updated_pizza = PizzaUpdate(cheese_type=str(randint(11111, 99999)))
    response = client.patch(
        url=f"/v1/restaurants/{created_restaurant.uuid}/pizzas/1111111111",
        json=updated_pizza.dict()
    )
    assert response.status_code == 404


def test_pizza_delete(
        client: TestClient,
        created_pizza: PizzaModel,
        created_restaurant: RestaurantModel
) -> None:
    response = client.delete(
        url=f"/v1/restaurants/{created_restaurant.uuid}/pizzas/{created_pizza.uuid}",
    )
    assert response.status_code == 204


def test_pizza_delete_by_invalid_uuid(
        client: TestClient,
        created_restaurant: RestaurantModel
) -> None:
    response = client.delete(
        url=f"/v1/restaurants/{created_restaurant.uuid}/pizzas/121212"
    )
    assert response.status_code == 404


def test_pizza_delete_with_not_existing_restaurant(
        client: TestClient
) -> None:
    response = client.delete(
        url=f"/v1/restaurants/111111/pizzas/1111111"
    )
    assert response.status_code == 404