import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from pages.utils.utils import Preprocessing,Plots
import time
import seaborn as sns
import matplotlib.pyplot as plt

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
    else:
        st.error('Invalid file format')
        st.stop()

    #uncomment this add spinner | progress bar
    # progressBar = st.progress(0, text='Processing File')
    # for percentageComplete in range(100):
    #     time.sleep(0.05)
    #     progressBar.progress(percentageComplete + 1, text='Processing File')

    # hide progress bar after finish
    # progressBar.empty()

    processor = Preprocessing(df)
    df = processor.fillMissingValues()
    df = processor.preprocessPackage('Package')
    # df.to_csv(f"{inputFile.name.split('.')[0]}.csv")

    with st.expander('Show Data in Tabular form'):
        st.success('Click on cloumn name to filter | sort | search')  
        st.dataframe(df)
        # AgGrid(df)

    
    import streamlit as st

    col1, col2 = st.columns([5,5])

    with col1:
        try:
            fig = plt.figure(figsize=(15, 10))
            plt.title('Package Staticstics')
            plt.xlabel('Package')
            plt.ylabel('No of Students')
            sns.histplot(df['Package'])
            plt.legend(['No of Students','Pakcage'],loc='upper right')
            st.pyplot(fig)
            plot = Plots(df)
            plot.downloadPlotBtn(fileName='Package Statistics.png')
            

        except Exception as e:
            st.error(str(e))

    with col2:
        try:
            fig = plt.figure(figsize=(15, 10))
            sns.histplot(df['Package'])
            st.pyplot(fig)
            plot = Plots(df)
            plot.downloadPlotBtn()

        except:
            st.error('error in ploating graph')





