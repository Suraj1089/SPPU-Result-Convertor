import streamlit as st
import pandas as pd
import PyPDF2
import base64
import re
import os 
from st_aggrid.grid_options_builder import GridOptionsBuilder

@st.cache
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


@st.cache
def getTabledownloadLink(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    """
    csv = df.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="output.csv">Download Excel file</a>'
    return href



@st.cache
def cleanText(text: str) -> str:
    subjects = ['INFORMATION AND CYBER SECURITY', 'MACHINE LEARNING & APPS.', 
                'SOFTWARE DESIGN AND MODELING', 'BUS. ANALYTICS & INTEL.', 'SW. TESTING & QA.',
                'COMPUTER LABORATORY-VII', 'COMPUTER LABORATORY-VII', 'COMPUTER LABORATORY-VIII', 
                'COMPUTER LABORATORY-VIII', 'PROJECT PHASE-I', 'CRITICAL THINKING',
                'DISTRIBUTED COMPUTING SYSTEM', 'UBIQUITOUS COMPUTING', 'INTERNET OF THINGS (IOT)', 
                'INTERNET OF THINGS (IOT)', 'SOCIAL MEDIA ANALYTICS', 'COMPUTER LABORATORY-IX', 'COMPUTER LABORATORY-IX', 
                'COMPUTER LABORATORY-X', 'PROJECT WORK', 'PROJECT WORK', 'IOT- APPLI. IN ENGG. FIELD']
    
    for i in subjects:
        text = text.replace(i, '')

    # SE subject names and TE subject names
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


@st.cache(suppress_st_warning=True)
def displayPDF(file):
    """
    Function to display PDF in Streamlit

    """
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


@st.cache
def pdfToText(path):
    pdfreader = PyPDF2.PdfFileReader(path)
    no_of_pages = pdfreader.numPages
    with open('final_txt.txt', 'w') as f:
        for i in range(0, no_of_pages):
            pagObj = pdfreader.getPage(i)
            f.write(pagObj.extractText())
    with open('final_txt.txt', 'r') as f:
        text = f.read()
    if os.path.exists("final_txt.txt"):
        os.remove("final_txt.txt")
        return text


@st.cache
def showUploadedFile(file):
    f = pd.read_csv(file)
    return f


@st.cache
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
        ], 'OR': [], 'TOT': [], 'CRD': [], 'GRD': [], 'PTS1': [], 'PTS2': []}
        
        for i in pattern:
            temp = i.split()
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
        dataframe = pd.DataFrame(d)
        subject_codes[codes] = dataframe
    return subject_codes



def displayInteractive(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(enableValue=True, enableRowGroup=True, enablePivot=True,
                                sortable=True, filter=True, editable=True, resizable=True)
    gb.configure_selection(selection_mode='multiple', use_checkbox=True)
    gb.configure_side_bar()
    gridOptions = gb.build()
    return gridOptions