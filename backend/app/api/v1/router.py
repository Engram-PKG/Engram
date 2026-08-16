from fastapi import APIRouter

from app.api.v1.endpoints import auth, chat, connectors, graph, health, memory

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(connectors.router, prefix="/connectors", tags=["connectors"])
api_router.include_router(memory.router, prefix="/memory", tags=["memory"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(graph.router, prefix="/graph", tags=["graph"])
