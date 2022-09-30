import streamlit as st
import pandas as pd
import plotly.express as px  
import time
from itdepartment import get_table_download_link,cleanText,displayPDF,pdfToText,show_uploaded_file


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
# multiple tabls in header
tab1, tab2 = st.tabs(["📈 EXCEL/CSV DATA ANALYSIS", "🧑‍💻PDF TO CSV/Excel"])

department = st.sidebar.selectbox(
    'Select Department',
    ['IT', 'COMPUTER', 'AIDS', 'MECHANICAL', 'E&TC',
        'CIVIL', 'ELECTRICAL', 'INSTRUMENTATION']
)
with tab1:
    if department == 'IT':
        if department not in st.session_state:
            st.session_state.department = 'COMPUTER'
            with tab1:
                # select department
                department_year = st.sidebar.selectbox('Select Year',
                                                    ['SE', 'TE', 'BE']
                                                    )
                st.write(f"selected department is {department}")
                st.write(f"selected branch is {department_year}")
                uploaded_excel_file = st.sidebar.file_uploader(
                    "", type=['csv', 'xlsx','pdf'])
                if uploaded_excel_file is not None:
                    file_container = st.expander('See uploaded data')
                    excel_file = pd.read_csv(uploaded_excel_file)
                    uploaded_excel_file.seek(0)
                    file_container.write(excel_file)

        



    elif department == 'COMPUTER':
        if department not in st.session_state:
            st.session_state.department = 'COMPUTER'
        with tab1:
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
        with tab1:
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
        with tab1:
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
        with tab1:
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
        with tab1:
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
        with tab1:
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
        with tab1:
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
        with tab1:
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



with tab2:
    st.write("hello")