import streamlit as st
from src.summarizer import summarize_document, summarize_text
import tempfile
import os


def main():
    st.title("(LangChain + Streamlit) Legal Document Summarizer")

    input_type = st.selectbox("Choose input type:", ["Paste Text", "Upload PDF/DOCX File"])

    if input_type == "Paste Text":
        user_text = st.text_area("Paste the legal text below:")

        if st.button("Summarize"):
            if not user_text.strip():
                st.warning("Please enter some text to summarize.")
            else:
                with st.spinner("Summarizing text..."):
                    summary = summarize_text(user_text)
                st.subheader("Summary")
                st.write(summary)

    else:
        uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=['pdf', 'docx'])

        if uploaded_file is not None:
            if st.button("Summarize"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name

                try:
                    with st.spinner("Summarizing document..."):
                        summary = summarize_document(tmp_path)
                    st.subheader("Summary")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error during summarization: {e}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)


if __name__ == "__main__":
    main()
