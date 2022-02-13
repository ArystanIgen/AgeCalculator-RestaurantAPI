from fastapi import APIRouter

from app.api.v1.endpoints import person, restaurant, pizza

api_router = APIRouter()

api_router.include_router(person.router, prefix="/people", tags=['People'])
api_router.include_router(restaurant.router, prefix="/restaurants", tags=['Restaurant'])
api_router.include_router(pizza.router, prefix="/restaurants", tags=['Pizza'])
