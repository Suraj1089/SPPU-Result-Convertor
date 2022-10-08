import csv
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
    
def mainApp():
    
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
            try:

                seat_no_name = student_details(text)
                student_prn_no = prn_no(text)

                student_data = pd.concat([seat_no_name,student_prn_no],axis=1)
            except:
                st.error("Error in extracting data from pdf. Please check the pdf file and try again.")
                return
            # with st.expander('Display text'):
            #     st.write(text)
             
            
            with st.expander('Show Students Details'):
                st.write(student_data)
                st.markdown(get_table_download_link(student_data), unsafe_allow_html=True)
            
            with st.expander('Show students marks'):
                subject_codes = st.text_input('Enter subject code to see subject marks(One at at time)')
                subject_codes_submit = st.button('Submit',key='one_subject_codes_submit')
                if subject_codes_submit:
                    try:
                        subject_codes = subject_codes.split()
                        subject_codes = {i:None for i in subject_codes}
                        st.markdown('### Selected subjects are :')
                        st.write(subject_codes)
                        marks = cleanMarks(text,subject_codes)
                        student_marks = concat_subjects(marks)
                        student_marks = pd.concat([student_data,student_marks],axis=1)
                        st.dataframe(student_marks)
                        st.markdown(get_table_download_link(student_marks), unsafe_allow_html=True)
                    except:
                        st.error('Please enter valid subject codes')
                        st.error('Cannot convert following subject codes to excel file')
                        return 
            
            with st.expander('Dowload Excel File'):
                subject_codes = st.text_input('Enter subject codes separated by space Example: 18IT101 18IT102')
                subject_codes_submit = st.button('Submit',key='all_subject_codes_submit')
                if subject_codes_submit:
                    try: 
                        subject_codes = subject_codes.split()
                        subject_codes = {i:None for i in subject_codes}
                        st.markdown('### Selected subjects are :')
                        st.write(subject_codes)
                        marks = cleanMarks(text,subject_codes)
                        student_marks = concat_subjects(marks)
                        student_marks = pd.concat([student_data,student_marks],axis=1)
                        st.markdown(get_table_download_link(student_marks), unsafe_allow_html=True)
                    except:
                        st.error('Please enter valid subject codes')
                        st.error('Cannot convert following subject codes to excel file')
                        return
            
            
    else:
        st.warning('This app is working only for IT department(SELECT IT DEPARTMENT)')

def drop_empty_colums():
    with st.expander('Drop Empty columns from Excel file'):
        csv_file = st.file_uploader(label = "Upload csv file")
    
    
        if csv_file is not None:
            if csv_file.type == 'text/csv':
                df = pd.read_csv(csv_file)
                df = df.replace('nnnnnnn',np.nan)
                df = df.replace('nnn',np.nan)
                df = df.replace('nan',np.nan)
                df = df.dropna(axis=1,how='all')
                st.markdown('### Dataframe after dropping empty columns')
                st.dataframe(df)
                st.markdown(get_table_download_link(df), unsafe_allow_html=True)
            elif csv_file.type == 'excel':
                df = pd.read_excel(csv_file)
                df = df.replace('nnnnnnn',np.nan)
                df = df.replace('nnn',np.nan)
                df = df.replace('nan',np.nan)
                df = df.dropna(axis=1,how='all')
                st.markdown('### Dataframe after dropping empty columns')
                st.dataframe(df)
                st.markdown(get_table_download_link(df), unsafe_allow_html=True)

def datavisualization():
    with st.expander('Data Visualization'):
        st.warning('Data visualization is supported for only numerical data Make sure that the columns to visualize are numerical')
        csv_file = st.file_uploader(label = "Upload csv/excel file")
        if csv_file is not None:
            df = None
            if csv_file.type == 'text/csv':
                df = pd.read_csv(csv_file)
                df = df.replace('nnnnnnn',np.nan)
                df = df.replace('nnn',np.nan)
                df = df.replace('nan',np.nan)
                df = df.dropna(axis=1,how='all')
                st.dataframe(df)
                st.markdown(get_table_download_link(df), unsafe_allow_html=True)
            elif csv_file.type == 'excel':
                df = pd.read_excel(csv_file)
                df = df.replace('nnnnnnn',np.nan)
                df = df.replace('nnn',np.nan)
                df = df.replace('nan',np.nan)
                df = df.dropna(axis=1,how='all')
                st.dataframe(df)
                st.markdown(get_table_download_link(df), unsafe_allow_html=True)

            if df is not None:

                columns = st.multiselect('Select columns to visualize',df.columns)
                if columns:
                    st.markdown('### Selected columns')
                    st.write(columns)
                    for i in columns:
                        if df[i].dtype == 'int64' or df[i].dtype == 'float64':
                            fig = px.histogram(df,x=i)
                            st.plotly_chart(fig)
                        else:
                            st.error('Cannot visualize non numerical data')
                            return
                else:
                    st.error('Please select columns to visualize')
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
        ## :outbox_tray: SPPU DATA ANALYSER: PDF TO EXCEL/CSV
       
    """)

    st.warning("This app is still in development. Please report any bugs to the developer.")
    st.warning("developer contact - surajpisal113@gmail.com")

    mainApp()

    #drop empty columns
    drop_empty_colums()

    #data visualization
    datavisualization()