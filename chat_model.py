from langchain.chat_models import ChatOpenAI

def initialize_chat_model(model_name='gpt-3.5-turbo', temperature=0):
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)
    return llm
