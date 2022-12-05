# csv to excel conversion

import csv
import xlsxwriter
import streamlit as st
import pandas
import base64
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import streamlit as st
import time


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def app():
    st.title("Excel to CSV Coverter")
    st.subheader("Upload your Excel file")
    uploaded_file = st.file_uploader("Choose a file", type="xlsx")
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name,
                        "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)
        df = pandas.read_excel(uploaded_file)
        st.write("Data in Excel file")
        st.write(df)
        fileName = uploaded_file.name.split(".")[0] + ".csv"
        csvFile = df.to_csv(index=False)
        if st.download_button(
            label="Download CSV File",
            data=csvFile,
            file_name=fileName,
            mime='text/csv'
        ):
            st.success('Downloaded!')


# main app
app()
