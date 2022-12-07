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
import time
from st_aggrid import GridUpdateMode, DataReturnMode
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode

from itdepartment import dispaly_interactive
# from functionforDownloadButtons import download_button


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
    st.markdown("""
        ## CSV to Excel Conversion
    """)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name,
                        "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)
        df = pandas.read_csv(uploaded_file)
        storeDf = df
        st.write("Data in CSV file")

        gridOptions = dispaly_interactive(df)

        st.success(
            f"""
                💡 Tip! Hold the shift key when selecting rows to select multiple rows at once!
                """
        )
        response = AgGrid(
            df,
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
        fileName = uploaded_file.name.split(".")[0] + ".xlsx"
        excelFile = to_excel(storeDf)
        if st.download_button(
            label="Download Excel File",
            data=excelFile,
            file_name=fileName,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ):
            st.success('Downloaded!')


# main app
app()
