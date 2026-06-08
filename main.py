import os
from fastapi import FastAPI, UploadFile, File
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_community.memory import ConversationBufferMemory

app = FastAPI()

@app.post("/load-documents")
async def load_documents(file: UploadFile = File(...)):
    documents = []

    for file in os.listdir("documents"):
        if file.endswith(".txt"):
            path = os.path.join("documents", file)

            print(f"Loading: {file}")

            loader = TextLoader(path, encoding="utf-8")

            documents.extend(loader.load())

    return {"message": f"{len(documents)} pages loaded"}

@app.post("/generate-embeddings")
async def generate_embeddings():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(
        chunks,
        embeddings
    )

    retriever = db.as_retriever(
        search_kwargs={"k": 3}
    )

    return {"message": "Embeddings generated"}

@app.post("/ask-question")
async def ask_question(question: str):
    memory = ConversationBufferMemory()

    llm = OllamaLLM(model="qwen2.5:7b")  # Define 'llm' here

    docs = retriever.invoke(question, memory=memory)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
    Answer ONLY from the context.

    If the answer is not present,
    say:
    'I could not find that information in the documents.'

    Context:
    {context}

    Question:
    {question}
    """

    answer = llm.invoke(prompt, memory=memory)

    return {"answer": answer}

print("Program Started")
documents = []

for file in os.listdir("documents"):
    if file.endswith(".txt"):
        path = os.path.join("documents", file)

        print(f"Loading: {file}")

        loader = TextLoader(path, encoding="utf-8")

        documents.extend(loader.load())

print(f"Pages loaded: {len(documents)}")

print("Splitting documents...")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

print(f"Chunks created: {len(chunks)}")

print("Loading embeddings model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Creating FAISS database...")

db = FAISS.from_documents(
    chunks,
    embeddings
)

retriever = db.as_retriever(
    search_kwargs={"k": 3}
)

memory = ConversationBufferMemory()

print("\nKnowledge Chatbot Started")
print("Type exit to quit\n")

llm = OllamaLLM(model="qwen2.5:7b")  # Define 'llm' here

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    docs = retriever.invoke(question, memory=memory)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
    Answer ONLY from the context.

    If the answer is not present,
    say:
    'I could not find that information in the documents.'

    Context:
    {context}

    Question:
    {question}
    """

    answer = llm.invoke(prompt, memory=memory)

    print("\nBot:")
    print(answer)
    print()
