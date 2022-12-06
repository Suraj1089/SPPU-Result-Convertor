import csv
import streamlit as st
import pandas as pd
import plotly.express as px
import time
import re
import numpy as np
from itdepartment import get_table_download_link, displayPDF, pdfToText, cleanText, student_details, cleanMarks, concat_subjects, remove_subject_names
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

        pdf_file = st.file_uploader(label="Upload Pdf File", type="pdf")
        if pdf_file:
            # display document
            with st.expander(label="Show Uploaded File"):
                displayPDF(pdf_file)

            text = pdfToText(pdf_file)
            text = cleanText(text)
            text = remove_subject_names(text)
            try:

                seat_no_name = student_details(text)
                student_prn_no = prn_no(text)

                student_data = pd.concat(
                    [seat_no_name, student_prn_no], axis=1)
            except:
                st.error(
                    "Error in extracting data from pdf. Please check the pdf file and try again.")
                return
            # with st.expander('Display text'):
            #     st.write(text)

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

                st.subheader("Filtered data will appear below 👇 ")
                st.text("")

                st.table(df)

                st.text("")

                st.markdown(get_table_download_link(
                    storeStudentData), unsafe_allow_html=True)

            with st.expander('Show Students Marks'):

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
                        marks = cleanMarks(text, subject_codes)
                        student_marks = concat_subjects(marks)
                        student_marks = pd.concat(
                            [student_data, student_marks], axis=1)
                        st.success('Done!....')
                        # remove columns with all nan values
                        student_marks = student_marks.replace(
                            'nnnnnnn', np.nan)
                        student_marks = student_marks.replace('nnn', np.nan)
                        student_marks = student_marks.dropna(axis=1, how='all')
                        st.dataframe(student_marks)
                        st.markdown(get_table_download_link(
                            student_marks), unsafe_allow_html=True)
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
                        # replace nnnnnnn with np.nan
                        student_data = student_data.replace('nnnnnnn', np.nan)
                        # remove columns with all nan values
                        # student_data = student_data.dropna(axis=1, how='all')
                        st.write(subject_codes)

                        # remove subject names from text
                        # subject_names = st.text_input(
                        # 'Enter subject names separated by space same as in pdf Example: Data Structure and Algorithms Computer Organization and Architecture')
                        # subject_names = subject_names.split()
                        # text = remove_subject_names(text, subject_names)
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
        st.warning(
            'This app is working only for IT department(SELECT IT DEPARTMENT)')


def drop_empty_colums():
    """
        function to drop empty columns
    """
    with st.expander('Drop Empty columns from Excel file'):
        csv_file = st.file_uploader(label="Upload csv file")

        if csv_file is not None:
            if csv_file.type == 'text/csv':
                df = pd.read_csv(csv_file)

                # replace n with np.nan
                df = df.replace('nnnnnnn', np.nan)
                df = df.replace('nnn', np.nan)
                df = df.replace('nan', np.nan)
                df = df.dropna(axis=1, how='all')
                # split the column value those contains / and take first value

                st.markdown('### Dataframe after dropping empty columns')
                # remove columns with all nan values

                st.dataframe(df)
                st.markdown(get_table_download_link(
                    df), unsafe_allow_html=True)
            elif csv_file.type == 'excel':
                df = pd.read_excel(csv_file)
                df = df.replace('nnnnnnn', np.nan)
                df = df.replace('nnn', np.nan)
                df = df.replace('nan', np.nan)
                df = df.dropna(axis=1, how='all')
                st.markdown('### Dataframe after dropping empty columns')
                st.dataframe(df)
                st.markdown(get_table_download_link(
                    df), unsafe_allow_html=True)


def datavisualization():
    with st.expander('Data Analysis'):
        st.warning(
            'Data visualization is supported for only numerical data Make sure that the columns to visualize are numerical')
        csv_file = st.file_uploader(label="Upload csv/excel file")
        if csv_file is not None:
            df = None
            if csv_file.type == 'text/csv':
                df = pd.read_csv(csv_file)
                df = df.replace('nnnnnnn', np.nan)
                df = df.replace('nnn', np.nan)
                df = df.replace('nan', np.nan)
                df = df.dropna(axis=1, how='all')
                st.dataframe(df)
                st.write(df.dtypes)
                st.markdown(get_table_download_link(
                    df), unsafe_allow_html=True)
            elif csv_file.type == 'excel':
                df = pd.read_excel(csv_file)
                df = df.replace('nnnnnnn', np.nan)
                df = df.replace('nnn', np.nan)
                df = df.replace('nan', np.nan)
                df = df.dropna(axis=1, how='all')
                st.dataframe(df)
                st.markdown(get_table_download_link(
                    df), unsafe_allow_html=True)

            # if df is not None:

            #     columns = st.multiselect('Select columns to visualize',df.columns)
            #     if columns:
            #         st.markdown('### Selected columns')
            #         st.write(columns)
            #         for i in columns:
            #             if df[i].dtype == 'int64' or df[i].dtype == 'float64':
            #                 fig = px.histogram(df,x=i)
            #                 st.plotly_chart(fig)
            #             else:
            #                 st.error('Cannot visualize non numerical data')
            #                 return
            #     else:
            #         st.error('Please select columns to visualize')
            #         return


def input_dataframe_column_names():
    """
        function to change column names from file 
    """
    with st.expander('Rename Column Names'):
        csv_file = st.file_uploader(
            label="Upload csv/excel file", key='input_dataframe_column_names')
        if csv_file is not None:
            st.write(csv_file.type)
            df = None
            if csv_file.type == 'text/csv':
                df = pd.read_csv(csv_file)
            elif csv_file.type == 'excel':
                df = pd.read_excel(csv_file)
            elif csv_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                df = pd.read_excel(csv_file)
            else:
                st.error('Upload a valid csv/excel file')
                return

            # store length of columns
            initial_df_columns_length = len(df.columns)
            if df is not None:
                st.markdown('##### Show Initial column names')
                st.write(list(df.columns))
                st.markdown('### Enter column names separated by space')
                column_names = st.text_input('Enter column names')
                column_names_submit = st.button('Submit')
                if column_names_submit:
                    try:
                        column_names = column_names.split()
                        try:
                            df.columns = column_names
                        except:
                            st.error(
                                f'Initial file contains {initial_df_columns_length} columns and you entered {len(column_names)} column names')
                            return
                        st.markdown('##### columns names after renaming')
                        st.write(list(df.columns))
                        st.markdown('### Dataframe after renaming columns')
                        st.success('Done..........')
                        st.dataframe(df)
                        st.markdown(get_table_download_link(
                            df), unsafe_allow_html=True)
                    except:
                        st.error(
                            'Please enter valid column names(all column names should be unique)')
                        return


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
        # :outbox_tray: SPPU DATA ANALYSER: PDF TO EXCEL/CSV
    """)

    # main App
    mainApp()

    # drop empty columns
    drop_empty_colums()

    # change column names
    input_dataframe_column_names()

    # data visualization
    datavisualization()
