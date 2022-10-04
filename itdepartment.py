import time
import streamlit as st
import pandas as pd
import numpy as np
import PyPDF2
from io import StringIO
import base64
import re

import tabula.io as tabula
import plotly.express as px
# import seaborn as sns
import matplotlib.pyplot as plt


# --- LOAD CSS, PDF & PROFIL PIC ---
with open('css/main.css') as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


@st.cache
def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="SeatNo.csv">Download Excel file</a>'
    return href

# find name,seat_no,prn_no


# @st.cache

def student_details(text : str):
    pattern = re.findall(
        r'[ST]\w{9}\s*\w*\s*\w*\s*\w*\s*\w*\w*\s*\w*\s*\w*\s*\w*\s*', text)
    d = {'seat_no': [], 'name': [], 'mother_name': [], 'PRN_NO': [],'undefine1':[]}
    # 0-seat no 1-2-3-name 4-mother_name 5-prn
    for i in pattern:
        #split the string
        temp = i.split()
        # print(len(temp))
        #create list of same size 
        if len(temp) <= 6:
            temp.append('Nan')
        d['seat_no'].append(temp[0])
        d['name'].append(temp[1]+' '+temp[2]+' '+temp[3])
        d['mother_name'].append(temp[4])
        d['PRN_NO'].append(temp[5])
        d['undefine1'].append(temp[6])
        dataframe = pd.DataFrame(d)
    return dataframe

# function to clean text string


def cleanText(text : str)->str:

    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY ,T.E.(2019 COURSE) EXAMINATION, OCT/NOV 2021','')
    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY, S.E.(2015 COURSE) EXAMINATION,MAY 2018','')
    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY','')
    text = text.replace('COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE','')
    text = text.replace('SEM.:1       ............                  .......  .......  .......  .......  .......  .......  ...  ...  ...   ... ...  ... ...','')
    text = text.replace('............CONFIDENTIAL- FOR VERIFICATION AND RECORD ONLY AT COLLEGE, NOT FOR DISTRIBUTION.......................................','')
    text = text.replace('COLLEGE    : D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE','')
    text = text.replace('BRANCH CODE: 60-T.E.(2019 PAT.)(INFORMATION TECHNOLOGY)','')
    text = text.replace('D.Y. PATIL COLLEGE OF ENGINEERING','')
    text = text.replace('BRANCH CODE: 29-S.E.(2015 PAT.)(INFORMATIOM TECHNOLOGY)','')
    text = text.replace('COURSE NAME                      ISE      ESE     TOTAL      TW       PR       OR    Tot% Crd  Grd   GP  CP  P&R ORD','')
    text = text.replace('DATE       : 23 JUL 2018','')

    #remove subject names
    text = text.replace('THEORY OF COMPUTATION','')
    text = text.replace('OPERATING SYSTEMS','')
    text = text.replace('MACHINE LEARNING','')
    text = text.replace('HUMAN COMPUTER INTERACTION','')
    text = text.replace('A DESIGN AND ANALYSIS OF ALG.','')
    text = text.replace('SEMINAR','')
    text = text.replace('HUMAN COMP. INTERACTION-LAB.','')
    text = text.replace('LABORATORY PRACTICE-I','')
    text = text.replace('OPERATING SYSTEMS LAB(TW+PR)','')
    text = text.replace('LAB(TW+PR)','')
    text = text.replace('STARTUP ECOSYSTEMS','')


    text = text.replace('CLG.: DYPP[8]','')

    text = text.replace('DATE : 06 MAY 2022','')
    text = text.replace('BRANCH CODE: 60-T.E.(2019 PAT.)(INFORMATION TECHNOLOGY)','')
    text = text.replace('FOR VERIFICATION AND RECORD ONLY AT COLLEGE, NOT FOR DISTRIBUTION','')
    text = text.replace('INFORMATION TECHNOLOGY','')
    text = text.replace('BRANCH CODE','')
    text = text.replace('CEGP010530','')
    text = text.replace('EXAMINATION','')
    text = text.replace('CONFIDENTIAL','')
    text = text.replace('....................................................................................................','')
    text = text.replace('SEM.:1','')
    text = text.replace('PAGE :-','')
    text = text.replace('NAME','')
    text = text.replace('MOTHER','')
    text = text.replace('PRN','')
    text = text.replace('SEAT NO.','')
    text = text.replace('CLG.  [8]','')
    text = text.replace('PUNE','')
    text = text.replace('PAGE  n','')
    text = text.replace('SEM.:2','')
    text = text.replace('OE       TH     [OE+TH]     TW       PR       OR    Tot% Crd  Grd  Pts   Pts','')
    text = text.replace('OE       TH     [OE+TH]     TW       PR       OR    Tot% Crd  Grd  Pts   Pts','')
    text = text.replace('DYPP','')
    text = text.replace('Grd   Crd','')
    text = text.replace('SEM. 2','')
    text = text.replace('SEM. 1','')
    text = text.replace('~','')
    text = text.replace(' .','')
    text.replace('~','nan')
    text = text.replace('*',' ')
    text = text.replace(':',' ')
    text = text.replace('-','')
    text = text.replace('SECOND YEAR SGPA','')
    text = text.replace('TOTAL CREDITS EARNED ','')
    # SECOND YEAR SGPA   8.08, TOTAL CREDITS EARNED   50
    text = text.strip()
    return text

# function to display pdf


def displayPDF(file):
    # Opening file from file path
    # with open(file, "rb") as f:
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
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
        return text


def show_uploaded_file(file):
    f = pd.read_csv(file)
    return f


#function to extract student marks from pdf
def cleanMarks(text: str,subject_codes : dict) -> dict:
    """
    This function will clean the marks from the pdf file
    ## Parameters
    text : str 
    ## return
    dictonary containing dataframes of subject wise marks
    """
    #dict to store marks
    # subject_codes = {'214441':None, '214442':None, '214443':None, '214444':None,
    #                  '214445':None, '214446':None, '214447':None, '214448':None, '214449':None, '202054A':None,
    #                  '207003':None, '214450':None, '214451':None, '214452':None, '214453':None, '214454':None, '214455':None, '214456':None, '210258A':None}

    #find subject wise marks
    for codes in subject_codes.keys():
        pattern = re.findall(fr'{codes}[A-Z]?\s+\w+[\/!#&$@ \*~]*\w*\s*\w*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\+]*\w*\s*\+*\w*\s*\+*\w*\s*\w*\+*\s*\w*\s*\+*\w*\s',text)

        d = {'subject':[],'OE':[],'TH':[],'OE_TH':[],'TW':[],'PR':[],'OR':[],'TOT':[],'CRD':[],'GRD':[],'PTS1':[],'PTS2':[]}
        for i in pattern:
            # split the string in list
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
        dataframe = dataframe.replace('nnnnnnn','--')
        subject_codes[codes] = dataframe
    return subject_codes


def concat_subjects(d : dict):
    """
        function to concat subject wise marks
        ## Parameters
        text : str
        ## return
        dataframe containing student marks of all subjects.
    """
    return pd.concat([i for i in d.values()],axis=1)


# set title
st.title('PDF TO EXCEL')
tab1, tab2, tab3, tab4 = st.tabs(
    ["📈 PDF TO Excel Convertor", "📅 Excel data Analyser", "🎢Data visualisation", "🧑‍💻PDF TO CSV"])


with tab1:
    pdf_file = st.file_uploader("", type="pdf")
    if pdf_file:
        # display document
        with st.expander("Display document"):
            displayPDF(pdf_file)

        # convert pdf to text
        text = pdfToText(pdf_file)

        # clean text file remove all puntuations
        text = cleanText(text)
        
        #dict to store subject codes
        subject_codes = st.text_input('Enter subject codes seperated by space - Ex(2144a1 2144a2 2144a3)')
        subject_codes_submit = st.button('Submit')
        if subject_codes_submit:
            subject_codes = subject_codes.split()
            subject_codes = {i:None for i in subject_codes}
            st.write(subject_codes)
            marks = cleanMarks(text,subject_codes)
            student_marks = concat_subjects(marks)
            student_marks = student_marks.replace('--',np.nan)
            student_marks = student_marks.dropna(axis=1, how='all')
            data = student_details(text)
            student_marks = pd.concat([data,student_marks],axis=1)
            st.markdown(get_table_download_link(student_marks), unsafe_allow_html=True)


with tab2:
    pdf_to_excel = st.file_uploader("", type="pdf", key=546)
    if pdf_to_excel is not None:
        st.spinner('Converting............')
        time.sleep(2)
        dfs = tabula.read_pdf(pdf_to_excel, pages='all')

        tabula.convert_into(pdf_to_excel, 'output.csv',
                            output_format="csv", pages='all')
        df2 = pd.read_csv('output.csv')
        st.dataframe(df2)

with tab3:
    csv_file = st.file_uploader("", type='csv')
    df = None
    if csv_file is not None:
        df = pd.read_csv(csv_file)
        with st.expander('Show Uploaded File'):
            st.dataframe(df)

        df['age'] = df['age'].fillna(df['age'].mean())
        df.drop('deck', inplace=True, axis=1)
        df.dropna(inplace=True)

        fig1 = px.pie(df, names='survived', title='Passenger Survival')
        st.plotly_chart(fig1)

        fig2 = px.histogram(df, x='age', nbins=30, marginal='box')
        st.plotly_chart(fig2)

        fig3 = px.scatter(df['age'])
        st.plotly_chart(fig3)
        # add another
