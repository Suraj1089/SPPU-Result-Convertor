import streamlit as st 
import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.express as px #interactive plotting
import re       #clean string
import PyPDF2  #convert pdf to text 


#set page title and icon
st.set_page_config(
    page_title='Result Analysis',
    page_icon='📃'
)
st.title("Result Analysis")
st.markdown("""
    ## :outbox_tray: Text data extractor: PDF to Text
    [![Twitter](https://img.shields.io/twitter/url?label=Twitter&style=social&url=https%3A%2F%2Ftwitter.com%2Fnainia_ayoub)](https://www.twitter.com/nainia_ayoub)
    [![Linkedin](https://img.shields.io/twitter/url?label=Linkedin&logo=linkedin&style=social&url=https%3A%2F%2Fwww.linkedin.com%2Fin%2Fayoub-nainia%2F%3Flocale%3Den_US)](https://www.linkedin.com/in/ayoub-nainia/?locale=en_US)
    [![GitHub](https://img.shields.io/twitter/url?label=Github&logo=GitHub&style=social&url=https%3A%2F%2Fgithub.com%2Fnainiayoub)](https://github.com/nainiayoub)
    Before extracting information from a document, we have to extract text data first. 
    Hence, this PDF text data extractor was created.
""")
#multiple tabls in header
tab1, tab2 = st.tabs(["📈 PDF TO Excel Convertor", "🗃 Excel data Analyser"])


#add values in tab1
with tab1:
    st.write("Drag or Drop pdf file to Convert")
    department = st.sidebar.selectbox("CHOOSE DEPARTMENT :",options=['IT','CS','E&TC','MECHANICAL','CIVIL'])
    year = st.sidebar.selectbox("CHOOSE YEAR :",options=['FE','SE','TE','BE'])

    pdf_file = st.sidebar.file_uploader("",type='pdf')

    button = st.sidebar.button('PREVIEW')
    file_name = None 
    if button:
        #check file is selected or not
        if pdf_file is None:
            st.write("Please select a file")
        else:
            st.write("pdf is selected")
            file_name = st.write(pdf_file.name)
            if 'pdf_file' not in st.session_state:
                st.session_state['pdf_file'] = pdf_file
            
            
        st.button("DOWNLOAD")



with tab2:
    d = pd.read_csv('s12.csv')
    st.dataframe(d)
    st.table(d.columns)
    st.write("tab2 is pressed")

