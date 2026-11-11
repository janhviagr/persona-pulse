from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import personas, products, reports, simulations
from backend.app.core.config import settings
from backend.app.database.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Persona Pulse API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in (products.router, personas.router, simulations.router, reports.router):
    app.include_router(r, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
