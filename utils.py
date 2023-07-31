import pandas as pd
from typing import List


class PdfProcessor:
    """
        class to preprocess pdf file
    """
    def __init__(self,text: str) -> None:
        self.text = text

    def removeSubjectNames(self, subjectNames: List[str]) -> str:
        print('*' * 50)
        for name in subjectNames:
            print(name)
            self.text = self.text.replace(name,'')
        return self.text 
    
