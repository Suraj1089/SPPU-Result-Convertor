from PIL import Image  
import streamlit as st


st.title("Image to PDF")

# take multiple images and convert them to pdf
inputImages = st.file_uploader("Upload Images", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)

if inputImages:
# convert images to pdf
    images = [Image.open(img) for img in inputImages]
    print(len(images))
    
    convertButton = st.button("Convert")
    if convertButton:
        images[0].save("output.pdf", save_all=True, append_images=images[1:])

        # download the pdf
        with open("output.pdf", "rb") as f:
            bytes = f.read()
            st.download_button(label="Download PDF", data=bytes, file_name="output.pdf", mime="application/pdf")

        # delete the pdf
        import os

        
        os.remove("output.pdf")