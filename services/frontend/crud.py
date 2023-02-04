import PyPDF2
import os 

def pdf_to_text(pdf_file_path):
    pdfreader = PyPDF2.PdfReader(pdf_file_path)
    no_of_pages = pdfreader.numPages

    # store text in .txt file
    with open('result.txt', 'w') as f:
        for i in range(0, no_of_pages):
            pagObj = pdfreader.getPage(i)
            f.write(pagObj.extractText())

    with open('result.txt', 'r') as f:
        text = f.read()

    # remove unnecessary files
    if os.path.exists("result.txt"):
        os.remove("result.txt")
    return text
