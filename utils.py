from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_community.document_loaders.parsers import LLMImageBlobParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Zilliz
from pymilvus import MilvusClient
import streamlit as st
import os
import json


def create_temp_file(temp_filename, file_extension, uploaded_file):
    # Save the uploaded file to a temporary location
    st.write(f" Detected FileType: {file_extension}")
    with open(temp_filename, "wb") as tmpFile:
        tmpFile.write(uploaded_file.read())

    st.write("Document read successful.")

def add_matadata(documents, user_name, filename, blobname="", other=""):
    """
    Updates metadata for each Document
    """
    for doc in documents:
        
        metadata = doc.metadata
        metadata = {}
        metadata['user_name'] = user_name
        metadata['filename'] = filename
        metadata['blobname'] = blobname
        metadata['other'] = other

        doc.metadata=metadata
        # print(doc.metadata)

    return documents

def split_document_into_chunks(documents, chunk_size, chunk_overlap):
    """
    splits a list of documents into smaller text chunks based on 
    specified chunk_size and chunk_overlap
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    document_chunks = text_splitter.split_documents(documents)

    return document_chunks
    

def create_document_vector(doc_stream, filename, doc_type, agent_name, user_name):

    llm = ChatOpenAI(model="gpt-4.1-nano")
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    COLLECTION_NAME = json.loads( os.getenv("AGENTS_COLLECTION"))[agent_name]

    if doc_type == '.pdf':
        loader = PyMuPDFLoader(doc_stream,
                            # mode="single",
                            images_inner_format="html-img",
                            images_parser=LLMImageBlobParser(model=llm), # Will Extract the Document
                            extract_tables="markdown"
                    )

    elif doc_type == '.txt':
        loader = TextLoader(doc_stream, encoding="utf-8")

    
    documents = loader.load()
    st.write("Document load sucessfull.")

    documents = add_matadata(documents, user_name, filename)
    document_chunks = split_document_into_chunks(documents, chunk_size=1000, chunk_overlap=300)

    st.write("Saving to DB...")
    status =  save_to_vectorDB(document_chunks, embeddings, COLLECTION_NAME)
    st.write("Save Sucessfull !!")

    return status


def save_to_vectorDB(chunks, embeddings, COLLECTION_NAME):

    ZILLIZ_CLOUD_URI = os.getenv("ZILLIZ_CLOUD_URI")
    ZILLIZ_CLOUD_TOKEN = os.getenv("ZILLIZ_CLOUD_TOKEN")

    # try:
    #     # Establish a connection to Zilliz
    #     zilliz_client = MilvusClient(uri=ZILLIZ_CLOUD_URI, token=ZILLIZ_CLOUD_TOKEN, secure=True)
    #     # Load the collection
    #     if zilliz_client.has_collection(COLLECTION_NAME):
    #         zilliz_client.drop_collection(COLLECTION_NAME)
    #         print(f"Collection '{COLLECTION_NAME}' dropped successfully.")
    # except Exception as e:
    #     print(f"Collection '{COLLECTION_NAME}' does not exist or could not be dropped: {e}")

    Zilliz.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection_args={
            "uri": ZILLIZ_CLOUD_URI,
            "token": ZILLIZ_CLOUD_TOKEN,
            "secure": True
        },
        auto_id=True
    )

    return True