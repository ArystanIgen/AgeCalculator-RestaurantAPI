from pytest import fixture
from sqlalchemy.orm import Session

from app.models import RestaurantModel, PizzaModel, PersonModel
from app.schemas.pizza import PizzaCreate
from app.schemas.restaurant import RestaurantCreate
from app.schemas.person import PersonCreate
from app.services.age_calculator import calculate_age
from app.api.deps import get_restaurant_repo, get_pizza_repo, get_person_repo


@fixture(scope='function')
def created_restaurant(session: Session) -> RestaurantModel:
    restaurant_to_create = RestaurantCreate(
        name="TestRestaurant",
        address="TestAddress",
    )
    restaurant_repo = get_restaurant_repo()
    fetched_restaurant = restaurant_repo.create(
        session=session,
        obj_in=restaurant_to_create
    )
    yield fetched_restaurant
    restaurant_repo.remove(session=session, id_=fetched_restaurant.id)


@fixture(scope='function')
def created_person(session: Session) -> PersonModel:
    person_to_create = PersonCreate(
        iin="760724300757",
        age=calculate_age(iin="760724300757")
    )
    person_repo = get_person_repo()
    fetched_person = person_repo.create(
        session=session,
        obj_in=person_to_create
    )
    yield fetched_person
    person_repo.remove(session=session, id_=fetched_person.id)


@fixture(scope='function')
def created_pizza(session: Session, created_restaurant: RestaurantModel) -> PizzaModel:
    pizza_to_create = PizzaCreate(
        restaurant_id=created_restaurant.id,
        name="Margherita",
        cheese_type="Parmesan",
        dough_thickness="thin",
        secret_ingredient="grapefruit seed extract"
    )
    pizza_repo = get_pizza_repo()
    fetched_pizza = pizza_repo.create(
        session=session,
        obj_in=pizza_to_create
    )
    yield fetched_pizza
    pizza_repo.remove(session=session, id_=fetched_pizza.id)
