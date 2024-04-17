import structlog
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import clear_mappers
from starlette.requests import Request
from starlette.responses import Response

from src.core.fastapi.mapper import start_mapper
from src.core.fastapi.routes import add_routes
from src.dependency.container import Container
from src.logging_custom.costum_logging import configure_logger
from src.modules.address.usecase import router as address_router
from src.modules.address.usecase.get_address import api as get_address_api

load_dotenv()
configure_logger()

logger = structlog.stdlib.get_logger("start_logger")

origins = [
    "http://localhost",
    "http://localhost:8080",
]


def create_app(create_db: bool = False) -> FastAPI:
    container = Container()
    container.wire(
        modules=[
            get_address_api,
        ]
    )

    application = FastAPI(
        title="test project API",
        version="0.0.1",
        description="REST API and backend services",
        docs_url="/api/test_project/docs",
        openapi_url="/api/test_project/openapi.json",
        servers=[],
    )
    application.container = container
    db = container.db()

    # logger.info("Add Routes..")

    add_routes(
        [
            address_router,
        ],
        application,
    )

    # logger.info("Add middlewares..")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.on_event("startup")
    async def on_startup():
        await logger.info("Starting Python Micro Framework Data FastAPI Sample App..")

        await db.connect()

        if create_db:
            await db.create_database()

        start_mapper()
        await logger.info("Start_mapper..")

        await logger.info("Started Python Micro Framework Data FastAPI Sample App..")

    @application.on_event("shutdown")
    async def on_shutdown():
        await logger.info("Stopping Python Micro Framework Data FastAPI Sample App..")
        clear_mappers()

        await db.disconnect()

        await logger.info("Stopped Python Micro Framework Data FastAPI Sample App..")

    @application.middleware("http")
    async def logging_middleware(request: Request, call_next) -> Response:
        req_id = request.headers.get("request-id")

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=req_id,
        )

        response: Response = await call_next(request)

        return response

    return application


app = create_app()
