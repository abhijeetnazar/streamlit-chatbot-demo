import faiss
from langchain import OpenAI
from langchain.chains import VectorDBQAWithSourcesChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
# from langchain.chains import  BaseQAWithSourcesChain
import pickle
import argparse

parser = argparse.ArgumentParser(description='Ask a question to the notion DB.')
parser.add_argument('question', type=str, help='The question to ask the notion DB')
args = parser.parse_args()

# Load the LangChain.
index = faiss.read_index("course.index")

with open("course.pkl", "rb") as f:
    store = pickle.load(f)

store.index = index

chain = load_qa_with_sources_chain(OpenAI(temperature=0),chain_type="refine")
result = chain({"input_documents": store.similarity_search(args.question, k=4),"question": args.question,},return_only_outputs=True,)["output_text"]

print(result)

# chain = VectorDBQAWithSourcesChain.from_llm(llm=OpenAI(temperature=0), vectorstore=store)
# result = chain({"question": args.question})
# print(f"Answer: {result['answer']}")
# print(f"Sources: {result['sources']}")