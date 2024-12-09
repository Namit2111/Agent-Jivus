# This file is for running and testin the app locally easily should not be pushed out of ai-agent branch

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import debugpy

# Importing configuration and routers
from src.config import config
from src.auth import router as auth_router
from src.post_call.router import router as post_call_router
from src.integrations.router import router as integrations_router
from src.db.router import router as db_router_v1
from src.pre_call.router_v1 import router as pre_call_router_v1
from src.live_call.router_v1 import router as live_call_router_v1
from src.ai_agent.router import aiAgent as ai_agent_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI app instance.
    """
    if config["ENV"] == "dev":
        app = FastAPI()
        app.include_router(auth_router)
    else:
        app = FastAPI(docs_url=None, redoc_url=None)  # Disable docs in non-dev environments

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Consider stricter CORS origins in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routes
    app.include_router(post_call_router)
    app.include_router(integrations_router)
    app.include_router(ai_agent_router)

    # Version 1 routes
    app.include_router(db_router_v1)
    app.include_router(pre_call_router_v1)
    app.include_router(live_call_router_v1)

    return app


def start_debugger():
    """
    Starts the debugpy debugger to allow for remote debugging.
    """
    debugpy.listen(("0.0.0.0", 5678))
    print("⏳ Waiting for debugger attach...")
    debugpy.wait_for_client()  # Block execution until debugger is attached
    print("🎉 Debugger attached")


# Expose the app for external usage
app = create_app()
