from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from db.database import Base, engine
from internal.config import settings
from routers import converter, user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(converter.router)
app.include_router(user.router)


@app.get("/")
async def home():
    return {
        "env": settings.UPLOADCARE_API_KEY,
        "dropbox": settings.DROPBOX_ACCESS_TOKEN
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
