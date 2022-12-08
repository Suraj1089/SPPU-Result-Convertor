import streamlit as st 
import PyPDF2

def app():
    # st.warning('This feature is under maintenance mode try after some time')
    st.title('PDF to Word Converter')
    uploadedFile = st.file_uploader("Choose a PDF file", type="pdf")
    if uploadedFile is not None:
        pdfReader = PyPDF2.PdfFileReader(uploadedFile)
        pageObj = pdfReader.getPage(0)
        text = pageObj.extractText()
        
        st.write(text)
        


app()