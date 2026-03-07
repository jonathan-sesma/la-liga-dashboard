from fastapi import FastAPI
from app.database import engine, Base
from contextlib import asynccontextmanager
from app.routers import teams

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown logic (optional)

app = FastAPI(
    title="La Liga Statistics API",
    description="Backend API for La Liga Statistics dashboard",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(teams.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "La Liga API is running"}