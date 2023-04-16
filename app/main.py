import casbin_sqlalchemy_adapter
import casbin

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from app.api.api_v1.api import api_router
# from app.database import engine, Model
#
# Model.metadata.create_all(bind=engine)
from app.core.config import settings
from app.db.base import Base
from app.db.session_async import SQLALCHEMY_DATABASE_URL, engine

adapter = casbin_sqlalchemy_adapter.Adapter(SQLALCHEMY_DATABASE_URL)

enforce = casbin.Enforcer('./casbin/rbac_model.conf', adapter, True)

async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


def include_router(app):
    app.include_router(api_router)  # список маршрутов для API


def include_staticfiles(app):
    app.mount('/media', StaticFiles(directory='media'), name='media')


def start_application():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    # app = FastAPI()
    include_router(app)
    include_staticfiles(app)
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"], #[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    return app


app = start_application()

add_pagination(app)


@app.on_event("startup")
async def startup_event():
    print('startup fastapi')


@app.on_event("shutdown")
async def stop_event():
    print('stop fastapi')


# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
