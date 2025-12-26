import base64
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM 
from langchain_classic.memory import ConversationBufferMemory 
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate

# --- VISION MODEL SETUP ---
# Moondream model ko yahan initialize karna zaroori hai
vision_model = OllamaLLM(model="moondream")

def analyze_image(image_path, user_query):
    """Image ko base64 mein convert karke Moondream se analyze karwane ke liye"""
    try:
        with open(image_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        
        prompt = f"Analyze this pet image and describe it based on this question: {user_query}"
        # Moondream ko image aur prompt bhej rahe hain
        description = vision_model.invoke(input=prompt, images=[img_base64])
        return description
    except Exception as e:
        print(f"Vision Error: {e}")
        return f"Error analyzing image: {str(e)}"

# --- RAG CHAIN ---
def build_rag_chain():
    print("[DEBUG] Loading PDFs from data folder...")
    # 'data' folder se PDF load ho rahi hain
    loader = DirectoryLoader("data", glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)

    llm = OllamaLLM(model="llama3", temperature=0.7) 
    
    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True, 
        output_key="answer"
    )

    template = """You are a professional PetCare Assistant.
    Use the Context to answer. If not in Context, use General Knowledge.
    
    Context: {context}
    Chat History: {chat_history}
    User Question: {question}
    Assistant Answer:"""

    CUSTOM_PROMPT = PromptTemplate(template=template, input_variables=["context", "chat_history", "question"])

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
        memory=memory,
        return_source_documents=True,
        output_key="answer",
        combine_docs_chain_kwargs={"prompt": CUSTOM_PROMPT} 
    )
    return chain