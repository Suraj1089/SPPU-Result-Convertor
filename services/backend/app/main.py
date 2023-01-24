from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home_page():
    return {"message": "Hello World"}

# upload pdf file
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    await file.read()
    return {"filename": file.filename}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

