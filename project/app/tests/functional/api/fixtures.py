from pytest import fixture

from app.schemas.restaurant import RestaurantCreate
from app.schemas.pizza import PizzaCreate
from app.schemas.person import PersonCreate
from app.models import RestaurantModel
from app.services.age_calculator import calculate_age


@fixture(scope='function')
def test_restaurant_to_create() -> RestaurantCreate:
    return RestaurantCreate(
        name="TestRestaurant",
        address="TestAddress",
    )


@fixture(scope="function")
def test_pizza_to_create(
        created_restaurant: RestaurantModel
) -> PizzaCreate:
    return PizzaCreate(
        restaurant_id=created_restaurant.id,
        name="Margherita",
        cheese_type="Parmesan",
        dough_thickness="thin",
        secret_ingredient="grapefruit seed extract"
    )


@fixture(scope="function")
def test_person_to_create(
) -> PersonCreate:
    return PersonCreate(
        iin="760724300757",
        age=calculate_age(iin="760724300757")
    )
