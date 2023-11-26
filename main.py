from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI
from routers import converter
from internal.config import Settings, get_settings





app = FastAPI()
app.include_router(converter.router)


@app.get("/")
async def home(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "env": settings.UPLOADCARE_API_KEY,
        "dropbox": settings.DROPBOX_ACCESS_TOKEN
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)