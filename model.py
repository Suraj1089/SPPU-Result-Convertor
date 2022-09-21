import streamlit as st 
import tabula
import pandas as pd
import numpy as np 

st.title('pdf to excel converter')


file_name = st.sidebar.text_input('file input: ')
pdf_file = st.sidebar.file_uploader('upload file :')

if file_name:
    if pdf_file is not None:
        df = tabula.read_pdf('{0}.pdf'.format(file_name),pages='all')
        tabula.convert_into('{0}.pdf'.format(file_name),'data1.csv',output_format='csv',pages='all')
        data = pd.DataFrame(df[0])

        st.write("your data is ...................")
        st.dataframe(data)
        data.to_excel('outputsam.xlsx')

else:
    st.write('please input file name and pdf file')