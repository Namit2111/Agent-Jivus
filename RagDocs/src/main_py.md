# FastAPI Application Documentation

This document outlines the structure and functionality of the FastAPI application defined in the provided Python code.

## Overview

The application uses FastAPI for building a RESTful API.  It includes several features:

* **CORS Middleware:** Enables Cross-Origin Resource Sharing, allowing requests from any origin (currently, a wildcard `*` is used; this should be restricted in production).
* **Modular Design:**  The application's logic is divided into separate routers for different functionalities (authentication, post-call processing, integrations, database interactions, pre-call actions, live-call actions, and an AI agent).
* **Versioning:**  Some routes are versioned (v1), suggesting future-proofing and potential for different API versions.
* **Debugging:** The application includes a debugging mechanism using `debugpy`, enabling remote debugging during development.
* **Environment-Specific Configuration:** The application's behavior (e.g., whether to expose documentation) differs based on the environment variable `config["ENV"]`.


## Dependencies

The application relies on the following libraries:

* `fastapi`
* `fastapi.middleware.cors`
* `debugpy`
* Custom modules:
    * `src.config`: Contains application configuration, including environment variables.
    * `src.auth`: Authentication-related routes (`auth_router`).
    * `src.post_call`: Post-call processing routes (`post_call_router`).
    * `src.integrations`: Integration-related routes (`integrations_router`).
    * `src.db`: Database interaction routes (`db_router_v1`).
    * `src.pre_call`: Pre-call processing routes (`pre_call_router_v1`).
    * `src.live_call`: Live-call processing routes (`live_call_router_v1`).
    * `src.ai_agent`: AI agent routes (`ai_agent_router`).

## Code Structure

The application's structure is modular, with each functionality encapsulated in a separate router:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# ... imports from src modules ...
import debugpy

# Debugging setup
debugpy.listen(("0.0.0.0", 5678))
# ... (debugpy wait) ...

# Conditional app initialization based on environment
if config["ENV"] == "dev":
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)

# CORS middleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)

# Route inclusion
# v0 routes
app.include_router(post_call_router)
app.include_router(integrations_router)
app.include_router(ai_agent_router)

# v1 routes
app.include_router(db_router_v1)
app.include_router(pre_call_router_v1)
app.include_router(live_call_router_v1)
```

## TODOs

The code contains the following TODOs:

* **Stricter CORS Origins:** The `allow_origins=["*"]` in the CORS middleware should be replaced with a more restrictive list of allowed origins for production environments.
* **Refactor post-call router:**  The `post_call_router` needs refactoring.


##  Further Development

To fully understand the application's functionality, it's necessary to examine the code within each of the `src` modules.  The specific API endpoints and their functionalities are not described here as the code for these routes is not provided.  Further documentation should detail the individual endpoints and their parameters and responses.
