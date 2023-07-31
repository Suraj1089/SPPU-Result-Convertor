import pandas as pd
from typing import List


class PdfProcessor:
    """
        class to preprocess pdf file
    """
    def __init__(self,text: str) -> None:
        self.text = text

    def removeSubjectNames(self, subjectNames) -> str:
        subjectNames = subjectNames.split('\n')
        for name in subjectNames:
            name = name.strip()
            self.text = self.text.replace(name,'')
        return self.text 
    
