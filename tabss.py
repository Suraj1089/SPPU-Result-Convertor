import streamlit as st 
import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.express as px # interactive plotting
import re       # clean string
import PyPDF2  # convert pdf to text 
import time 
import plotly.express as px 


# set variables in session state
st.session_state.projects = [
    'Boring Project', 'Interesting Project'
]
st.session_state.current_project = st.radio(
    'Select a project to work with:',
    st.session_state.projects,
)

st.write(st.session_state.projects)