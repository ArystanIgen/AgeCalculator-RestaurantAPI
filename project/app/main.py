import uvicorn  # type: ignore
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import CONFIG

from starlette import status

main_app = FastAPI(
    title=CONFIG.api.title,
    debug=CONFIG.api.debug,
    version=CONFIG.api.version,
    openapi_url='/openapi.json'
)


async def validation_error_handler(_: Request) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'code': "InvalidRequest",
        }
    )


main_app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=CONFIG.api.allowed_hosts or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
main_app.add_middleware(GZipMiddleware, minimum_size=1000)
main_app.add_exception_handler(
    RequestValidationError,
    validation_error_handler,
)
main_app.add_exception_handler(
    Exception,
    validation_error_handler,
)
main_app.include_router(prefix=CONFIG.api.prefix, router=api_router)

if __name__ == "__main__":
    uvicorn.run(main_app, host="0.0.0.0", port=8000)
