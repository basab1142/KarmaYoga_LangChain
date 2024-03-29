from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import pickle
import numpy as np
import faiss
from langchain_google_genai import ChatGoogleGenerativeAI
import os

from dotenv import load_dotenv
load_dotenv()

from langchain import HuggingFaceHub
llm_huggingface=HuggingFaceHub(repo_id="google/flan-t5-xxl",model_kwargs={"temperature":0.5,"max_length":1000})
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm_gemini = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

loader = TextLoader('karmayoga.txt')
data = loader.load()
file_path="vector_index.pkl"
doc_file = "doc_file.pkl"
encoder = SentenceTransformer('all-mpnet-base-v2')


building_vector_db = False # to build file make it True
if building_vector_db:
    text_splitter = RecursiveCharacterTextSplitter(
    separators=['\n\n','\n','.',' '],
    chunk_size=500,
    chunk_overlap=100
    )

    docs = text_splitter.split_documents(data)
    with open(doc_file,'wb') as f:
        pickle.dump(docs, f)
    vectors = []

    for i in range(len(docs)):
        texti = docs[i].page_content
        vector = encoder.encode(texti)
        vectors.append(vector)
    vectors = np.array(vectors)    


    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    with open(file_path, "wb") as f:
        pickle.dump(index, f)

def response(query):
    with open(file_path, "rb") as f:
        vectorstore = pickle.load(f)
    with open(doc_file, "rb") as f:
        docs = pickle.load(f)        
    search_vector = encoder.encode([query])
    dist, I = vectorstore.search(search_vector, k = 5)
    sent = f"Using the information mentioned  find answer of {query} :" + '. '.join([docs[i].page_content for i in I[0]])
    result = llm_huggingface.invoke(sent)
    return result

def gemini_response(query):
    with open(file_path, "rb") as f:
        vectorstore = pickle.load(f)
    with open(doc_file, "rb") as f:
        docs = pickle.load(f)        
    search_vector = encoder.encode([query])
    dist, I = vectorstore.search(search_vector, k = 5)
    sent = f"Using the information mentioned  find answer of {query} :" + '. '.join([docs[i].page_content for i in I[0]])
    result = llm_gemini.invoke(sent).content


    return result



