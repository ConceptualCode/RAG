from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def create_conversational_chain(llm, vectordb):
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    retriever = vectordb.as_retriever()
    conversational_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        memory=memory
    )
    return conversational_chain
