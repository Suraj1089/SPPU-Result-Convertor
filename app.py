import streamlit as st 
import pandas as pd 


st.title("pdf to csv convertor")

department = st.selectbox("CHOOSE DEPARTMENT :",options=['IT','CS','E&TC','MECHANICAL','CIVIL'])
year = st.selectbox("CHOOSE YEAR :",options=['FE','SE','TE','BE'])

pdf_file = st.file_uploader("")

button = st.button('CONVERT')

if button:
    d = pd.read_csv('s12.csv')
    st.dataframe(d)
