from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import config

from src.auth import router as auth_router

from src.post_call.router import router as post_call_router
from src.integrations.router import router as integrations_router

from src.db.router import router as db_router_v1
from src.pre_call.router_v1 import router as pre_call_router_v1
from src.live_call.router_v1 import router as live_call_router_v1
from src.ai_agent.router import aiAgent as ai_agent_router
import debugpy


# Start debugpy
debugpy.listen(("0.0.0.0", 5678))
print("⏳ Waiting for debugger attach...")
debugpy.wait_for_client()
print("🎉 Debugger attached")

if config["ENV"] == "dev":
    app = FastAPI()
    app.include_router(auth_router)
else:
    app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Stricter origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# v0 routes
app.include_router(post_call_router)  # TODO: Refactor
app.include_router(integrations_router)
app.include_router(ai_agent_router)

# v1 routes
app.include_router(db_router_v1)
app.include_router(pre_call_router_v1)
app.include_router(live_call_router_v1)

