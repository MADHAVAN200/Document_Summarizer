# Legal Document Summarizer

This project is an AI-powered Legal Document Summarizer that utilizes Groq’s Gemma2 large language model integrated with LangChain. It allows users to input legal documents in PDF, DOCX, or raw text formats. The system preprocesses the input by extracting, cleaning, and splitting the text into manageable chunks that fit within the model’s token limits. Each chunk is individually summarized using a map-reduce approach, then the summaries are combined to produce a concise and accurate overview of complex legal texts. The project features an interactive Streamlit-based web interface for easy user interaction, along with modular backend code enabling efficient, accurate summarization that simplifies understanding for both legal professionals and non-experts alike.

---

To run the app, use the following command:
 `streamlit run streamlit_app.py`
