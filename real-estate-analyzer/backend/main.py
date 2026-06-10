from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth_routes import router as auth_router
from api.routes import router as analysis_router
from db.database import Base, engine

app = FastAPI(title="Autonomous Real Estate Investment Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(analysis_router, prefix="/api")


@app.on_event("startup")
def on_startup() -> None:
    if engine.dialect.name == "sqlite":
        Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/test-cors")
def test_cors():
    return {"cors": "working"}
