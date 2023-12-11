from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from sqladmin import Admin, ModelView

from db.database import Base, engine
from db.models.user import User
from api.v1.endpoints import converter, user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

Base.metadata.create_all(bind=engine)

app = FastAPI()

# register fastapi admin panel
admin = Admin(app=app, engine=engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.email]


admin.add_view(UserAdmin)

app.include_router(converter.router)
app.include_router(user.router)


@app.get("/")
async def home():
    return RedirectResponse('/docs')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
