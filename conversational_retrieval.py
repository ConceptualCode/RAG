from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
#from prompt_template import create_qa_prompt_template

def create_conversational_chain(llm, vectordb):
    """
    Creates a conversational chain with a given language model and vector database.

    Args:
        llm (ChatOpenAI): An instance of a language model used for conversation.
        vectordb (Chroma): An instance of a vector database used for information retrieval.

    Returns:
        ConversationalRetrievalChain: An instance of the ConversationalRetrievalChain initialized with the given language model, vector database, and conversation memory.
    """
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    system_template = """Answer the user question using the provided context and chat history. 
    If you cannot find the answer from the pieces of context, just say that you don't know, don't try to make up an answer.
    When asked, where you got your information from, kindly tell the user the source and context where you got the responses.
    ----------------
    CONTEXT:
    {context}

    CHAT HISTORY:
    {chat_history}

    USER QUESTION:
    {question}

    """

    # Create the chat prompt templates
    messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    #prompt = create_qa_prompt_template()
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 2})
    conversational_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={'prompt': prompt}
    )
    return conversational_chain