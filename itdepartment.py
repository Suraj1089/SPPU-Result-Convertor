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
def cleanSE2015Marks(text:str)->str:
    text = text.replace('DISCRETE STRUCTURES','')
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
    text = text.replace('PROCESSOR ARCH AND INTERFACING','')
    text = text.replace('DATA STRUCTURES & FILES','')
    text = text.replace('FOUND OF COMM & COMP NETWORK','')
    text = text.replace('PROCESSOR INTERFACING LAB','')
    text = text.replace('DATA STRUCTURE & FILES LAB','')
    text = text.replace('COMPUTER GRAPHICS LABORATORY','')
    text = text.replace('WATER MANAGEMENT','')
    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY ,S.E.(2015 COURSE) EXAMINATION, MAY 2020','')
    text = text.replace('COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING, PUNE','')
    text = text.replace('BRANCH CODE: 29-S.E.(2015 PAT.)(INFORMATION TECHNOLOGY)','')
    text = text.replace('SUBJECT NAME OE TH [OE+TH] TW PR OR Tot% Crd Grd GP CP P&R ORD','')
    text = text.replace('SEM.:')


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
    text = 
#     314441 THEORY OF COMPUTATION 021/030 049/070 070/100 --- --- --- 70 04 A+ 09 36 --- ---
#  314442 DATABASE MANAGEMENT SYSTEMS 022/030 048/070 070/100 --- --- --- 70 04 A+ 09 36 --- ---
#  314443 SW. ENGG. & PROJECT MGMT. 018/030 044/070 062/100 --- --- --- 62 03 A 08 24 --- ---
#  314444 OPERATING SYSTEM 028/030 052/070 080/100 --- --- --- 80 04 O 10 40 --- ---
#  314445 HUMAN-COMPUTER INTERACTION 023/030 038/070 061/100 --- --- --- 61 03 A 08 24 --- ---
#  314446 SOFTWARE LABORATORY-I --- --- --- --- 043/050 --- 86 01 O 10 10 --- ---
#  314446 SOFTWARE LABORATORY-I --- --- --- 022/025 --- 043/050 86 01 O 10 10 --- ---
#  314447 SOFTWARE LABORATORY-II --- --- --- 022/025 044/050 --- 88 02 O 10 20 --- ---
#  314448 SOFTWARE LABORATORY-III --- --- --- 044/050 --- --- 88 01 O 10 10 --- ---
#  310260D LEDSP. & PERSONALITY DEVOP. --- --- --- PP --- --- PP 00 P 00 00 --- ---
# SEM.:2
#  314450 COMPUTER NETWORK TECHNOLOGY * 028/030 059/070 087/100 --- --- --- 87 03 O 10 30 --- ---
#  314451 SYSTEMS PROGRAMMING * 024/030 054/070 078/100 --- --- --- 78 04 A+ 09 36 --- ---
#  314452 DESIGN AND ANALYSIS OF ALGO. * 017/030 046/070 063/100 --- --- --- 63 04 A 08 32 --- ---
#  314453 CLOUD COMPUTING * 021/030 051/070 072/100 --- --- --- 72 03 A+ 09 27 --- ---
#  314454 DATA SCI. & BIG DATA ANALYTICS * 020/030 049/070 069/100 --- --- --- 69 04 A 08 32 --- ---
#  314455 SOFTWARE LABORATORY-IV * --- --- --- 022/025 --- 023/025 90 01 O 10 10 --- ---
#  314456 SOFTWARE LABORATORY-V * --- --- --- 040/050 --- --- 80 01 O 10 10 --- ---
#  314456 SOFTWARE LABORATORY-V * --- --- --- --- 042/050 --- 84 01 O 10 10 --- ---
#  314457 SOFTWARE LABORATORY-VI * --- --- --- 023/025 023/025 --- 92 01 O 10 10 --- ---
#  314458 PROJECT BASED SEMINAR * --- --- --- --- --- 045/050 90 01 O 10 10 --- ---
#  314459D HEALTH & FITNESS MGMT. 


@st.cache
def cleanText(text: str) -> str:
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
    # dict to store marks
    # subject_codes = {'214441':None, '214442':None, '214443':None, '214444':None,
    #                  '214445':None, '214446':None, '214447':None, '214448':None, '214449':None, '202054A':None,
    #                  '207003':None, '214450':None, '214451':None, '214452':None, '214453':None, '214454':None, '214455':None, '214456':None, '210258A':None}

    # find subject wise marks
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


# # @st.cache
# # def change_column_data_type(dataframe):

#     """
#         function to change data type of columns
#         ## Parameters
#         dataframe : dataframe
#         ## return
#         dataframe with changed data type
#     """
#     dataframe['OE'] = dataframe['OE'].astype('float')
#     dataframe['TH'] = dataframe['TH'].astype('float')
#     dataframe['OE_TH'] = dataframe['OE_TH'].astype('float')
#     dataframe['TW'] = dataframe['TW'].astype('float')
#     dataframe['PR'] = dataframe['PR'].astype('float')
#     dataframe['OR'] = dataframe['OR'].astype('float')
#     dataframe['TOT'] = dataframe['TOT'].astype('float')
#     dataframe['CRD'] = dataframe['CRD'].astype('float')
#     dataframe['PTS1'] = dataframe['PTS1'].astype('float')
#     dataframe['PTS2'] = dataframe['PTS2'].astype('float')
#     return dataframe

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