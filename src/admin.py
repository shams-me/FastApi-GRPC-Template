from fastapi import FastAPI, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette_admin.contrib.sqla import Admin, ModelView

from src.models.user import User, RefreshToken, Device, SocialAccount
from src.settings import settings

engine = create_engine(settings.pg_dsn)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


class UserAdmin(ModelView):
    pass


class RefreshTokenAdmin(ModelView):
    pass


class DeviceAdmin(ModelView):
    pass


class SocialAccountAdmin(ModelView):
    pass


admin = Admin(engine, title="FastAPI Admin Panel")
admin.add_view(UserAdmin(User, icon="fa fa-user"))
admin.add_view(RefreshTokenAdmin(RefreshToken, icon="fa fa-user"))
admin.add_view(DeviceAdmin(Device, icon="fa fa-device"))
admin.add_view(SocialAccountAdmin(SocialAccount, icon="fa fa-device"))

admin.mount_to(app)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application with Admin Panel"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
