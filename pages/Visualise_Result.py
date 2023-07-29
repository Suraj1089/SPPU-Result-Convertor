import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
import openpyxl as op

st.title("Visualize Result")
st.warning('To visualize result your input file contains the following columns with exact same name')
columns =[
    'Sr. No. ', 'PRN ', 'Candidate Name', 'Category', 'Admission Quota',
       '10th % Marks', '12th % Marks', 'CET Marks/Rank', 'M1', 'PHY/ CHEM',
       'FPL-I', 'BEE/ BXE', 'BCEE', 'EG-I', 'SGPA', 'CLASS', 'No. of Backlogs',
       'M-II', 'PHY/ CHEM.1', 'FPL-II', 'EM', 'BEE / BXE', 'BME', 'SGPA.1',
       'CLASS.1', 'Sem-I Back', 'Sem-II Back', 'Total back', 'FE SGPA',
       'FE Status Y', 'DS', 'COA', 'DELD', 'FDS', 'PSOO', 'MIII', 'CG', 'PA',
       'DSF', 'FCCN', 'Sem2', 'Sem1', 'SE SGPA', 'SE Status Y', 'TOC', 'DBMS',
       'SEPM', 'OS ', 'HCI', 'CNT', 'SP', 'DAA', 'CC', 'DSBDA', 'TE SGPA',
       'TE Status Y', 'ICS', 'ML&A', 'SDM', 'BAI', 'STQA', 'DCS', 'UC', 'IOT',
       'SMA', 'BE SGPA', 'BE Status Y', 'Name of Company', 'Unnamed: 68',
       'Package'
]

st.write(pd.DataFrame({'columns':columns}).transpose())

# Take multiple CSV/Excel files and convert them to Pandas DataFrames
inputFile = st.file_uploader("Upload Csv/Excel File", type=['csv', 'excel', 'xlsx'], accept_multiple_files=False)

df = None
if inputFile:
    fileExtension = inputFile.name.split('.')[-1]
    if fileExtension == 'csv':
        df = pd.read_csv(inputFile)
    elif fileExtension == "xlsx":
        df = pd.read_excel(inputFile)

    with st.expander('Show Data in Tabular form'):
        st.success('Click on cloumn name to filter | sort | search')  
        AgGrid(df)

    
    import streamlit as st

    col1, col2 = st.columns([5,5])

    with col1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg")

    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")


