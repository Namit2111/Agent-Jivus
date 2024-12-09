# Python FastAPI Application Documentation

This document describes a FastAPI application.

## File Overview: `main.py`

This file initializes and configures a FastAPI application, including routing, middleware, and debugging capabilities.

## Imports

The following libraries and modules are imported:

* `fastapi`: The core FastAPI library for building APIs.
* `fastapi.middleware.cors`: Middleware for handling Cross-Origin Resource Sharing (CORS).
* `src.config`:  A module containing application configuration (likely environment variables).
* `src.auth.router`:  Router for authentication-related endpoints.
* `src.post_call.router`: Router for post-call related endpoints.
* `src.integrations.router`: Router for integration endpoints.
* `src.db.router`: Router for database-related endpoints (v1).
* `src.pre_call.router_v1`: Router for pre-call endpoints (v1).
* `src.live_call.router_v1`: Router for live-call endpoints (v1).
* `src.ai_agent.router`: Router for AI agent endpoints.
* `debugpy`: Library for debugging the application.

## Debugging

The application uses `debugpy` for debugging. It listens on `0.0.0.0:5678` for debugger connections.  This allows attaching a debugger (e.g., VS Code) for development purposes.


## Application Initialization

The application is initialized differently depending on the environment variable `config["ENV"]`:

* **Development (`config["ENV"] == "dev"`):** A standard `FastAPI` application is created with full documentation enabled.
* **Production (otherwise):** A `FastAPI` application is created with documentation disabled (`docs_url=None`, `redoc_url=None`).

## CORS Middleware

CORS middleware is added to allow requests from any origin (`allow_origins=["*"]`).  **Note:** This is a placeholder and should be replaced with stricter origin restrictions in a production environment.


## Routing

The application includes the following routers:

* **Version 0 (v0) routes:**
    * `post_call_router`:  (Marked for refactoring)
    * `integrations_router`
    * `ai_agent_router`

* **Version 1 (v1) routes:**
    * `db_router_v1`
    * `pre_call_router_v1`
    * `live_call_router_v1`

Each router likely contains specific API endpoints defined in their respective files.


## TODO Items

The code includes the following TODO items:

* **Stricter CORS origins:** Replace `allow_origins=["*"]` with specific allowed origins.
* **Refactor `post_call_router`:**  The `post_call_router` is marked for refactoring.


This documentation provides a high-level overview of the `main.py` file.  More detailed information would require examining the contents of the imported modules and routers.
