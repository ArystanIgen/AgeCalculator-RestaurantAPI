from fastapi.testclient import TestClient

from app.schemas.person import PersonCreate
from app.models import PersonModel


def test_person_create(
        client: TestClient,
        test_person_to_create: PersonCreate,
) -> None:
    response = client.post(
        url="/v1/people",
        json=test_person_to_create.dict()
    )
    assert response.status_code == 201

    created_person = response.json()
    assert created_person['iin'] == test_person_to_create.iin
    assert created_person['age'] == test_person_to_create.age


def test_person_create_with_existing_iin(
        client: TestClient,
        test_person_to_create: PersonCreate,
        created_person: PersonModel
) -> None:
    response = client.post(
        url="/v1/people",
        json=test_person_to_create.dict()
    )
    assert response.status_code == 409


def test_person_get_by_iin(
        client: TestClient,
        created_person: PersonModel
) -> None:
    response = client.get(
        url=f"/v1/people/{created_person.iin}"
    )
    assert response.status_code == 200

    received_person = response.json()
    assert received_person['age'] == created_person.age


def test_person_get_by_not_existing_one(
        client: TestClient
) -> None:
    response = client.get(
        url=f"/v1/restaurants/770724300757"
    )
    assert response.status_code == 404
