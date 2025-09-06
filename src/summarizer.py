from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms.base import LLM
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
import os
import requests
import re
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables (.env file)
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class GroqGemma2LLM(LLM, BaseModel):
    api_key: str = Field(...)
    model_name: str = Field(default="gemma2-9b-it")
    temperature: float = Field(default=0.3)

    def _call(self, prompt: str, stop=None, **kwargs) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": 1024,
        }
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    @property
    def _identifying_params(self):
        return {"model_name": self.model_name, "temperature": self.temperature}

    @property
    def _llm_type(self):
        return "groq"


llm = GroqGemma2LLM(api_key=GROQ_API_KEY)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
)


def load_pdf_document(path: str) -> list:
    loader = PyPDFLoader(path)
    return loader.load()


def load_docx_document(path: str) -> list:
    loader = UnstructuredWordDocumentLoader(path)
    return loader.load()


def clean_text(text: str) -> str:
    # Normalize white spaces and strip
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_documents(docs: list) -> list:
    all_chunks = []
    for doc in docs:
        splits = text_splitter.split_text(doc.page_content)
        all_chunks.extend(splits)
    return [Document(page_content=clean_text(chunk)) for chunk in all_chunks]


def summarize_documents(docs: list) -> str:
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    result = chain.invoke({"input_documents": docs})
    for key in ("text", "output_text", "summary"):
        if key in result:
            return result[key]
    return str(result)


def summarize_document(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        docs = load_pdf_document(path)
    elif ext == ".docx":
        docs = load_docx_document(path)
    else:
        raise ValueError(f"Unsupported document format: {ext}")
    chunks = chunk_documents(docs)
    return summarize_documents(chunks)


def summarize_text(text: str) -> str:
    docs = [Document(page_content=text)]
    chunks = chunk_documents(docs)
    return summarize_documents(chunks)