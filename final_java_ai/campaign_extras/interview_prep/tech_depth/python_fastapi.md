# Python + FastAPI + Pydantic + asyncio

## What
Python is the primary language across IA agent service Uber FRM Menu Masters. FastAPI for HTTP APIs. Pydantic for request/response validation. asyncio/Celery for concurrent and background work.

## How used here
- IA: FastAPI hosts LangGraph/MCP agent chat endpoints.
- FRM: FastAPI handlers → services → repositories → SQLAlchemy MySQL.
- Masters: FastAPI microservices strangler replacing PHP.
- Menu: Python Selenium + RAG pipeline services on GCP.

## Tradeoffs
FastAPI speed of delivery and typing vs Go raw throughput. Chose FastAPI for agent/ORM-heavy domains Go for shared compute doing layer.

## Failure modes
- Blocking calls inside async routes
- Over-fat handlers without service layer
- Pydantic model drift vs DB schema

## Likely questions
Why FastAPI vs Flask/Django REST? How do you structure layers? How do you test handlers? When would you move a path to Go?
