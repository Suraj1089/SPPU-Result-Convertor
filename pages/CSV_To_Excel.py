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
    st.title("CSV to Excel Conversion")
    st.write("This is a simple CSV to Excel conversion app")
    st.write("Upload your CSV file")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name,
                        "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)
        df = pandas.read_csv(uploaded_file)
        st.write("Data in CSV file")
        st.write(df)
        fileName = uploaded_file.name.split(".")[0] + ".xlsx"
        excelFile = to_excel(df)
        if st.download_button(
            label="Download Excel File",
            data=excelFile,
            file_name=fileName,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ):
            st.success('Downloaded!')


# main app
app()
