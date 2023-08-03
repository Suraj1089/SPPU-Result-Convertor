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

    placement = {
        'Package > 10': 8,
        'Package 8 - 10': 6,
        'Package 6 - 8': 12,
        'Package 4 - 6': 20,
        'Package < 4': 30
    }
    fig = plt.figure(figsize=(15, 10))
    # plot pie chart
    plt.pie(placement.values(), labels=placement.keys(), autopct='%1.1f%%')
    plt.title('Package Distribution')
    plt.show()
    st.pyplot(fig)
    plot = Plots(df)
    plot.downloadPlotBtn(fileName='Package Distribution.png')

    col0, col_1 = st.columns([5,5])

    with col0:
        try:
            topper_Students = {
                'FE': {'Name': 'HONDE RENUKA RADHAKRUSHAN', 'SGPA': 9.5},
                'SE': {'Name': 'BHAMARE VISHAL SHARAD', 'SGPA': 9.34},
                'TE': {'Name': 'SAGAR BALASAHEB GAME', 'SGPA': 9.1},
                'BE': {'Name': 'POKHARKAR KASTURI SANJAY', 'SGPA': 9.7}
            }
            fig = plt.figure(figsize=(15, 15))
            plt.title('Topper Students in each year')
            plt.ylabel('SGPA')
            plt.xlabel('Year')
            sns.barplot(x=list(topper_Students.keys()),y=[topper_Students['FE']['SGPA'],topper_Students['SE']['SGPA'],topper_Students['TE']['SGPA'],topper_Students['BE']['SGPA']],palette='twilight_shifted_r')
            plt.show()
            st.pyplot(fig)
            plot = Plots(df)
            plot.downloadPlotBtn(fileName='topper.png')
        except Exception as e:
            st.error('error in ploating graph', str(e))
    

    with col_1:
        try:
            no_of_distinction = {
                'FE': 42,
                'SE': 32,
                'TE': 61,
                'BE': 52
            }
            fig = plt.figure(figsize=(15, 15))
            plt.title('No. of Distinction in each year')
            plt.ylabel('No. of Students')
            plt.xlabel('Year')
            sns.barplot(x=list(no_of_distinction.keys()),y=[no_of_distinction['FE'],no_of_distinction['SE'],no_of_distinction['TE'],no_of_distinction['BE']],palette='inferno')
            plt.show()
            st.pyplot(fig)
            plot = Plots(df)
            plot.downloadPlotBtn(fileName='distinction.png')



        except:
            st.error('error in ploating graph')



    col1, col2 = st.columns([5,5])

    with col1:
        try:
            fig = plt.figure(figsize=(15, 12))
            plt.title('Package Staticstics')
            plt.xlabel('Package')
            plt.ylabel('No of Students')
            sns.histplot(df['Package'],color='green')
            plt.legend(['No of Students','Pakcage'],loc='upper right')
            st.pyplot(fig)
            plot = Plots(df)
            plot.downloadPlotBtn(fileName='Package Statistics.png')
            

        except Exception as e:
            st.error(str(e))

    with col2:
        try:
            fig = plt.figure(figsize=(15, 12))
            plt.title('Package Staticstics')
            plt.xlabel('Package')
            plt.ylabel('No of Students')
            sns.histplot(df['Package'])
            st.pyplot(fig)
            plot = Plots(df)
            plot.downloadPlotBtn()

        except:
            st.error('error in ploating graph')





    col3, col4 = st.columns([5,5])

    with col3:
        try:
            df['BE Status Y'] = df['BE Status Y'].apply(lambda x: x.upper())
            fig = plt.figure(figsize=(15, 15))
            plt.title('Number of BE Students Pass/Fail')
            plt.ylabel('No. of Students')
            plt.xlabel('Pass/Fail/ATKT/Not Available')
            sns.countplot(x='BE Status Y',data=df) 
            plt.show()
            st.pyplot(fig)
            plot = Plots(df)
            plot.downloadPlotBtn(fileName='Package Statistics.png')
            

        except Exception as e:
            st.error(f'Error in BE Status ', str(e))

    with col4:
        try:
            sgpa_count = {'SGPA > 9':4, 'SGPA 8 - 9':5, 'SGPA 7 - 8':8, 'SGPA 6 - 7':20, 'SGPA < 6':30}
            for sgpa in df['BE SGPA']:
                if type(sgpa) == int or type(sgpa) == float:
                    if sgpa > 9:
                        sgpa_count['SGPA > 9'] += 1
                    elif sgpa >= 8 and sgpa <= 9:
                        sgpa_count['SGPA 8 - 9'] += 1
                    elif sgpa >= 7 and sgpa <=8:
                        sgpa_count['SGPA 7 - 8'] += 1
                    elif sgpa >= 6 and sgpa <=7:
                        sgpa_count['SGPA 6 - 7'] += 1
                    elif sgpa < 6:
                        sgpa_count['SGPA < 6'] += 1

            fig = plt.figure(figsize=(15, 10))
            # plot pie chart
            plt.pie(sgpa_count.values(), labels=sgpa_count.keys(), autopct='%1.1f%%')
            plt.title('SGPA Distribution')
            plt.show()
            st.pyplot(fig)
            plot = Plots(df)
            plot.downloadPlotBtn(fileName='SGPA Distribution.png')

        except Exception as e:
            st.error('error in ploating graph', str(e))



    col5, col6 = st.columns([5,5])

    with col5:
        try:
            df['Admission Quota'] = df['Admission Quota'].fillna(value=0)
            fig = plt.figure(figsize=(15, 15))
            plt.title('Admission Quota')
            plt.ylabel('No. of Students')
            plt.xlabel('CAP/NON-CAP')
            sns.countplot(x='Admission Quota',data=df) 
            plt.show()
            st.pyplot(fig)
            plot = Plots(df)
            plot.downloadPlotBtn(fileName='admissionQuota.png')
        except Exception as e:
            st.error('error in ploating graph', str(e))
    
    with col6:
        try:
            # pass fail status in each year
            pass_fail = {
                'FE': {'Pass': 134, 'Fail': 14},
                'SE': {'Pass': 120, 'Fail': 28},
                'TE': {'Pass': 140, 'Fail': 8},
                'BE': {'Pass': 145, 'Fail': 3},
            }
            plt.title('Pass/Fail Status in each year')
            plt.ylabel('No. of Students')
            plt.xlabel('Year')
            sns.barplot(x=list(pass_fail.keys()),y=[pass_fail['FE']['Pass'],pass_fail['SE']['Pass'],pass_fail['TE']['Pass'],pass_fail['BE']['Pass']],palette='RdPu')
            plt.show()
            st.pyplot(fig)
            plot = Plots(df)
            plot.downloadPlotBtn(fileName='pass_fail.png')
        except Exception as e:
            st.error('error in ploating graph', str(e))





    # col7 = st.columns(10)   
    # with col7:

    try:
        max_cgpa = {
            'OS': 85,
            'DS': 64,
            'CNS': 95,
            'DE': 69,
            'CG': 85,
            'DSA': 71,
            'SE': 75,
            'DBMS': 96,
            'CA': 85,
            'AI': 85,
            'ML': 92,
            'SD': 72,
            'BDA': 98,

        }
        fig = plt.figure(figsize=(15, 15))
        plt.title('Subject Wise Maximum Marks')
        plt.ylabel('CGPA')
        plt.xlabel('Subjects')
        # plt.bar(max_cgpa.keys(),max_cgpa.values())
        import random
        num_bars = len(max_cgpa)
        random_colors = [f'#{random.randint(0, 0xFFFFFF):06x}' for _ in range(num_bars)]

        # sns.barplot(x=list(max_cgpa.keys()),y=list(max_cgpa.values()),palette='OrRd_r')
        sns.barplot(x=list(max_cgpa.keys()), y=list(max_cgpa.values()), palette=random_colors)
        for index, value in enumerate(list(max_cgpa.values())):
            plt.text(index, value, str(value), ha='center', va='bottom')

        plt.show()
        st.pyplot(fig)
        plot = Plots(df)
        plot.downloadPlotBtn(fileName='max_cgpa.png')
    except Exception as e:
        st.error('error in ploating graph', str(e))

        