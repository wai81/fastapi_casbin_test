from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_authz import CasbinMiddleware
import casbin

def include_staticfiles(app):
    app.mount('/media', StaticFiles(directory='media'), name='media')

enforcer = casbin.Enforcer('./config_casbin/rbac_model.conf', './config_casbin/rbac_policy.csv')

def start_application():
    # app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    app = FastAPI()
    include_staticfiles(app)
    # if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], #[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(CasbinMiddleware, enforcer=enforcer)
    return app

app = start_application()


@app.on_event("startup")
async def startup_event():
    print('startup fastapi')


@app.on_event("shutdown")
async def stop_event():
    print('stop fastapi')

#  https://github.com/pycasbin/fastapi-authz