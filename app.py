import streamlit as st
import pandas as pd
import plotly.express as px
import time
import re 
import numpy as np 
from itdepartment import get_table_download_link,displayPDF, pdfToText, cleanText,student_details,cleanMarks,concat_subjects

@st.cache
def prn_no(text : str):
    pattern = re.findall(
        r'7\d{7}[A-Z]*',text
    )
    d = {'PRN-NO':[]}
    for i in pattern:
        temp = i.split()
        d['PRN-NO'].append(temp[0])
        
    dataframe = pd.DataFrame(d)
    return dataframe
    


if __name__ == "__main__":

    # set page title and icon
    try:
        st.set_page_config(
            page_title='Result Analysis',
            page_icon='📃'
        )
    except Exception as e:
        pass 

    # st.title("SPPU Result Analyser")
    st.markdown("""
        ## :outbox_tray: SPPU DATA ANALYSER: PDF TO EXCEL/CSV
       
    """)


    department = st.selectbox(
        'Select Department',
        ['IT', 'COMPUTER', 'AIDS', 'MECHANICAL', 'E&TC',
            'CIVIL', 'ELECTRICAL', 'INSTRUMENTATION']
    )

    if department == 'IT':

        pdf_file = st.file_uploader(label = "Upload file", type="pdf")
        if pdf_file:
            # display document
            with st.expander(label = "Display document"):
                displayPDF(pdf_file)

            text = pdfToText(pdf_file)
            text = cleanText(text)
            seat_no_name = student_details(text)
            student_prn_no = prn_no(text)

            student_data = pd.concat([seat_no_name,student_prn_no],axis=1)
            
            with st.expander('Display text'):
                st.write(text)
             
            
            with st.expander('Show clean data'):
                st.write(student_data)
                st.markdown(get_table_download_link(student_data), unsafe_allow_html=True)
            
            with st.expander('Show students marks'):
                subject_codes = st.text_input('Enter subject code to see subject marks(One at at time)')
                subject_codes_submit = st.button('Submit',key='one_subject_codes_submit')
                if subject_codes_submit:
                    subject_codes = subject_codes.split()
                    subject_codes = {i:None for i in subject_codes}
                    st.markdown('### Selected subjects are :')
                    st.write(subject_codes)
                    marks = cleanMarks(text,subject_codes)
                    student_marks = concat_subjects(marks)
                    student_marks = pd.concat([student_data,student_marks],axis=1)
                    st.dataframe(student_marks)
                    st.markdown(get_table_download_link(student_marks), unsafe_allow_html=True)
            
            with st.expander('Dowload Excel File'):
                subject_codes = st.text_input('Enter subject codes separated by space Example: 18IT101 18IT102')
                subject_codes_submit = st.button('Submit',key='all_subject_codes_submit')
                if subject_codes_submit:
                    subject_codes = subject_codes.split()
                    subject_codes = {i:None for i in subject_codes}
                    st.markdown('### Selected subjects are :')
                    st.write(subject_codes)
                    marks = cleanMarks(text,subject_codes)
                    student_marks = concat_subjects(marks)
                    student_marks = pd.concat([student_data,student_marks],axis=1)
                    st.markdown(get_table_download_link(student_marks), unsafe_allow_html=True)
            
            

