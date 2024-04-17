import uvicorn

from src.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "src.application:app",
        host=settings.server.host,
        log_level=settings.log.level,
        port=settings.server.port,
        reload=True,
    )
