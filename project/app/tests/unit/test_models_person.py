# App Imports
from app.models import PersonModel


def test_created_person(created_person: PersonModel) -> None:
    assert created_person.iin is not None
    assert created_person.age is not None
