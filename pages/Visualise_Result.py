import pandas as pd
from ydata_profiling import ProfileReport

import streamlit as st

from streamlit_pandas_profiling import st_profile_report

df = pd.read_excel('result.xlsx')
pr = df.profile_report()

st_profile_report(pr)