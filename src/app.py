import os
import sys
import structlog
import asyncio
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes import upload_router, examples_router
from services import periodic_cleanup
from models import Sessions

# Get environment variables once at startup
IS_PRODUCTION = os.getenv("ENV") == "production"
ALLOWED_HOST = os.getenv("ALLOWED_HOST")


# Configure standard logging
logging.basicConfig(level=logging.INFO, format="%(message)s")


# Create file handler
file_handler = RotatingFileHandler(
    "app.log", maxBytes=1 * 1024 * 1024 * 1024, backupCount=5  # 1 GB
)
file_handler.setLevel(logging.INFO)


# Create formatters
json_formatter = structlog.stdlib.ProcessorFormatter(
    processor=structlog.processors.JSONRenderer()
)


# Set formatters
file_handler.setFormatter(json_formatter)


# Add handlers to the root logger
logging.getLogger().addHandler(file_handler)


# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


# Create a base logger
logger = structlog.get_logger()


# Context manager to manage the lifespan of the application
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Initialize the sessions
    app.state.sessions = Sessions()

    # Startup: schedule the periodic cleanup
    cleanup_task = asyncio.create_task(periodic_cleanup(app, logger))

    yield

    # Shutdown: cancel the cleanup task
    cleanup_task.cancel()
    try:
        await cleanup_task
        app.state.sessions.clear()
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)

# Configure CORS
if IS_PRODUCTION:
    allowed_origins = [f"https://{ALLOWED_HOST}/"]
else:
    allowed_origins = ["*"]

# Add CORS middleware with dynamic configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware to limit requests to the allowed host
@app.middleware("http")
async def request_limiter(request: Request, call_next):
    if IS_PRODUCTION and (
        (request.client.host != ALLOWED_HOST) or ("petry-ai" in request.client.host)
    ):
        logger.warning(f"Unauthorized access attempt from {request.client.host}")
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    return await call_next(request)


# Middleware to add the session ID to the request state
@app.middleware("http")
async def add_session_id(request: Request, call_next):
    session_id = request.headers.get("petry-session-id", None)

    if session_id:
        request.state.session_id = session_id
        request.state.logger = logger.bind(session_id=session_id)
    else:
        request.state.session_id = None
        request.state.logger = logger.bind(session_id="No-Session")

    response = await call_next(request)

    if session_id:
        response.headers["petry-session-id"] = session_id

    return response


# Include the routers
app.include_router(examples_router)
app.include_router(upload_router)
