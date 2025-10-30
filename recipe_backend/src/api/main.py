from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .db import engine
from .db import Base
from .routers_auth import router as auth_router
from .routers_users import router as users_router
from .routers_recipes import router as recipes_router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    contact={"name": "Recipe Hub"},
    license_info={"name": "MIT"},
    openapi_tags=[
        {"name": "auth", "description": "Authentication endpoints"},
        {"name": "users", "description": "User management"},
        {"name": "recipes", "description": "Recipe operations"},
        {"name": "health", "description": "Service health and status"},
    ],
)

# Configure CORS with allowed origins
origins = ["*"]
if settings.REACT_APP_FRONTEND_URL:
    origins = [settings.REACT_APP_FRONTEND_URL]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables (simple auto-migrate for SQLite demo)
Base.metadata.create_all(bind=engine)

@app.get("/", tags=["health"], summary="Health Check", description="Simple health check endpoint.")
def health_check():
    """Return a simple health payload to verify the API is running."""
    return {"message": "Healthy"}

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(recipes_router)
