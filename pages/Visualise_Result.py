import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import numpy as np



def main():
    st.title('Result Visualiser')

    # file uploader for csv or excel file
    uploadedFile = st.file_uploader(
        label="Upload CSV or Excel File", type=["csv", "xlsx"])
    
    st.warning('To view the visualisation, please upload the file in the format provided in the sample file.')
    st.write('File contains columns Sr. No.	Division	Exam Seat No	PRN	Name of Students	ISE	ESE	Total	Total%	CRD	GRD	GP	CP	TW	Total%	CRD	GRD	GP	CP	ISE	ESE	Total	Total%	CRD		GP	CP	ISE	ESE	Total	Total%	CRD	GRD	GP	CP	ISE	ESE	Total	Total%	CRD	GRD	GP	CP	ISE	ESE	Total	Total%	CRD	GRD	GP	CP	TW	PR	Total%	CRD	GRD	GP	CP	TW	PR	Total%	CRD	GRD	GP	CP	PR	Total%	CRD	GRD	GP	CP	TW	Total%	CRD	GRD	GP	CP	SGPA1	Total CRD	Total Backlog')

    if uploadedFile is not None:
        stroedDf = None
        if uploadedFile.type == 'text/csv':
            stroedDf = pd.read_csv(uploadedFile)
        else:
            stroedDf = pd.read_excel(uploadedFile)

        df = stroedDf

        with st.expander('Show Details'):

            st.write("Data in Uploded file")

            AgGrid(df)
            st.subheader("Filtered data will appear below 👇 ")
            st.text("")

            st.table(stroedDf)

            st.text("")

        # show the visualisation options
        # create three columns
        # st.write(stroedDf.columns)
        # st.write(df.astype(str))
        col1, col2 = st.columns(2)
        try:

            with col1:
                col1.metric('No of students having 0 backlogs',
                            len(df[df['Total Backlog'] == 0]), 0)

            with col2:
                col2.metric('No of students having 1 backlogs',
                            len(df[df['Total Backlog'] == 1]), 1)

            col3, col4 = st.columns(2)
            with col3:
                col3.metric('No of students having 2 backlogs',
                            len(df[df['Total Backlog'] == 2]), 2)

            with col4:
                col4.metric('No of students having more than 3 backlogs',
                            len(df[df['Total Backlog'] >= 3]), 3)
        except:
            st.error('File is not in valid format')
            return

        # st.write(df.dtypes.astype(str))
        # count of sgpa chart in plotly
        # st.success('SGPA Vs Count of Students')
        try:
            fig = px.histogram(df, x="SGPA1", color="SGPA1", marginal="rug",
                               title="SGPA Distribution")
            fig.update_layout(
                xaxis_title='Student SGPA',
                yaxis_title='No of Students'
            )

            st.plotly_chart(fig)
        except:
            st.error('Error occured while rendering the graph')

        # subject wise maximum marks
        st.success('Subject wise maximum marks')
        maxCount = []

        for i in range(len(df.columns)):
            if 'Total%' in df.columns[i]:
                df[df.columns[i]] = df[df.columns[i]].replace('FF', np.nan)
                df[df.columns[i]] = df[df.columns[i]].replace('', np.nan)
                df[df.columns[i]] = df[df.columns[i]].replace(' ', np.nan)
                df[df.columns[i]] = df[df.columns[i]].replace('--', np.nan)
                df[df.columns[i]] = df[df.columns[i]].replace('O', np.nan)

                try:
                    df[df.columns[i]] = df[df.columns[i]].astype(float)
                    maxCount.append(df[df.columns[i]].max())
                except:
                    pass

        try:
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric('214441', maxCount[0], '214441')
            col2.metric('214442', maxCount[1], '214442')
            col3.metric('214443', maxCount[2], '214443')
            col4.metric('214444', maxCount[3], '214444')
            col5.metric('214445', maxCount[4], '214445')
            col6, col7, col8, col9, col10 = st.columns(5)
            col6.metric('214446', maxCount[5], '214446')
            col7.metric('214447', maxCount[6], '214447')
            col8.metric('214448', maxCount[7], '214448')
            col9.metric('214449', maxCount[8], '214449')
            col10.metric('21444A', maxCount[9], '21444A')
        except:
            st.error('Error occured while loading the data')

        st.success('subject wise average marks')
        avgCount = []

        for i in range(len(df.columns)):
            if 'Total%' in df.columns[i]:
                df[df.columns[i]] = df[df.columns[i]].replace('FF', np.nan)
                df[df.columns[i]] = df[df.columns[i]].replace('', np.nan)
                df[df.columns[i]] = df[df.columns[i]].replace(' ', np.nan)
                df[df.columns[i]] = df[df.columns[i]].replace('--', np.nan)
                df[df.columns[i]] = df[df.columns[i]].replace('O', np.nan)

                try:
                    df[df.columns[i]] = df[df.columns[i]].astype(float)
                    avgCount.append(df[df.columns[i]].mean())
                except:
                    pass

        try:

            fig = px.bar(x=['214441', '214442', '214443', '214444', '214445', '214446', '214447',
                            '214448', '214449', '21444A'], y=avgCount, color=avgCount, hover_data=[avgCount])
            # update x and y legends
            fig.update_layout(
                xaxis_title='subject codes',
                yaxis_title='average marks'
            )

            st.plotly_chart(fig)
        except:
            st.error('Error occured while plotting the graph')

        
        with st.expander("Get topper details"):
            
            try:
                df = df.sort_values(by=['SGPA1'],ascending=False)
                st.dataframe(df[['Exam Seat No','Name of Students','SGPA1']].head(5).reset_index(drop=True))
            except:
                st.error('Error occured while loading the data')


main()