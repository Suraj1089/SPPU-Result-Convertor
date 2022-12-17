from fastapi import APIRouter


router = APIRouter(
    prefix='/convertResult',
    tags=['Result Convertor']
)


@router.get('')
async def home():
    return {"data": "hello suraj"}


@router.post('/changeColumnsNames')
async def changeColumnsNames():
    return {
        "data": "columns names changed"
    }


@router.post('/convertToCSV')
async def convertToCSV():
    return {
        "data": "converted to CSV"
    }


@router.post('/convertToJSON')
async def convertToJSON():
    return {
        "data": "converted to JSON"
    }


@router.post('/convertToExcel')
async def convertToExcel():
    return {
        "data": "converted to Excel"
    }
