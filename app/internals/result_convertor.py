import pandas as pd 
import numpy as np 
import re 


def getStudentDetails(text: str):
    """
    This function takes the text from the image and returns a pandas dataframe
    with the student details.
    """

    studentDataPattern = re.findall(
        r'[STB]\d{9}\s*\w*\s*\w*\s*\w*\s*\w*\w*\s*\w*\s*\w*\s*\w*\s*', text)
    
    studentDataDict = {'seatNumber': [], 'StudentName': []}
    for data in studentDataPattern:
        studentData = data.split()
        studentDataDict['seatNumber'].append(studentData[0])
        studentDataDict['StudentName'].append(studentData[1]+' '+studentData[2]+' '+studentData[3])
        studentDataDataFrame = pd.DataFrame(studentDataDict)
    return studentDataDataFrame

        

