from fastapi import FastAPI, File, UploadFile


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Hello World"}

# upload pdf file
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    await file.read()
    return {"filename": file.filename}