import streamlit as st
import pandas as pd
import time
import re
import numpy as np
from itdepartment import getTabledownloadLink, displayPDF, pdfToText, cleanText, studentDetails, cleanMarks
from st_aggrid import GridUpdateMode, DataReturnMode
from st_aggrid import AgGrid
from itdepartment import displayInteractive


@st.cache
def concat_subjects(d: dict):
    """
        function to concat subject wise marks
    """
    return pd.concat([i for i in d.values()], axis=1)


@st.cache
def cleanTextRe(text: str) -> str:
    text = re.sub(r'^[a-zA-Z]{2}', '', text)
    return text


@st.cache
def extractPrnNo(text: str):
    """
        function to extract prn no from text
    """
    # PRN NO pattern
    pattern = re.findall(
        r'7\d{7}[A-Z]*', text
    )
    d = {'PRN-NO': []}
    for i in pattern:
        temp = i.split()
        d['PRN-NO'].append(temp[0])

    dataframe = pd.DataFrame(d)
    return dataframe


def App():

    st.markdown("""
        ## :outbox_tray: SPPU DATA ANALYSER
    """)

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
            with open('text.txt', 'w') as f:
                f.write(text)

            # st.write(text)
            try:

                seat_no_name = studentDetails(text)
                student_prn_no = extractPrnNo(text)

                student_data = pd.concat(
                    [seat_no_name, student_prn_no], axis=1)
            except:
                st.error(
                    "Error in extracting data from pdf. Please check the pdf file and try again.")
                return

            with st.expander('Show Students Details'):
                student_data = student_data.dropna(axis=1, how='all')
                storeStudentData = student_data.copy()
                gridOptions = displayInteractive(student_data)

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

                st.markdown(getTabledownloadLink(
                    storeStudentData), unsafe_allow_html=True)

            with st.expander('Show Students Marks by Subject Code'):

                # text = cleanTextRe(text)
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
                        st.spinner('Processing...')
                        pattern = r'[A-Z]\w*[A-Z]'
                        text = cleanTextRe(text)
                        text = re.sub(pattern, '', text)
                        # st.write(text)
                        try:
                            marks = cleanMarks(text, subject_codes)
                        except:
                            # st.write(text[:5000])
                            st.error(
                                'Error in extracting marks. Please check the pdf file and try again.@cleanMarks')
                            return
                        
                        try:
                            student_marks = concat_subjects(marks)
                            student_marks = pd.concat(
                                [student_data, student_marks], axis=1)
                        except:
                            st.error(
                                'Error in extracting marks. Please check the pdf file and try again.@concat_subjects')
                            return


                        st.success('Done!....')
                        # remove columns with all nan values
                        student_marks = student_marks.replace(
                            'nnnnnnn', np.nan)
                        student_marks = student_marks.replace(
                            'nnnnnnn', np.nan)
                        student_marks = student_marks.replace('nnn', np.nan)
                        student_marks = student_marks.replace('nan', np.nan)
                        student_marks = student_marks.replace('nnnn', np.nan)

                        # student_marks = student_marks.replace('nnn', np.nan)
                        student_marks = student_marks.dropna(axis=1, how='all')
                        studentMarksStore = student_marks.copy()
                        gridOptions = displayInteractive(student_marks)

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

                        st.markdown(getTabledownloadLink(
                            studentMarksStore), unsafe_allow_html=True)
                    except:
                        st.error('Please enter valid subject code or cannot convert this marks')
                        
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
                        st.spinner('Processing...')
                        text = cleanTextRe(text)
                        pattern = r'[A-Z]\w*[A-Z]'
                        text = re.sub(pattern, '', text)
                        try:
                            marks = cleanMarks(text, subject_codes)
                        except:
                            st.error(
                                'Error in extracting marks. Please check the pdf file and try again.@cleanMarks')
                            return
                        
                        try:

                            student_marks = concat_subjects(marks)
                            student_marks = pd.concat(
                                [student_data, student_marks], axis=1)
                        except:
                            st.error(
                                'Error in extracting marks. Please check the pdf file and try again.@concat_subjects')
                            return

                        student_marks = student_marks.replace(
                            'nnnnnnn', np.nan)
                        student_marks = student_marks.replace('nnn', np.nan)
                        student_marks = student_marks.replace('nan', np.nan)
                        student_marks = student_marks.replace('nnnn', np.nan)

                        student_marks = student_marks.dropna(axis=1, how='all')

                        st.markdown(getTabledownloadLink(
                            student_marks), unsafe_allow_html=True)
                    except:
                        st.error(
                            'Please enter valid subject codes OR Cannot convert following subject codes to excel file')
                        return

    else:
        st.write('selected department is ', department)


if __name__ == "__main__":

    # set page title and icon
    try:
        st.set_page_config(
            page_title='Result Analysis',
            page_icon='📃'
        )
    except Exception as e:
        pass

    App()
