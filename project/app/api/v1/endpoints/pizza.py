from typing import List, Optional

from fastapi import Query, Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app.schemas.pizza import PizzaCreate, PizzaIn, PizzaOut, PizzaUpdate
from app.api.deps import get_session, get_restaurant_repo, get_pizza_repo
from app.models import PizzaModel, RestaurantModel
from app.repositories import RestaurantRepository, PizzaRepository

router = APIRouter()


def check_restaurant_existing(
        session: Session,
        restaurant_repo: RestaurantRepository,
        restaurant_id: str
) -> RestaurantModel:
    restaurant: Optional[RestaurantModel] = restaurant_repo.get_by_uuid(
        session=session,
        uuid=restaurant_id,
    )
    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    return restaurant


@router.post(
    "/{restaurant_id}/pizzas",
    status_code=status.HTTP_201_CREATED,
    response_model=PizzaOut,
    response_description='Pizza was created'
)
def create_pizza(
        restaurant_id: str,
        pizza_in: PizzaIn,
        pizza_repo: PizzaRepository = Depends(get_pizza_repo),
        restaurant_repo: RestaurantRepository = Depends(get_restaurant_repo),
        session: Session = Depends(get_session)
) -> Optional[PizzaModel]:
    fetched_restaurant: RestaurantModel = check_restaurant_existing(
        session=session,
        restaurant_repo=restaurant_repo,
        restaurant_id=restaurant_id
    )
    fetched_pizza: Optional[PizzaModel] = pizza_repo.get_by_name(
        session=session,
        name=pizza_in.name,
    )
    if fetched_pizza:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A Pizza with the same name already exists"
        )
    return pizza_repo.create(
        session=session,
        obj_in=PizzaCreate(
            restaurant_id=fetched_restaurant.id,
            name=pizza_in.name,
            cheese_type=pizza_in.cheese_type,
            dough_thickness=pizza_in.dough_thickness,
            secret_ingredient=pizza_in.secret_ingredient
        )
    )


@router.get(
    "/{restaurant_id}/pizzas",
    status_code=status.HTTP_200_OK,
    response_model=List[PizzaOut],
    response_description='Pizza info'
)
def get_pizzas(
        restaurant_id: str,
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=0, le=50),
        pizza_repo: PizzaRepository = Depends(get_pizza_repo),
        restaurant_repo: RestaurantRepository = Depends(get_restaurant_repo),
        session: Session = Depends(get_session)
) -> List[PizzaModel]:
    fetched_restaurant: RestaurantModel = check_restaurant_existing(
        session=session,
        restaurant_repo=restaurant_repo,
        restaurant_id=restaurant_id
    )
    return pizza_repo.get_list_of_pizzas(
        session=session,
        restaurant_id=fetched_restaurant.id,
        skip=offset,
        limit=limit
    )


@router.get(
    "/{restaurant_id}/pizzas/{pizza_id}",
    status_code=status.HTTP_200_OK,
    response_model=PizzaOut,
    response_description='Pizza info'
)
def get_pizza(
        restaurant_id: str,
        pizza_id: str,
        pizza_repo: PizzaRepository = Depends(get_pizza_repo),
        restaurant_repo: RestaurantRepository = Depends(get_restaurant_repo),
        session: Session = Depends(get_session),

) -> PizzaModel:
    fetched_restaurant: RestaurantModel = check_restaurant_existing(
        session=session,
        restaurant_repo=restaurant_repo,
        restaurant_id=restaurant_id
    )
    fetched_pizza: Optional[PizzaModel] = pizza_repo.get_by_uuid(
        session=session,
        uuid=pizza_id,
        restaurant_id=fetched_restaurant.id
    )
    if fetched_pizza is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza not found"
        )
    return fetched_pizza


@router.delete(
    "/{restaurant_id}/pizzas/{pizza_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description='Pizza was deleted'
)
def delete_pizza(
        restaurant_id: str,
        pizza_id: str,
        pizza_repo: PizzaRepository = Depends(get_pizza_repo),
        restaurant_repo: RestaurantRepository = Depends(get_restaurant_repo),
        session: Session = Depends(get_session),
) -> None:
    fetched_restaurant: RestaurantModel = check_restaurant_existing(
        session=session,
        restaurant_repo=restaurant_repo,
        restaurant_id=restaurant_id
    )
    fetched_pizza: Optional[PizzaModel] = pizza_repo.get_by_uuid(
        session=session,
        uuid=pizza_id,
        restaurant_id=fetched_restaurant.id
    )
    if fetched_pizza is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza not found"
        )
    pizza_repo.remove(session=session, id_=fetched_pizza.id)


@router.patch(
    "/{restaurant_id}/pizzas/{pizza_id}",
    status_code=status.HTTP_200_OK,
    response_description='Pizza has been updated'
)
def update_pizza(
        restaurant_id: str,
        pizza_id: str,
        pizza_update: PizzaUpdate,
        session: Session = Depends(get_session),
        pizza_repo: PizzaRepository = Depends(get_pizza_repo),
        restaurant_repo: RestaurantRepository = Depends(get_restaurant_repo),

) -> PizzaModel:
    fetched_restaurant: RestaurantModel = check_restaurant_existing(
        session=session,
        restaurant_repo=restaurant_repo,
        restaurant_id=restaurant_id
    )
    fetched_pizza: Optional[PizzaModel] = pizza_repo.get_by_uuid(
        session=session,
        uuid=pizza_id,
        restaurant_id=fetched_restaurant.id
    )
    if fetched_pizza is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza not found"
        )
    update_data = pizza_update.dict(exclude_unset=True)
    for var, value in update_data.items():
        setattr(fetched_pizza, var, value) if value else None
    pizza_repo.update(session=session, instance=fetched_pizza)
    return fetched_pizza
