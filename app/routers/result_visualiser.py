from fastapi import APIRouter


router = APIRouter(
    prefix='/visualiseResult',
    tags=['Result Visualiser']
)


@router.get('')
async def home():
    return {"data": "hello suraj"}

@router.post('/visualise')
async def visualise():
    return {
        "data": "visualised"
    }

@router.post('/download')
async def download():
    return {
        "data": "downloaded"
    }

@router.post('/get-toppers/{toppperCount}')
async def getToppers(topperCount: int):
    return {
        "data": "toppers"
    }

@router.post('/get-failers/')
async def getFailers():
    return {
        "data": "failers"
    }

@router.post('/get-student-details/{studentId}')
async def getStudentDetails(studentId: int):
    return {
        "data": "student details"
    }

@router.post('/get-student-marks/{studentId}')
async def getStudentMarks(studentId: int):
    return {
        "data": "student marks"
    }

