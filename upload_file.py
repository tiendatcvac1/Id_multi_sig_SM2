import streamlit as st
import docx
import io

content = None
# Use st.file_uploader to allow the user to upload a .docx file
def upload_file():
    uploaded_file = st.file_uploader("Choose a .docx file", type=['docx'])

    if uploaded_file is not None:
        # Read the file into a BytesIO object so python-docx can use it
        bytes_data = uploaded_file.getvalue()
        # Use io.BytesIO to treat the bytes data as a file
        file_like_object = io.BytesIO(bytes_data)
        
        # Load the document using python-docx
        doc = docx.Document(file_like_object)
        
        # Extract all text from the document
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        
        # Join the paragraphs into a single string for display
        content = '\n'.join(full_text)
        
        # st.subheader("File Content:")
        # Use st.markdown or st.write to display the content
        # st.markdown(content)
        # print(type(content))
        return content
    else:
        st.info("Vui lòng chọn file cần ký để upload")
