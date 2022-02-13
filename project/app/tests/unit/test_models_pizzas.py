# App Imports
from app.models import PizzaModel


def test_created_pizza(created_pizza: PizzaModel) -> None:
    assert created_pizza.name is not None
    assert created_pizza.cheese_type is not None
    assert created_pizza.dough_thickness is not None
    assert created_pizza.secret_ingredient is not None
