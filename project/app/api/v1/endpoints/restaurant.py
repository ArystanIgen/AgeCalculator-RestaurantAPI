from typing import List, Optional
from fastapi import Query, Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from app.schemas.restaurant import RestaurantUpdate, RestaurantCreate, RestaurantOut, RestaurantIn
from app.api.deps import get_session, get_restaurant_repo
from app.models import RestaurantModel
from app.repositories import RestaurantRepository

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=RestaurantOut,
    response_description='Restaurant was created'
)
def create_restaurant(
        restaurant_in: RestaurantIn,
        restaurant_repo: RestaurantRepository = Depends(get_restaurant_repo),
        session: Session = Depends(get_session)
) -> Optional[RestaurantModel]:
    fetched_restaurant: Optional[RestaurantModel] = restaurant_repo.get_by_name(
        session=session,
        name=restaurant_in.name
    )
    if fetched_restaurant:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A restaurant with the same name already exists"
        )
    return restaurant_repo.create(
        session=session,
        obj_in=RestaurantCreate(
            name=restaurant_in.name,
            address=restaurant_in.address
        )
    )


@router.get(
    "/{restaurant_id}",
    status_code=status.HTTP_200_OK,
    response_model=RestaurantOut,
    response_description='Restaurant info'
)
def get_restaurant(
        restaurant_id: str,
        restaurant_repo: RestaurantRepository = Depends(get_restaurant_repo),
        session: Session = Depends(get_session)
) -> Optional[RestaurantModel]:
    fetched_restaurant: Optional[RestaurantModel] = restaurant_repo.get_by_uuid(
        session=session,
        uuid=restaurant_id,
    )
    if fetched_restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    return fetched_restaurant


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[RestaurantOut],
    response_description='Restaurants info'
)
def get_restaurants(
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=0, le=50),
        restaurant_repo: RestaurantRepository = Depends(get_restaurant_repo),
        session: Session = Depends(get_session)
) -> List[RestaurantModel]:
    return restaurant_repo.get_multi(session=session, skip=offset, limit=limit)


@router.delete(
    '/{restaurant_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_description='Restaurant was removed'
)
def delete_restaurant(
        restaurant_id: str,
        session: Session = Depends(get_session),
        restaurant_repo: RestaurantRepository = Depends(get_restaurant_repo),
) -> None:
    fetched_restaurant: Optional[RestaurantModel] = restaurant_repo.get_by_uuid(
        session=session,
        uuid=restaurant_id,
    )
    if fetched_restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    restaurant_repo.remove(session=session, id_=fetched_restaurant.id)


@router.patch(
    "/{restaurant_id}",
    response_model=RestaurantOut,
    status_code=status.HTTP_200_OK,
    response_description='Restaurant information has been updated',
)
def update_restaurant(
        restaurant_update: RestaurantUpdate,
        restaurant_id: str,
        session: Session = Depends(get_session),
        restaurant_repo: RestaurantRepository = Depends(get_restaurant_repo),
) -> Optional[RestaurantModel]:
    fetched_restaurant: Optional[RestaurantModel] = restaurant_repo.get_by_uuid(
        session=session,
        uuid=restaurant_id,
    )
    if fetched_restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    update_data = restaurant_update.dict(exclude_unset=True)
    for var, value in update_data.items():
        setattr(fetched_restaurant, var, value) if value else None
    restaurant_repo.update(session=session, instance=fetched_restaurant)
    return fetched_restaurant
