import streamlit as st
from src.summarizer import summarize_document, summarize_text
import tempfile
import os

def main():
    st.set_page_config(page_title="Legal Document Summarizer", layout="centered")
    st.title("Legal Document Summarizer")

    input_mode = st.radio("Select input type:", ["Paste Text", "Upload PDF/DOCX"])

    if input_mode == "Paste Text":
        user_text = st.text_area("Paste the legal document text here:", height=300)

        if st.button("Summarize Text"):
            if not user_text.strip():
                st.warning("Please enter some text before summarizing.")
            else:
                with st.spinner("Generating summary..."):
                    try:
                        summary = summarize_text(user_text)
                        st.subheader("Summary")
                        st.write(summary)
                    except Exception as e:
                        st.error(f"Error during summarization: {str(e)}")

    else:
        uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=['pdf', 'docx'])

        if uploaded_file is not None:
            if st.button("Summarize Document"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name

                try:
                    with st.spinner("Generating summary..."):
                        summary = summarize_document(tmp_path)
                        st.subheader("Summary")
                        st.write(summary)
                except Exception as e:
                    st.error(f"Error during summarization: {str(e)}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

if __name__ == "__main__":
    main()
