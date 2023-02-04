from fastapi import (
    FastAPI, 
    File, 
    UploadFile,
    Request,
    Response,
    status
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil
from crud import pdf_to_text



app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI()

app.mount("/static", StaticFiles(directory='static'), name="static")

templates = Jinja2Templates(directory="")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})


@app.get("/{some_route}", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})





@app.post("/upload",status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    try:
        with open(f'results/{file.filename}','wb') as buffer:
            shutil.copyfileobj(file.file,buffer)
        
        # print(file.filename)
        return {
            'message':'File uploaded successfully',
            'filename':file.filename,
            'filepath':f'results/{file.filename}'
        }
    except Exception as e:
        return Response(
            content={
                'message':'Not able to upload file try again',
                'error':str(e)
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )


@app.post('/convert-to-excel',status_code=status.HTTP_201_CREATED)
def pdf_to_excel(pdf_file_path: str):
    text = pdf_to_text(pdf_file_path)
    return text


@app.get('/excel-file',status_code=status.HTTP_200_OK)
def download_exel_file():
    pass 

