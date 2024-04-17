import structlog
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import clear_mappers
from starlette.requests import Request
from starlette.responses import Response

from src.core.fastapi.error import init_error_handler
from src.core.fastapi.mapper import start_mapper
from src.core.fastapi.middleware import TokenRefreshMiddleware
from src.core.fastapi.routes import add_routes
from src.dependency.container import Container
from src.logging_custom.costum_logging import configure_logger
from src.modules.user.usecase import router as user_router
from src.modules.vacation.usecase import router as vacation_router
from src.modules.jira_employee.usecase import router as generate_doc_router
from src.modules.user.usecase.get_user import api as get_user_api
from src.modules.user.usecase.login import api as login_user_api
from src.modules.user.usecase.me import api as me_user_api
from src.modules.vacation.usecase.create_vacation import api as create_vacation_api
from src.modules.vacation.usecase.notify_vacation import api as notify_vacation_api
from src.modules.user.usecase.delete_user import api as delete_user_api
from src.modules.user.usecase.register import api as create_user_api
from src.modules.user.usecase.update_user import api as update_user_api
from src.modules.jira_employee.usecase.generate_doc import api as generate_doc_api

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
            get_user_api,
            create_user_api,
            update_user_api,
            delete_user_api,
            login_user_api,
            me_user_api,
            create_vacation_api,
            notify_vacation_api,
            generate_doc_api,
        ]
    )

    application = FastAPI(
        title="Internal Portal API",
        version="0.0.1",
        description="REST API and backend services",
        docs_url="/api/internal_portal/docs",
        openapi_url="/api/internal_portal/openapi.json",
        default_response_class=ORJSONResponse,
        servers=[],
    )
    application.container = container
    db = container.db()

    # logger.info("Add Routes..")

    add_routes(
        [
            user_router,
            vacation_router,
            generate_doc_router,
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
    application.middleware("http")(TokenRefreshMiddleware(application))

    init_error_handler(application, "")

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
