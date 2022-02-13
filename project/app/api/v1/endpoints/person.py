# Standard Library
from typing import Optional
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from app.schemas import PersonOut, PersonCreate, PersonIn
from app.api.deps import get_session, get_person_repo
from app.models.person import PersonModel
from app.repositories.person import PersonRepository
from app.services.age_calculator import calculate_age

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PersonOut,
    response_description='Person was created'
)
def create_people(
        person_in: PersonIn,
        person_repo: PersonRepository = Depends(get_person_repo),
        session: Session = Depends(get_session)
) -> Optional[PersonModel]:
    fetched_person: Optional[PersonModel] = person_repo.get_by_iin(
        session=session,
        iin=person_in.iin
    )
    if fetched_person:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A person with the same IIN already exists"
        )
    return person_repo.create(
        session=session,
        obj_in=PersonCreate(
            iin=person_in.iin,
            age=calculate_age(
                iin=person_in.iin
            )
        )
    )


@router.get(
    "/{iin}",
    status_code=status.HTTP_200_OK,
    response_model=PersonOut,
    response_description='Age info'
)
def get_age(
        iin: str,
        person_repo: PersonRepository = Depends(get_person_repo),
        session: Session = Depends(get_session),
) -> Optional[PersonModel]:
    fetched_person: Optional[PersonModel] = person_repo.get_by_iin(
        session=session,
        iin=iin
    )
    if fetched_person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IIN not found"
        )
    return fetched_person
