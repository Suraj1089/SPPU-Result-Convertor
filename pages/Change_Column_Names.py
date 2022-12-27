import streamlit as st
import pandas as pd
from itdepartment import getTabledownloadLink


def changeColumnNames():
    """
        function to change column names from file 
    """
    st.write('Change Column Names from Csv/Excel file')

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
                    st.markdown(getTabledownloadLink(
                        df), unsafe_allow_html=True)
                except:
                    st.error(
                        'Please enter valid column names(all column names should be unique)')
                    return


#
changeColumnNames()
