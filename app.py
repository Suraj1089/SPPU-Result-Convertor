import streamlit as st
import pandas as pd
import plotly.express as px
import time
import numpy as np 
from itdepartment import get_table_download_link, displayPDF, pdfToText, cleanText, student_details, cleanMarks, concat_subjects

if __name__ == "__main__":

    # set page title and icon
    st.set_page_config(
        page_title='Result Analysis',
        page_icon='📃'
    )

    # st.title("SPPU Result Analyser")
    st.markdown("""
        ## :outbox_tray: SPPU DATA ANALYSER: PDF to Excel
        [![GitHub](https://img.shields.io/twitter/url?label=Github&logo=GitHub&style=social&url=https%3A%2F%2Fgithub.com%2Fnainiayoub)](https://github.com/Suraj1089/SPPU-Result-Convertor)
        
    """)

    department = st.selectbox(
        'Select Department',
        ['IT', 'COMPUTER', 'AIDS', 'MECHANICAL', 'E&TC',
            'CIVIL', 'ELECTRICAL', 'INSTRUMENTATION']
    )

    if department == 'IT':

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
            subject_codes = st.text_input('Enter subject codes seperated by space - Ex(214441 214445 214447)')
            subject_codes_submit = st.button('Submit')
            if subject_codes_submit:
                subject_codes = subject_codes.split()
                subject_codes = {i:None for i in subject_codes}
                st.markdown('### Selected subjects are :')
                st.write(subject_codes)
                marks = cleanMarks(text,subject_codes)
                student_marks = concat_subjects(marks)
                # st.dataframe(student_marks)
                student_marks = student_marks.replace('--',np.nan)
                student_marks = student_marks.replace('nnn',np.nan)
                student_marks = student_marks.dropna(axis=1, how='all')
                st.markdown('### Generated Excel Sheet')
                # st.dataframe(student_marks)
                data = student_details(text)
                student_marks = pd.concat([data,student_marks],axis=1)
                st.markdown(get_table_download_link(student_marks), unsafe_allow_html=True)



    elif department == 'COMPUTER':
        if department not in st.session_state:
            st.session_state.department = 'COMPUTER'
        
            # select department
            department_year = st.sidebar.selectbox('Select Year',
                                                ['SE', 'TE', 'BE']
                                                )
            st.write(f"selected department is {department}")
            st.write(f"selected branch is {department_year}")
            uploaded_excel_file = st.sidebar.file_uploader(
                "", type=['csv', 'xlsx'])
            if uploaded_excel_file is not None:
                file_container = st.expander('See uploaded data')
                excel_file = pd.read_csv(uploaded_excel_file)
                uploaded_excel_file.seek(0)
                file_container.write(excel_file)

    elif department == 'AIDS':
        if department not in st.session_state:
            st.session_state.department = 'AIDS'
    
            # select department
            department_year = st.sidebar.selectbox('Select Year',
                                                ['SE', 'TE', 'BE']
                                                )
            st.write(f"selected department is {department}")
            st.write(f"selected branch is {department_year}")
            uploaded_excel_file = st.sidebar.file_uploader(
                "", type=['csv', 'xlsx'])
            if uploaded_excel_file is not None:
                file_container = st.expander('See uploaded data')
                excel_file = pd.read_csv(uploaded_excel_file)
                uploaded_excel_file.seek(0)
                file_container.write(excel_file)


    elif department == 'MECHANICAL':
        if department not in st.session_state:
            st.session_state.department = 'MECHANICAL'
    
            # select department
            department_year = st.sidebar.selectbox('Select Year',
                                                ['SE', 'TE', 'BE']
                                                )
            st.write(f"selected department is {department}")
            st.write(f"selected branch is {department_year}")
            uploaded_excel_file = st.sidebar.file_uploader(
                "", type=['csv', 'xlsx'])
            if uploaded_excel_file is not None:
                file_container = st.expander('See uploaded data')
                excel_file = pd.read_csv(uploaded_excel_file)
                uploaded_excel_file.seek(0)
                file_container.write(excel_file)


    elif department == 'E&TC':
        if department not in st.session_state:
            st.session_state.department = 'E&TC'
    
            # select department
            department_year = st.sidebar.selectbox('Select Year',
                                                ['SE', 'TE', 'BE']
                                                )
            st.write(f"selected department is {department}")
            st.write(f"selected branch is {department_year}")
            uploaded_excel_file = st.sidebar.file_uploader(
                "", type=['csv', 'xlsx'])
            if uploaded_excel_file is not None:
                file_container = st.expander('See uploaded data')
                excel_file = pd.read_csv(uploaded_excel_file)
                uploaded_excel_file.seek(0)
                file_container.write(excel_file)

    elif department == 'CIVIL':
        if department not in st.session_state:
            st.session_state.department = 'CIVIL'
        
            # select department
            department_year = st.sidebar.selectbox('Select Year',
                                                ['SE', 'TE', 'BE']
                                                )
            st.write(f"selected department is {department}")
            st.write(f"selected branch is {department_year}")
            uploaded_excel_file = st.sidebar.file_uploader(
                "", type=['csv', 'xlsx'])
            if uploaded_excel_file is not None:
                file_container = st.expander('See uploaded data')
                excel_file = pd.read_csv(uploaded_excel_file)
                uploaded_excel_file.seek(0)
                file_container.write(excel_file)


    elif department == 'ELECTRICAL':
        if department not in st.session_state:
            st.session_state.department = 'ELECTRICAL'

            # select department
            department_year = st.sidebar.selectbox('Select Year',
                                                ['SE', 'TE', 'BE']
                                                )
            st.write(f"selected department is {department}")
            st.write(f"selected branch is {department_year}")
            uploaded_excel_file = st.sidebar.file_uploader(
                "", type=['csv', 'xlsx'])
            if uploaded_excel_file is not None:
                file_container = st.expander('See uploaded data')
                excel_file = pd.read_csv(uploaded_excel_file)
                uploaded_excel_file.seek(0)
                file_container.write(excel_file)

    elif department == 'INSTRUMENTATION':
        if department not in st.session_state:
            st.session_state.department = 'INSTRUMENTATION'
    
            # select department
            department_year = st.sidebar.selectbox('Select Year',
                                                ['SE', 'TE', 'BE']
                                                )
            st.write(f"selected department is {department}")
            st.write(f"selected branch is {department_year}")
            uploaded_excel_file = st.sidebar.file_uploader(
                "", type=['csv', 'xlsx'])
            if uploaded_excel_file is not None:
                file_container = st.expander('See uploaded data')
                excel_file = pd.read_csv(uploaded_excel_file)
                uploaded_excel_file.seek(0)
                file_container.write(excel_file)

    elif department == 'FIRST YEAR':
        if department not in st.session_state:
            st.session_state.department = 'FIRST YEAR'
        
            # select department
            department_year = st.sidebar.selectbox('Select Year',
                                                ['SE', 'TE', 'BE']
                                                )
            st.write(f"selected department is {department}")
            st.write(f"selected branch is {department_year}")
            uploaded_excel_file = st.sidebar.file_uploader(
                "", type=['csv', 'xlsx'])
            if uploaded_excel_file is not None:
                file_container = st.expander('See uploaded data')
                excel_file = pd.read_csv(uploaded_excel_file)
                uploaded_excel_file.seek(0)
                file_container.write(excel_file)



