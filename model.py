# import streamlit as st 
# import tabula
# import pandas as pd
# import numpy as np 
# import PyPDF2 
# from io import StringIO
# import base64

# def cleanText(text : str) -> str:
#     type(text)
#     text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY, S.E.(2015 COURSE) EXAMINATION,MAY 2018','')
#     text = text.replace('COLLEGE    : D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE','')
#     text = text.replace('BRANCH CODE: 29-S.E.(2015 PAT.)(INFORMATIOM TECHNOLOGY)','')
#     text = text.replace('DATE       : 23 JUL 2018','')
#     text = text.replace('....................................................................................................','')
#     text = text.replace('SEM.:1','')
#     text = text.replace('SEM.:2','')
#     text = text.replace('OE       TH     [OE+TH]     TW       PR       OR    Tot% Crd  Grd  Pts   Pts','')
#     text = text.replace('OE       TH     [OE+TH]     TW       PR       OR    Tot% Crd  Grd  Pts   Pts','')
#     text = text.replace('DYPP','')
#     text = text.replace('Grd   Crd','')
#     text = text.replace('SEM. 2','')
#     text = text.replace('SEM. 1','')
#     text = text.replace('~','')
#     text = text.replace(' .','')
#     text.replace('~','nan')
#     text = text.replace('*',' ')
#     text = text.replace(':',' ')
#     text = text.replace('-','n')
#     text = text.replace('SECOND YEAR SGPA','')
#     text = text.replace('TOTAL CREDITS EARNED ','')
#     # SECOND YEAR SGPA   8.08, TOTAL CREDITS EARNED   50
#     text = text.strip()
#     return text 

# def displayPDF(file):
#   # Opening file from file path
#   # with open(file, "rb") as f:
#   base64_pdf = base64.b64encode(file.read()).decode('utf-8')
#   # Embedding PDF in HTML
#   pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
#   # Displaying File
#   st.markdown(pdf_display, unsafe_allow_html=True)

# @st.cache
# def pdfToText(path):
#     pdfreader = PyPDF2.PdfFileReader(path)
#     no_of_pages = pdfreader.numPages
#     with open('final_txt.txt','w') as f:
#         for i in range(0,no_of_pages):
#             pagObj = pdfreader.getPage(i)
#             f.write(pagObj.extractText())
#     with open('final_txt.txt','r') as f:
#         text = f.read()
#         return text 
        


# st.title('PDF TO EXCEL')


# with st.sidebar:
#     st.title("PDF to Text")
#     textOutput = st.selectbox(
#         "How do you want your output data?",
#         ('One text file (.txt)', 'Text file per page (ZIP)'))

# pdf_file = st.file_uploader("Upload PDF file", type="pdf")
# if pdf_file:
#     # display document
#     with st.expander("Display document"):
#         displayPDF(pdf_file)

# show_text = st.button('show text')
# if show_text:
#     text = pdfToText(pdf_file)
#     st.write(type(text))
#     st.markdown("""
    
#        Hello
#     """)

#     text = cleanText(text)
#     st.write(text)
   
    
import base64
import pandas as pd 
import streamlit as st 
def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="SeatNo.csv">Download Excel file</a>'
    return href

df = pd.read_csv('datasets/214443.csv')
st.markdown(get_table_download_link(df), unsafe_allow_html=True)
st.button('Download csv',on_click=get_table_download_link,args=[df,])