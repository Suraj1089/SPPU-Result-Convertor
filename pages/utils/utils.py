import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

class Preprocessing:
    def __init__(self,df: pd.DataFrame) -> None:
        self.df = df 
    
    def fillMissingValues(self) -> pd.DataFrame:
        self.df = self.df.replace(to_replace='',value=np.nan).fillna(value=np.nan)
        return self.df 
    
    def toExel(self,outputFileName: str) -> pd.ExcelFile:
        return self.df.to_excel(outputFileName)
    
    def toCsv(self,outputFileName: str):
        return self.df.to_csv(outputFileName)
    
    def preprocessPackage(self,columnName: str) -> pd.DataFrame:
        self.df[columnName] = self.df[columnName].astype(str).apply(lambda x: x.split('L')[0]).astype(float)
        return self.df
    


class Plots:
    def __init__(self,df: pd.DataFrame) -> None:
        self.df = df 

    def downloadPlotBtn(self, label: str = 'Download Image',fileName: str = 'image.png', mime: str = 'image/png'):
        plt.savefig(fileName)
        with open(fileName, 'rb') as img:
            btn = st.download_button(
                label=label,data=img,
                file_name=fileName,
                mime=mime
            )
        
    def histogram(self):
        pass 

