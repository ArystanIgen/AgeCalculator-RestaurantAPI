# App Imports
from app.models import RestaurantModel


def test_created_restaurant(created_restaurant: RestaurantModel) -> None:
    assert created_restaurant.name is not None
    assert created_restaurant.address is not None
