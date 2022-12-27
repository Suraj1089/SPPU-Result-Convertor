import csv
import streamlit as st
import pandas as pd
import plotly.express as px
import time
import re
import numpy as np
from itdepartment import get_table_download_link, displayPDF, pdfToText, cleanText, student_details, cleanMarks, concat_subjects, remove_subject_names
from itdepartment import cleanSE2015PatternMarks, cleanTE2015Marks
from st_aggrid import GridUpdateMode, DataReturnMode
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from itdepartment import dispaly_interactive
# from functionforDownloadButtons import download_button


@st.cache
def prn_no(text: str):
    """
        function to extract prn no from text
    """
    # finding prn no pattern in text
    pattern = re.findall(
        r'7\d{7}[A-Z]*', text
    )
    d = {'PRN-NO': []}
    for i in pattern:
        temp = i.split()
        d['PRN-NO'].append(temp[0])

    dataframe = pd.DataFrame(d)
    return dataframe


def mainApp():
    """
        main app
    """
    department = st.selectbox(
        'Select Department',
        ['IT', 'COMPUTER', 'AIDS', 'MECHANICAL', 'E&TC',
            'CIVIL', 'ELECTRICAL', 'INSTRUMENTATION']
    )

    if department == 'IT':
        st.write('Selected department is ', department)

        pdf_file = st.file_uploader(label="Upload Pdf File", type="pdf")
        if pdf_file:
            # display document
            with st.expander(label="Show Uploaded File"):
                displayPDF(pdf_file)

            text = pdfToText(pdf_file)
            text = cleanText(text)

            # st.write(text)
            with open('text.txt', 'w') as f:
                f.write(text)
            try:

                seat_no_name = student_details(text)
                student_prn_no = prn_no(text)

                student_data = pd.concat(
                    [seat_no_name, student_prn_no], axis=1)
            except:
                st.error(
                    "Error in extracting data from pdf. Please check the pdf file and try again.")
                return

            with st.expander('Show Students Details'):
                # remove columns with all nan values
                student_data = student_data.dropna(axis=1, how='all')
                storeStudentData = student_data.copy()
                gridOptions = dispaly_interactive(student_data)

                response = AgGrid(
                    student_data,
                    gridOptions=gridOptions,
                    enable_enterprise_modules=True,
                    update_mode=GridUpdateMode.MODEL_CHANGED,
                    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
                    fit_columns_on_grid_load=False,
                )

                df = pd.DataFrame(response["selected_rows"])

                st.spinner('Processing...')
                time.sleep(4)
                st.subheader("Filtered data will appear below 👇 ")
                st.text("")

                st.table(df)

                st.text("")

                st.markdown(get_table_download_link(
                    storeStudentData), unsafe_allow_html=True)

            with st.expander('Show Students Marks by Subject Code'):

                subject_codes = st.text_input(
                    'Enter subject code to see subject marks(One at at time)')
                subject_codes_submit = st.button(
                    'Submit', key='one_subject_codes_submit')
                if subject_codes_submit:
                    try:
                        subject_codes = subject_codes.split()
                        subject_codes = {i: None for i in subject_codes}
                        st.markdown('#### Selected subjects')
                        st.write(subject_codes)
                        # st.write(text)
                        marks = cleanMarks(text, subject_codes)
                        student_marks = concat_subjects(marks)
                        # st.write(student_marks)
                        student_marks_even_rows = student_marks.iloc[::2]
                        student_marks_odd_rows = student_marks.iloc[1::2]
                        student_marks_odd_rows.reset_index()
                        student_marks_even_rows.reset_index()
                        # st.write(student_marks_even_rows)
                        # st.write(student_marks_odd_rows)
                        duplicateStudentRows = pd.concat([student_marks_odd_rows, student_marks_even_rows],axis=1)
                        # print(duplicateStudentRows)
                        st.write(duplicateStudentRows)
                        student_marks = pd.concat(
                            [student_data, duplicateStudentRows], axis=1)

                        student_marks = student_marks.replace(
                            'nnnnnnn', np.nan)
                        student_marks = student_marks.replace('nnn', np.nan)
                        student_marks = student_marks.dropna(axis=1, how='all')
                        studentMarksStore = student_marks.copy()
                        gridOptions = dispaly_interactive(student_marks)

                        response = AgGrid(
                            student_marks,
                            gridOptions=gridOptions,
                            enable_enterprise_modules=True,
                            update_mode=GridUpdateMode.MODEL_CHANGED,
                            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
                            fit_columns_on_grid_load=False,
                        )

                        df = pd.DataFrame(response["selected_rows"])

                        st.spinner('Processing...')
                        time.sleep(4)
                        st.subheader("Filtered data will appear below 👇 ")
                        st.text("")
                        st.table(df)
                        st.text("")

                        st.markdown(get_table_download_link(
                            studentMarksStore), unsafe_allow_html=True)
                    except:
                        st.error('Please enter valid subject code')
                        st.error(
                            'Cannot convert following subject codes to excel file')
                        return

            with st.expander('Download Student marks in Excel/Csv File'):
                st.warning(
                    'Enter subject codes those are common for all student(Exclude honors courses)')
                subject_codes = st.text_input(
                    'Enter subject codes separated by space Example: 18IT101 18IT102')
                subject_codes_submit = st.button(
                    'Submit', key='all_subject_codes_submit')


                if subject_codes_submit:
                    try:
                        subject_codes = subject_codes.split()
                        subject_codes = {i: None for i in subject_codes}
                        st.markdown('### Selected subjects are :')
                        student_data = student_data.replace('nnnnnnn', np.nan)
                        st.write(subject_codes)

                        text = text.replace(' V ', '')
                        text = text.replace(' I ', '')
                        text = text.replace(' II ', '')
                        text = text.replace(' III ', '')
                        with open('mmm.txt', 'w') as mm:
                            mm.write(text)
                        marks = cleanMarks(text, subject_codes)
                        student_marks = concat_subjects(marks)
                        student_marks = pd.concat(
                            [student_data, student_marks], axis=1)
                        student_marks = student_marks.replace(
                            'nnnnnnn', np.nan)
                        student_marks = student_marks.replace('nnn', np.nan)
                        student_marks = student_marks.replace('nan', np.nan)
                        student_marks = student_marks.replace('nnnn', np.nan)

                        student_marks = student_marks.dropna(axis=1, how='all')

                        # st.write(student_marks)
                        st.markdown(get_table_download_link(
                            student_marks), unsafe_allow_html=True)
                    except:
                        st.error('Please enter valid subject codes')
                        st.error(
                            'Cannot convert following subject codes to excel file')
                        return

    else:
        st.write('selected department is ', department)
        st.warning(
            'Enter subject names as present in pdf file to clean data')


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
        ## :outbox_tray: SPPU DATA ANALYSER
    """)

    # main App
    mainApp()
