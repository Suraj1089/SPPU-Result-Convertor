import streamlit as st
import smtplib


# Details how to use the app

def app():
    st.code("""
    Que 1: How to use this app?
    Ans: This app is very easy to use. Just upload the file and click on the button to convert it to the desired format.""")

    st.code("""Que 2: What are features of this app?
    Ans: This app has the following features:
    1. Convert Excel to CSV
    2. Convert PDF to Excel
    3. Convert Text to PDF
    4. Convert Word to PDF""")

    st.code("""Que 3: How to convert Excel to CSV?
    Ans: To convert Excel to CSV, follow the steps below:
    1. Click on the Excel to CSV button on the sidebar
    2. Upload the Excel file
    3. Click on the Download CSV button to download the converted file.""")

    st.code("""Que 4: How to convert PDF to Excel?
    Ans: To convert PDF to Excel, follow the steps below:
    1. Click on the PDF to Excel button on the sidebar
    2. Upload the PDF file
    3. Click on the Download Excel button to download the converted file.""")

    st.code("""Que 5: How to convert Text to PDF?
    Ans: To convert Text to PDF, follow the steps below:
    1. Click on the Text to PDF button on the sidebar
    2. Upload the Text file
    3. Click on the Download PDF button to download the converted file.""")

    st.code("""Que 6: How to convert Word to PDF?
    Ans: To convert Word to PDF, follow the steps below:
    1. Click on the Word to PDF button on the sidebar
    2. Upload the Word file
    3. Click on the Download PDF button to download the converted file.""")

    st.code("""Que 7: How to contact the developer?
    Ans: You can contact the developer at:
    1. Email: surajpisal113@gmail.com
    2. Email: Email: vikrammarkali007@gmail.com""")

    st.code("""Que 8: How to contribute to this project?
    Ans: You can contribute to this project by:
    1. Forking the project
    2. Making changes to the code
    3. Creating a pull request""")

    st.code("""Que 9: How to report a bug?
    Ans: You can report a bug by:
    1. Creating an issue on GitHub
    2. Mentioning the bug in the issue""")

    st.code("""Que 10: How to suggest a feature?
    Ans: You can suggest a feature by:
    1. Creating an issue on GitHub
    2. Mentioning the feature in the issue""")

    st.code("""Que 11: How to get the source code?
    Ans: You can get the source code by:
    1. Forking the project
    2. Cloning the project""")

    st.code("""Que 12: How to get the latest updates?
    Ans: You can get the latest updates by:
    1. Forking the project
    2. Pulling the latest changes from the main branch""")


    st.code("""Que 14: How to get support?
    Ans: contact the developer at:
    1. Email: surajpisal113@gmail.com.
    2.Emial: vikrammarkali007@gmail.com
    3.Email: durgeshmahajan1722@gmail.com""")

    st.code("""Que 15: Why should I use this app?
    Ans: You should use this app because:
    1. It is free
    2. It is easy to use
    3. It is fast
    4. It is secure
    5. It is open source""")

    # form to get feedback from the user
    st.title('Feedback')
    with st.form('feedback_form'):
        name = st.text_input('Name')
        email = st.text_input('Email')
        feedback = st.text_area('Feedback')
        submit = st.form_submit_button('Submit')

    if submit:
        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(email,'surajpisal113@gmail.com',feedback)         
            st.success('Email sent successfully')
        except Exception as e:
            pass 
        st.success('Feedback submitted successfully')
        st.balloons()


app()