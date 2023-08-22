import streamlit as st
import pandas as pd
# import PyPDF2
import base64
import re
import os 
import io
from typing import List
import pandas as pd
import pypdf


def getSubjectNames(text):
    pattern = r"\d{6}\s(.+?)\s\s\*"
    subject_codes = re.findall(pattern, text)
    return subject_codes


def getSubjectCodes(text: str,subjectCodeCount:int) -> list:
    pattern = re.findall(r'[1-4]{1}\d{4,6}\w{1}', text)
    # return a list of top 10 element having maximum occurence
    d = {}
    for i in pattern:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    return list(dict(sorted(d.items(), key=lambda item: item[1], reverse=True)).keys())[:subjectCodeCount]


def studentDetails(text: str):
    l = []
    pattern = re.findall(
        r'[STB]\d{9}\s*\w*\s*\w*\s*\w*\s*\w*\w*\s*\w*\s*\w*\s*\w*\s*', text)
    d = {'seat_no': [], 'name': []}
    for i in pattern:
        # split the string
        temp = i.split()
        d['seat_no'].append(temp[0])
        d['name'].append(temp[1]+' '+temp[2]+' '+temp[3])
        dataframe = pd.DataFrame(d)
    return dataframe


def studentSgpa(text: str):
    pattern = re.findall(r'SGPA1\W*\d*\W*\d*', text)
    # SGPA1: 8.3
    d = {'sgpa':[],'score':[]}
    for i in pattern:
        temp = i.split()
        d['sgpa'].append(temp[0])
        d['score'].append(temp[1])
    return pd.DataFrame(d)


def getTabledownloadLink(df: pd.DataFrame,fileName=str):
    """Generates a link allowing the data in a given panda dataframe to be downloaded as an Excel file.
    """
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    b64 = base64.b64encode(excel_buffer.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{fileName}">Download Excel file</a>'
    return href


def cleanText(text: str,year: str = 'SE') -> str:
    SE_SUBJECTS_END = [
        "DISCRETE MATHEMATICS",       
        "DISCRETE MATHEMATICS",       
        "LOGIC DESIGN & COMP. ORG.",  
        "DATA STRUCTURES & ALGO.",    
        "OBJECT ORIENTED PROGRAMMING",
        "BASIC OF COMPUTER NETWORK",  
        "LOGIC DESIGN COMP. ORG. LAB",
        "DATA STRUCTURES & ALGO. LAB",
        "OBJECT ORIENTED PROG. LAB",  
        "SOFT SKILL LAB",             
        "CYBER SECURITY AND LAW",    
        "ENGINEERING MATHEMATICS-III",   
        "ENGINEERING MATHEMATICS-III",   
        "PROCESSOR ARCHITECTURE",        
        "DATABASE MANAGEMENT SYSTEM",    
        "COMPUTER GRAPHICS",             
        "SOFTWARE ENGINEERING",          
        "PROG. SKILL DEVELOPMENT LAB",   
        "DATABASE MGMT. SYSTEM LAB",     
        "COMPUTER GRAPHICS LAB",         
        "PROJECT BASED LEARNING"
    ]
    subjects = ['OBJECT ORIENTED PROG. LAB','DATA STRUCTURES & ALGO. LAB','LOGIC DESIGN COMP. ORG. LAB','LOGIC DESIGN & COMP. ORG.','DATA STRUCTURES & ALGO.','INFORMATION AND CYBER SECURITY', 'MACHINE LEARNING & APPS.','DESIGN AND ANALYSIS OF ALG.' 
                'SOFTWARE DESIGN AND MODELING', 'BUS. ANALYTICS & INTEL.', 'SW. TESTING & QA.',
                'COMPUTER LABORATORY-VII', 'COMPUTER LABORATORY-VII', 'COMPUTER LABORATORY-VIII', 
                'COMPUTER LABORATORY-VIII', 'PROJECT PHASE-I', 'CRITICAL THINKING',
                'DISTRIBUTED COMPUTING SYSTEM', 'UBIQUITOUS COMPUTING', 'INTERNET OF THINGS (IOT)', 
                'INTERNET OF THINGS (IOT)', 'SOCIAL MEDIA ANALYTICS', 'COMPUTER LABORATORY-IX', 'COMPUTER LABORATORY-IX', 
                'COMPUTER LABORATORY-X', 'PROJECT WORK', 'PROJECT WORK', 'IOT- APPLI. IN ENGG. FIELD','INFO. & STORAGE RETRIEVAL']
    
    # first remove second year subject names
    if year == 'SE':
        for subject in SE_SUBJECTS_END:
            text = text.replace(subject,'')

        for i in subjects:
            text = text.replace(i, '')   
    else:
        for i in subjects:
            text = text.replace(i, '')
        for subject in SE_SUBJECTS_END:
            text = text.replace


    # SE subject names and TE subject names
    # BE subjects
    text = text.replace('INFO. & STORAGE RETRIEVAL','')
    text = text.replace('SOFTWARE PROJECT MANAGEMENT','')
    text = text.replace('DEEP LEARNING','')
    text = text.replace('MOBILE COMPUTING','')
    text = text.replace('INTRODUCTION TO DEVOPS','')
    text = text.replace('LAB PRACTICE III','')
    text = text.replace('LAB PRACTICE IV','')
    text = text.replace('PROJECT STAGE-I','')
    text = text.replace('COPYRIGHTS AND PATENTS','')
    text = text.replace('PROJECT STAGE II','')
    text = text.replace('DISTRIBUTED SYSTEMS','')
    text = text.replace('GAME ENGINEERING','')
    text = text.replace('BLOCKCHAIN TECHNOLOGY','')
    text = text.replace('STARTUP & ENTREPRENEURSHIP','')
    text = text.replace('LAB PRACTICE VI','')
    text = text.replace('LAB PRACTICE V','')
    text = text.replace('CYBER LAWS & USE OF S.M','')
    text = text.replace('TOTAL GRADE POINTS / TOTAL CREDITS','')
    text = text.replace('FOURTH YEAR','')
    text = text.replace('SE SGPA','')
    text = text.replace('FE SGPA','')
    text = text.replace('TE SGPA','')
    text = text.replace('FIRST CLASS WITH DISTINCTION','')
    text = text.replace('CGPA','')

    
    
    text = text.replace('DESIGN AND ANALYSIS OF ALG.','')
    text = text.replace('COMPUTER ORGANIZATION & ARCH.','')
    text = text.replace('THEORY OF COMPUTATION', '')
    text = text.replace('OPERATING SYSTEMS', '')
    text = text.replace('MACHINE LEARNING', '')
    text = text.replace('HUMAN COMPUTER INTERACTION', '')
    text = text.replace('A DESIGN AND ANALYSIS OF ALG.', '')
    text = text.replace('SEMINAR', '')
    text = text.replace('HUMAN COMP. INTERACTION-LAB.', '')
    text = text.replace('LABORATORY PRACTICE-I', '')
    text = text.replace('OPERATING SYSTEMS LAB(TW+PR)', '')
    text = text.replace('(TW+PR)', '')
    text = text.replace('STARTUP ECOSYSTEMS', '')
    text = text.replace('SEMINAR', '')
    text = text.replace('SEMINAR', '')
    text = text.replace('DISCRETE MATHEMATICS', '')
    text = text.replace('LOGIC DESIGN & COMP. ORG.', '')
    text = text.replace('DATA STRUCTURES & ALGO.', '')
    text = text.replace('OBJECT ORIENTED PROGRAMMING', '')
    text = text.replace('BASIC OF COMPUTER NETWORK', '')
    text = text.replace('LOGIC DESIGN COMP. ORG. LAB', '')
    text = text.replace('DATA STRUCTURES & ALGO. LAB', '')
    text = text.replace('DATA STRUCTURES & ALGO. LAB', '')
    text = text.replace('OBJECT ORIENTED PROG. LAB', '')
    text = text.replace('SOFT SKILL LAB', '')
    text = text.replace('ETHICS AND VALUES IN IT', '')
    text = text.replace('LAB', '')
    text = text.replace(
        'SAVITRIBAI PHULE PUNE UNIVERSITY ,S.E.(2019 CREDIT PAT.) EXAMINATION, OCT/NOV 2021', '')
    text = text.replace(
        'COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE', '')
    text = text.replace(
        'BRANCH CODE:  29-S.E.(2019 PAT.)(INFORMATIOM TECHNOLOGY)', '')
    text = text.replace('DATE : 21 APR 2022 ', '')
    text = text.replace(
        'COURSE NAME                      ISE      ESE     TOTAL      TW       PR       OR    Tot% Crd  Grd   GP  CP  P&R ORD', '')
    text = text.replace(
        'SAVITRIBAI PHULE PUNE UNIVERSITY, S.E.(2015 COURSE) EXAMINATION,MAY 2018', '')
    text = text.replace(
        'SAVITRIBAI PHULE PUNE UNIVERSITY ,T.E.(2019 COURSE) EXAMINATION, OCT/NOV 2021', '')
    text = text.replace(
        'COLLEGE    : D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE', '')
    text = text.replace(
        'COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE', '')
    text = text.replace(
        'BRANCH CODE: 29-S.E.(2015 PAT.)(INFORMATIOM TECHNOLOGY)', '')
    text = text.replace(
        'BRANCH CODE: 60-T.E.(2019 PAT.)(INFORMATION TECHNOLOGY)', '')
    text = text.replace('DATE       : 23 JUL 2018', '')
    text = text.replace('DATE : 06 MAY 2022', '')
    text = text.replace(
        '............CONFIDENTIAL- FOR VERIFICATION AND RECORD ONLY AT COLLEGE, NOT FOR DISTRIBUTION.......................................', '')
    text = text.replace(
        '....................................................................................................', '')
    text = text.replace(
        '............                  .......  .......  .......  .......  .......  .......  ...  ...  ...   ... ...  ... ...', '')

    text = text.replace('PAGE :-', '')
    text = text.replace('SEAT NO.', '')
    text = text.replace('SEAT NO.:', '')
    text = text.replace('NAME :', '')
    text = text.replace('MOTHER :', '')
    text = text.replace('PRN :', '')
    text = text.replace('CLG.: DYPP[8]', '')

    text = text.replace('..............................', '')
    text = text.replace('SEM.:1', '')
    text = text.replace('SEM.:2', '')
    text = text.replace(
        'OE       TH     [OE+TH]     TW       PR       OR    Tot% Crd  Grd  Pts   Pts', '')
    text = text.replace(
        'OE       TH     [OE+TH]     TW       PR       OR    Tot% Crd  Grd  Pts   Pts', '')
    text = text.replace('DYPP', '')
    text = text.replace('Grd   Crd', '')
    text = text.replace('SEM. 2', '')
    text = text.replace('SEM. 1', '')
    text = text.replace('~', '')
    text = text.replace(' .', '')
    text.replace('~', 'nan')
    text = text.replace('*', ' ')
    text = text.replace(':', ' ')
    text = text.replace('-', 'n')
    text = text.replace('SECOND YEAR SGPA', '')
    text = text.replace('TOTAL CREDITS EARNED ', '')

    text = text.strip()
    return text
# function to display pdf


def displayPDF(file):
    """
    Function to display PDF in Streamlit

    """
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

# Issue: https://github.com/Suraj1089/SPPU-Result-Convertor/security/dependabot/17
# Migrate to pypdf
# @st.cache_resource
# def pdfToText(path):
#     pdfreader = PyPDF2.PdfReader(path) 
#     no_of_pages = len(pdfreader.pages)
#     with open('final_txt.txt', 'w') as f:
#         for i in range(0, no_of_pages):
#             # pagObj = pdfreader.getPage(i) # deprecated
#             pagObj = pdfreader.pages[i]
#             f.write(pagObj.extract_text())
#     with open('final_txt.txt', 'r') as f:
#         text = f.read()
#     if os.path.exists("final_txt.txt"):
#         # os.remove("final_txt.txt")
#         return text


@st.cache_resource
def pdfToText(path):
    reader = pypdf.PdfReader(path)
    noOfPages = len(reader.pages)
    with open('extractedText.txt','w') as file:
        for line in range(0,noOfPages):
            page = reader.pages[line]
            file.write(page.extract_text())
    with open('extractedText.txt','r') as file:
        text = file.read()
    if os.path.exists('extractedText.txt'):
        os.remove('extractedText.txt')
        pass
    return text


def showUploadedFile(file):
    f = pd.read_csv(file)
    return f


def cleanMarks(text: str, subject_codes) -> dict:
    """
    This function will clean the marks from the pdf file.
    """
    # 
    for codes in subject_codes.keys():
        # Marks pattern
        pattern = re.findall(
            fr'{codes}[A-Z]?\s+\w+[\/!#&$@ \*~]*\w*\s*\w*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\+]*\w*\s*\+*\w*\s*\+*\w*\s*\w*\+*\s*\w*\s*\+*\w*\s', text)

        # dataframe column names
        d = {'subject': [], 'OE': [], 'TH': [], 'OE_TH': [], 'TW': [], 'PR': [
        ], 'OR': [], 'TOT': [], 'CRD': [], 'GRD': [], 'PTS1': [], 'PTS2': [],'CP':[]}
        
        # uncomment to log the data
        # with open('patern.txt', 'w') as patt:
        #     patt.write(str(pattern))
        for index,i in enumerate(pattern):
            temp = i.split()
            # print(len(temp))
            # max_lenght = 
            if len(temp) < 13:
                while len(temp)!=13:
                    temp.append('Error')
            
        
            d['subject'].append(temp[0])
            d['OE'].append(temp[1])
            d['TH'].append(temp[2])
            d['OE_TH'].append(temp[3])
            d['TW'].append(temp[4])
            d['PR'].append(temp[5])
            d['OR'].append(temp[6])
            d['TOT'].append(temp[7])
            d['CRD'].append(temp[8])
            d['GRD'].append(temp[9])
            d['PTS1'].append(temp[10])
            d['PTS2'].append(temp[11])
            d['CP'].append(temp[12])
        dataframe = pd.DataFrame(d)
        subject_codes[codes] = dataframe
    return subject_codes

