from langchain_google_genai import GoogleGenerativeAI
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import os

from dotenv import load_dotenv
load_dotenv()

api_key = os.environ['GOOGLE_API_KEY']

llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key, temperature=0.5)

instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
vectordb_file_path = "/home/alan/python/sideproject/faiss_index"

def create_vector_db ():
    loader = CSVLoader(file_path='/home/alan/python/sideproject/action_table.csv', source_column="prompt")
    action_docs = loader.load()

    vectordb = FAISS.from_documents(documents=action_docs, 
                                    embedding=instructor_embeddings)
    
    vectordb.save_local(vectordb_file_path)

def get_ask_chain():
    vectordb = FAISS.load_local(vectordb_file_path, instructor_embeddings)

    retriever = vectordb.as_retriever()

    prompt_template = """
    Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide the answer from "actions" according to context, and not make to much of changes.
    請用中文回答
    CONTEXT: {context}

    QUESTION: {question}
    """
    # Please answer in the following format(dictionary type):
    #     answer context:,action:,adjustment number:

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(llm=llm,
                                        chain_type="stuff",
                                        retriever=retriever,
                                        input_key="query",
                                        return_source_documents=True,
                                        chain_type_kwargs={"prompt": PROMPT})
    return chain


if __name__ == "__main__":
    # create_vector_db()
    chain = get_ask_chain()

    print(chain.invoke("調亮燈光"))



    # Given the following context and questions, generate an answer.
    # In the answer, try to provide context from "prompt" section without make to much of change.
    # In the answer try to provide as much text as possible from "actions" section in the source document context without making much changes.

    # prompt_template = """Given the following context and a question, generate an answer based on this context only.
    # In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
    # 請用中文回答
    # CONTEXT: {context}

    # QUESTION: {question}"""