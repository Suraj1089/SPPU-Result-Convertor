import streamlit as st 
import pandas as pd 
# import numpy as np 
# import seaborn as sns 
# import matplotlib.pyplot as plt 
import plotly.express as px # interactive plotting
# import re       # clean string
# import PyPDF2  # convert pdf to text 
import time 
import plotly.express as px 


#set page title and icon
st.set_page_config(
    page_title='Result Analysis',
    page_icon='📃'
)
# st.title("SPPU Result Analyser")
st.markdown("""
    ## :outbox_tray: SPPU DATA ANALYSER: PDF to Excel
    [![GitHub](https://img.shields.io/twitter/url?label=Github&logo=GitHub&style=social&url=https%3A%2F%2Fgithub.com%2Fnainiayoub)](https://github.com/Suraj1089/SPPU-Result-Convertor)
    
""")
#multiple tabls in header
tab1, tab2,tab3,tab4 = st.tabs(["📈 PDF TO Excel Convertor", "📅 Excel data Analyser","🎢Data visualisation","🧑‍💻PDF TO CSV"])


with tab1:
    st.sidebar.write('Upload CSV or EXCEL file')
    uploaded_excel_file = st.sidebar.file_uploader("",type=['csv','xlsx'])
    if uploaded_excel_file is not None:
        file_container = st.expander('See uploaded data')
        excel_file = pd.read_csv(uploaded_excel_file)
        uploaded_excel_file.seek(0)
        file_container.write(excel_file)

        with st.expander('show pie chart'):
            with st.spinner("Converting..."):
                time.sleep(5)
            st.success("Done!")

            labels = list(excel_file['GRD.13'].unique())
            sizes = list(excel_file['GRD.13'].value_counts())
            p = px.pie(sizes,labels)
            st.plotly_chart(p)
            
        
        with st.expander('show bar'):
            st.plotly_chart(px.bar(excel_file['PTS2.12']))


with tab2:
    st.write("hello")
# if tab2:
#     with tab2:
#         st.sidebar.write('Upload CSV or EXCEL file to Analyse')
#         # excel_file = st.sidebar.file_uploader("",type=['csv','xlsx'])
#         # if excel_file is not None:
#         #     df = pd.read_csv(excel_file)
#         #     st.write(df)




