import streamlit as st
import pandas as pd
import plotly.express as px
import time
import numpy as np 
from itdepartment import get_table_download_link, displayPDF, pdfToText, cleanText, student_details, cleanMarks, concat_subjects

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

            # convert pdf to text
            text = pdfToText(pdf_file)

            # clean text file remove all puntuations
            text = cleanText(text)
            
            #dict to store subject codes
            subject_codes = st.text_input(label = 'Enter subject codes seperated by space - Ex(214441 214445 214447)')
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




    else:
        st.markdown(f'### Sorry for incovinience🙏,currently this feature is not available for {department} department We will add it soon. ONLY IT DEPARTMENT IS AVAILABLE NOW')