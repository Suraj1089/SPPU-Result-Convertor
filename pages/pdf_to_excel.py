import streamlit as st 
import pandas as pd
import numpy as np 
import PyPDF2 
from io import StringIO
import base64
import re 
import plotly.express as px 
# import seaborn as sns 
import matplotlib.pyplot as plt 

st.set_page_config(
    page_title='Result Analysis',
    page_icon='📃'
)

# --- LOAD CSS, PDF & PROFIL PIC ---
with open('css/main.css') as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


#dowload file
def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="SeatNo.csv">Download Excel file</a>'
    return href

#find name,seat_no,prn_no

def seat_no(text):
    pattern = re.findall(r'[ST]\w{9}\s*\w*\s*\w*\s*\w*\s*\w*\w*\s*\w*\s*\w*\s*\w*\s*',text)
# print(len(pattern))
    d = {'seat_no':[],'name':[],'mother_name':[],'PRN_NO':[]}
#0-seat no 1-2-3-name 4-mother_name 5-prn
    for i in pattern:
        temp = i.split()
        temp.pop()
        temp.pop()
        if len(temp)==5:
            temp.append('Nan')
        d['seat_no'].append(temp[0])
        d['name'].append(temp[1]+' '+temp[2]+' '+temp[3])
        d['mother_name'].append(temp[4])
        d['PRN_NO'].append(temp[5])
        dataframe = pd.DataFrame(d)
    return dataframe
        # datafrmae.to_csv('seat_no_name_monther_name.csv',header=datafrmae.columns)

#function to clean text string
def cleanText(text : str) -> str:
    type(text)
    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY, S.E.(2015 COURSE) EXAMINATION,MAY 2018','')
    text = text.replace('COLLEGE    : D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE','')
    text = text.replace('BRANCH CODE: 29-S.E.(2015 PAT.)(INFORMATIOM TECHNOLOGY)','')
    text = text.replace('DATE       : 23 JUL 2018','')
    text = text.replace('....................................................................................................','')
    text = text.replace('SEM.:1','')
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
    text = text.replace('-','n')
    text = text.replace('SECOND YEAR SGPA','')
    text = text.replace('TOTAL CREDITS EARNED ','')
    # SECOND YEAR SGPA   8.08, TOTAL CREDITS EARNED   50
    text = text.strip()
    return text 

#function to display pdf
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
    with open('final_txt.txt','w') as f:
        for i in range(0,no_of_pages):
            pagObj = pdfreader.getPage(i)
            f.write(pagObj.extractText())
    with open('final_txt.txt','r') as f:
        text = f.read()
        return text 


def show_uploaded_file(file):
    f = pd.read_csv(file)
    return f

#set title
st.title('PDF TO EXCEL')
tab1, tab2,tab3,tab4 = st.tabs(["📈 PDF TO Excel Convertor", "📅 Excel data Analyser","🎢Data visualisation","🧑‍💻PDF TO CSV"])


with tab1:
    pdf_file = st.file_uploader("", type="pdf")
    if pdf_file:
        # display document
        with st.expander("Display document"):
            displayPDF(pdf_file)

        # convert pdf to text 
        text = pdfToText(pdf_file)

        #clean text file remove all puntuations
        text = cleanText(text)

        with st.expander('show data'):
            student_details = seat_no(text)
            st.dataframe(student_details)
            
       
        data = seat_no(text)
        # data = get_table_download_link(data)
        st.markdown(get_table_download_link(data), unsafe_allow_html=True)


with tab2:
    excel_file = st.file_uploader("", type="excel")
    
with tab3:
    csv_file = st.file_uploader("", type='csv')
    df = None
    if csv_file is not None:
        df = pd.read_csv(csv_file)
        with st.expander('Show Uploaded File'):
                st.dataframe(df)
             

        df['age'] = df['age'].fillna(df['age'].mean())
        df.drop('deck',inplace=True,axis=1)
        df.dropna(inplace=True)


                
        fig1 = px.pie(df, names='survived', title='Passenger Survival')
        st.plotly_chart(fig1)

        fig2 = px.histogram(df, x='age', nbins=30, marginal='box')
        st.plotly_chart(fig2)

        fig3 = px.scatter(df['age'])
        st.plotly_chart(fig3)
        #add another