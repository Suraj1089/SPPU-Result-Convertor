import streamlit as st 
import tabula
import pandas as pd
import numpy as np 
import PyPDF2 
from io import StringIO
import base64

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
        
@st.cache(suppress_st_warning=True)
def showTextFile(path):
    text_file = F'<iframe src="data:application/pdf;base64,{path}" width="700" height="1000" type="application/pdf"></iframe>'
  # Displaying File
    st.markdown(text_file, unsafe_allow_html=True)

# @st.cache
# def convert_pdf_to_txt_file(path):
#     texts = []
#     rsrcmgr = PDFResourceManager()
#     retstr = StringIO()
#     laparams = LAParams()
#     device = TextConverter(rsrcmgr, retstr, laparams=laparams)
#     # fp = open(path, 'rb')
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
    
#     file_pages = PDFPage.get_pages(path)
#     nbPages = len(list(file_pages))
#     for page in PDFPage.get_pages(path):
#       interpreter.process_page(page)
#       t = retstr.getvalue()
#     # text = retstr.getvalue()

#     # fp.close()
#     device.close()
#     retstr.close()
#     return t, nbPages

st.title('pdf to exel')


with st.sidebar:
    st.title("PDF to Text")
    textOutput = st.selectbox(
        "How do you want your output data?",
        ('One text file (.txt)', 'Text file per page (ZIP)'))

pdf_file = st.file_uploader("Load your PDF file", type="pdf")
if pdf_file:
    # display document
    with st.expander("Display document"):
        displayPDF(pdf_file)

show_text = st.button('show text')
if show_text:
   p = st.write(pdfToText(pdf_file))
   showTextFile(p)
    