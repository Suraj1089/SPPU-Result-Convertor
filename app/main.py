from fastapi import FastAPI
from .routers import result_convertor, result_visualiser

app = FastAPI()


app.include_router(result_convertor.router)
app.include_router(result_visualiser.router)



