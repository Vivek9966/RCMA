from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3",streaming=True)
print(llm.invoke("say ok").content)