import time
import streamlit as st
import pandas as pd
import numpy as np
import PyPDF2
from io import StringIO
import base64
import re
import os 
import plotly.express as px
# import seaborn as sns
import matplotlib.pyplot as plt
from st_aggrid import GridUpdateMode, DataReturnMode
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
# from functionforDownloadButtons import download_button


@st.cache
def student_details(text: str):
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
def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="output.csv">Download Excel file</a>'
    return href

# find name,seat_no,prn_no
@st.cache
def cleanSE2015PatternMarks(text:str)->str:
    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY ,S.E.(2015 COURSE) EXAMINATION, MAY 2020','')
    text = text.replace('COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE','')
    text = text.replace('BRANCH CODE: 29-S.E.(2015 PAT.)(INFORMATION TECHNOLOGY)','')
    text = text.replace('DISCRETE STRUCTURES','')
    text = text.replace('COMPUTER ORGANIZATION & ARCH.','')
    text = text.replace('DIGI ELECTRO & LOGIC DESIGN','')
    text = text.replace('FUNDAMENTAL OF DATASTRUCTURE','')
    text = text.replace('PROB SOLVI & OOPS','')
    text = text.replace('DIGITAL LABORATORY','')
    text = text.replace('PROGRAMMING LABORATORY','')
    text = text.replace('OBJECT ORIEN PROGRAMMING LAB.','')
    text = text.replace('COMMUNICATION SKILLS','')
    text = text.replace('ROAD SAFETY','')
    text = text.replace('ENGINEERING MATHEMATICS -III','')
    text = text.replace('COMPUTER GRAPHICS','')
    text = text.replace('PROCESSOR ARCH AND INTERFACING   *','')
    text = text.replace('DATA STRUCTURES & FILES','')
    text = text.replace('FOUND OF COMM & COMP NETWORK','')
    text = text.replace('PROCESSOR INTERFACING LAB','')
    text = text.replace('DATA STRUCTURE & FILES LAB','')
    text = text.replace('COMPUTER GRAPHICS LABORATORY','')
    text = text.replace('WATER MANAGEMENT','')

@st.cache
def cleanText(text: str) -> str:
    text = text.replace('THEORY OF COMPUTATION','')
    text = text.replace('DATABASE MANAGEMENT SYSTEMS','')
    text = text.replace('SW. ENGG. & PROJECT MGMT.','')
    text = text.replace('OPERATING SYSTEM','')
    text = text.replace('HUMAN-COMPUTER INTERACTION','')
    text = text.replace('SOFTWARE LABORATORY-I','')
    text = text.replace('SOFTWARE LABORATORY-II','')
    text = text.replace('SOFTWARE LABORATORY-III','')
    text = text.replace('LEDSP. & PERSONALITY DEVOP.','')
    text = text.replace('COMPUTER NETWORK TECHNOLOGY','')
    text = text.replace('SYSTEMS PROGRAMMING','')
    text = text.replace('DESIGN AND ANALYSIS OF ALGO.','')
    text = text.replace('CLOUD COMPUTING','')
    text = text.replace('DATA SCI. & BIG DATA ANALYTICS','')
    text = text.replace('SOFTWARE LABORATORY-IV','')
    text = text.replace('SOFTWARE LABORATORY-V','')
    text = text.replace('SOFTWARE LABORATORY-VI','')
    text = text.replace('PROJECT BASED  SEMINAR','')
    text = text.replace('HEALTH & FITNESS MGMT.','')
    text = text.replace('TOTAL CREDITS EARNED','')
    text = text.replace('TOTAL CREDITS EARNED','')
    text = text.replace('TOTAL CREDITS EARNED','')
    text = text.replace('THIRD YEAR SGPA','')
    text = text.replace('.........................CONFIDENTIAL- FOR VERIFICATION AND RECORD ONLY AT COLLEGE, NOT FOR DISTRIBUTION..........................','')
    text = text.replace('CONFIDENTIAL- FOR VERIFICATION AND RECORD ONLY AT COLLEGE, NOT FOR DISTRIBUTION','')
    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY ,T.E.(2015 COURSE) EXAMINATION, MAY 2020','')
    text = text.replace('COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE','')
    text = text.replace('BRANCH CODE: 60-T.E.(2015 PAT.)(INFORMATION TECHNOLOGY)','')
    text = text.replace('DATE : 06 JAN 2021','')
    
    text = text.replace('SUBJECT NAME OE TH [OE+TH] TW PR OR Tot% Crd Grd GP CP P&R ORD','')
    text = text.replace('SUBJECT NAME IN TH [IN+TH] TW PR OR Tot% Crd Grd GP CP P&R ORD','')
    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY ,S.E.(2015 COURSE) EXAMINATION, MAY 2020 DATE : 24 FEB 2021','')
    text = text.replace('COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING, PUNE','')
    text = text.replace('COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING, PUNE','')
    text = text.replace('BRANCH CODE: 29-S.E.(2015 PAT.)(INFORMATION TECHNOLOGY)','')
    text = text.replace('DATE : 24 FEB 2021','')
    text = text.replace('SUBJECT NAME OE TH [OE+TH] TW PR OR Tot% Crd Grd GP CP P&R ORD','')
    text = text.replace('SUBJECT NAME OE TH [OE+TH] TW PR OR Tot% Crd Grd GP CP P&R ORD','')
    text = text.replace('DISCRETE STRUCTURES', '')
    text = text.replace(' COMPUTER ORGANIZATION & ARCH.', '')
    text = text.replace('DIGI ELECTRO & LOGIC DESIGN', '')
    text = text.replace('FUNDAMENTAL OF DATASTRUCTURE', '')
    text = text.replace('PROB SOLVI & OOPS', '')
    text = text.replace('DIGITAL LABORATORY', '')
    text = text.replace(' PROGRAMMING LABORATORY', '')
    text = text.replace('OBJECT ORIEN PROGRAMMING LAB.', '')
    text = text.replace('COMPUTER GRAPHICS', '')
    text = text.replace('ENGINEERING MATHEMATICS -III', '')
    text = text.replace('PROCESSOR ARCH AND INTERFACING', '')
    text = text.replace('ROAD SAFETY','')
    text = text.replace('DATA STRUCTURES & FILES','')
    text = text.replace('FOUND OF COMM & COMP NETWORK','')
    text = text.replace('PROCESSOR INTERFACING LAB','')
    text = text.replace('DATA STRUCTURE & FILES LAB','')
    text = text.replace('COMPUTER GRAPHICS LABORATORY','')
    text = text.replace('WATER MANAGEMENT','')
    text = text.replace('COMMUNICATION SKILLS','')
    text = text.replace('.........................CONFIDENTIAL- FOR VERIFICATION AND RECORD ONLY AT COLLEGE, NOT FOR DISTRIBUTION..........................','')
    text = text.replace('TOTAL CREDITS EARNED :','')
    text = text.replace('SECOND YEAR SGPA :','')
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
    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY ,T.E.(2015 COURSE) EXAMINATION, MAY 2020 DATE : 06 JAN 2021', '')
    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY ,T.E.(2015 COURSE) EXAMINATION, MAY 2020', '')
    text = text.replace('COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING, PUNE', '')
    text = text.replace('BRANCH CODE: 60-T.E.(2015 PAT.)(INFORMATION TECHNOLOGY)', '')
    text = text.replace('SUBJECT NAME IN TH [IN+TH] TW PR OR Tot% Crd Grd GP CP P&R ORD', '')
    text = text.replace('THEORY OF COMPUTATION', '')
    text = text.replace('DATABASE MANAGEMENT SYSTEMS', '')
    text = text.replace('OPERATING SYSTEM', '')
    text = text.replace('HUMAN-COMPUTER INTERACTION', '')
    text = text.replace('SW. ENGG. & PROJECT MGMT.', '')
    text = text.replace('SOFTWARE LABORATORY-I', '')
    text = text.replace('SOFTWARE LABORATORY-II', '')
    text = text.replace('SOFTWARE LABORATORY-III', '')
    text = text.replace('LEDSP. & PERSONALITY DEVOP.', '')
    text = text.replace('COMPUTER NETWORK TECHNOLOGY', '')
    text = text.replace('SYSTEMS PROGRAMMING', '')
    text = text.replace('SYSTEMS PROGRAMMING              *', '')
    text = text.replace('DESIGN AND ANALYSIS OF ALGO.', '')
    text = text.replace('DESIGN AND ANALYSIS OF ALGO.     *', '')
    text = text.replace('CLOUD COMPUTING', '')
    text = text.replace('DATA SCI. & BIG DATA ANALYTICS', '')
    text = text.replace('DATA SCI. & BIG DATA ANALYTICS', '')
    text = text.replace('SOFTWARE LABORATORY-IV', '')
    text = text.replace('SOFTWARE LABORATORY-V', '')
    text = text.replace('SOFTWARE LABORATORY-VI', '')
    text = text.replace('PROJECT BASED SEMINAR', '')
    text = text.replace('HEALTH & FITNESS MGMT.', '')
    text = text.replace('TOTAL CREDITS EARNED', '')
    text = text.replace('THIRD YEAR SGPA', '')
    text = text.replace('DYPP[8]', '')
    text = text.replace('DYPP[8]', '')
    text = text.replace('SEM.:1', '')
    text = text.replace('SEM.:2', '')
    text = text.replace('SUBJECT NAME OE TH [OE+TH] TW PR OR Tot% Crd Grd GP CP P&R ORD', '')
    
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
    # SECOND YEAR SGPA   8.08, TOTAL CREDITS EARNED   50
    text = text.strip()
    return text
# function to display pdf


@st.cache(suppress_st_warning=True)
def displayPDF(file):
    # Opening file from file path
    # with open(file, "rb") as f:
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
def show_uploaded_file(file):
    f = pd.read_csv(file)
    return f


@st.cache
def cleanMarks(text: str, subject_codes) -> dict:
    """
    This function will clean the marks from the pdf file
    ## Parameters
    text : str 
    ## return
    dictonary containing dataframes of subject wise marks
    """
    for codes in subject_codes.keys():
        pattern = re.findall(
            fr'{codes}[A-Z]?\s+\w+[\/!#&$@ \*~]*\w*\s*\w*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\+]*\w*\s*\+*\w*\s*\+*\w*\s*\w*\+*\s*\w*\s*\+*\w*\s', text)

        d = {'subject': [], 'OE': [], 'TH': [], 'OE_TH': [], 'TW': [], 'PR': [
        ], 'OR': [], 'TOT': [], 'CRD': [], 'GRD': [], 'PTS1': [], 'PTS2': []}
        for i in pattern:
            # split the string in list
            temp = i.split()
            # print(len(temp))
            # print(temp)
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
        # dataframe = dataframe.replace('nnnnnnn',np.nan)
        # dataframe = dataframe.dropna(axis=1,how='all')
        subject_codes[codes] = dataframe
    return subject_codes

@st.cache
def cleanMarksDuplicateSubject(text: str, subject_codes) -> dict:
    """
    This function will clean the marks from the pdf file
    ## Parameters
    text : str 
    ## return
    dictonary containing dataframes of subject wise marks
    """
    for codes in subject_codes.keys():
        pattern = re.findall(
            fr'{codes}[A-Z]?\s+\w+[\/!#&$@ \*~]*\w*\s*\w*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\+]*\w*\s*\+*\w*\s*\+*\w*\s*\w*\+*\s*\w*\s*\+*\w*\s', text)

        d = {'subject': [], 'OE': [], 'TH': [], 'OE_TH': [], 'TW': [], 'PR': [
        ], 'OR': [], 'TOT': [], 'CRD': [], 'GRD': [], 'PTS1': [], 'PTS2': []}
        for i in pattern:
            # split the string in list
            temp = i.split()
            # print(len(temp))
            # print(temp)
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
        # dataframe = dataframe.replace('nnnnnnn',np.nan)
        # dataframe = dataframe.dropna(axis=1,how='all')
        subject_codes[codes] = dataframe
    return subject_codes




@st.cache
def concat_subjects(d: dict):
    """
        function to concat subject wise marks
        ## Parameters
        text : str
        ## return
        dataframe containing student marks of all subjects.
    """
    return pd.concat([i for i in d.values()], axis=1)


def create_analysis_table(dataframe):
    """
        function to create analysis table
        ## Parameters
        dataframe : dataframe
        ## return
        dataframe with analysis table
    """
    # create analysis table
    d = {'Total No of Students':None,'All Clear':None,'First Class with Distinction':None,
            'First Class':None,'Higher Second Class':None,'Second Class':None,'Pass Class':None,
            'One Backlog':None,'Two Backlog':None,'Three Backlog':None,'Four Backlog':None,
            'More than four Backlog':None,'Students Promoted to New class':None
            
        }
        
    

def subject_wise_analyse(dataframe,subject_codes):
    """
        function to analyse subject wise marks
    
    """
    for codes in subject_codes.keys():
        subject_codes[codes] = dataframe[dataframe['subject']==codes]
    return subject_codes


def remove_subject_names(text : str) -> str:
    """
        function to remove subject names from text
    """
    subject_names = []
    st.warning('Enter subject names present in pdf file(only for other than IT department)')
    with st.form(key='remove_subject_names'):
        total_no_of_subjects = int(st.number_input('Enter total no of subjects'))
        for i in range(total_no_of_subjects):
            subject_names.append(st.text_input(f'Enter subject {i+1} name'))
        submit = st.form_submit_button(label='Submit')
    if submit:
        for i in subject_names:
            text = text.replace(i,'')
    return text


def dispaly_interactive(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(enableValue=True, enableRowGroup=True, enablePivot=True,
                                sortable=True, filter=True, editable=True, resizable=True)
    gb.configure_selection(selection_mode='multiple', use_checkbox=True)
    gb.configure_side_bar()
    gridOptions = gb.build()
    return gridOptions


@st.cache
def cleanTE2015Marks(text:str)->str:

    text = text.replace('THEORY OF COMPUTATION','')
    text = text.replace('DATABASE MANAGEMENT SYSTEMS','')
    text = text.replace('SW. ENGG. & PROJECT MGMT.','')
    text = text.replace('OPERATING SYSTEM','')
    text = text.replace('HUMAN-COMPUTER INTERACTION','')
    text = text.replace('SOFTWARE LABORATORY-I','')
    text = text.replace('SOFTWARE LABORATORY-II','')
    text = text.replace('SOFTWARE LABORATORY-III','')
    text = text.replace('LEDSP. & PERSONALITY DEVOP.','')
    text = text.replace('COMPUTER NETWORK TECHNOLOGY','')
    text = text.replace('SYSTEMS PROGRAMMING','')
    text = text.replace('DESIGN AND ANALYSIS OF ALGO.','')
    text = text.replace('CLOUD COMPUTING','')
    text = text.replace('DATA SCI. & BIG DATA ANALYTICS','')
    text = text.replace('SOFTWARE LABORATORY-IV','')
    text = text.replace('SOFTWARE LABORATORY-V','')
    text = text.replace('SOFTWARE LABORATORY-VI','')
    text = text.replace('PROJECT BASED  SEMINAR','')
    text = text.replace('HEALTH & FITNESS MGMT.','')
    text = text.replace('TOTAL CREDITS EARNED','')
    text = text.replace('TOTAL CREDITS EARNED','')
    text = text.replace('TOTAL CREDITS EARNED','')
    text = text.replace('THIRD YEAR SGPA','')
    text = text.replace('.........................CONFIDENTIAL- FOR VERIFICATION AND RECORD ONLY AT COLLEGE, NOT FOR DISTRIBUTION..........................','')
    text = text.replace('CONFIDENTIAL- FOR VERIFICATION AND RECORD ONLY AT COLLEGE, NOT FOR DISTRIBUTION','')
    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY ,T.E.(2015 COURSE) EXAMINATION, MAY 2020','')
    text = text.replace('COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE','')
    text = text.replace('BRANCH CODE: 60-T.E.(2015 PAT.)(INFORMATION TECHNOLOGY)','')
    text = text.replace('DATE : 06 JAN 2021','')

    return text

