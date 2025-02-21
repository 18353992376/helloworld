import os

import bs4
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import DashScopeEmbeddings, QianfanEmbeddingsEndpoint
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.chat_message_histories import ChatMessageHistory


""
os.environ["https://proxy"] = "127.0.0.1:7890"
os.environ["https://proxy"] = "127.0.0.1:7890"
os.environ["TAVILY_API_KEY"] = "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"
os.environ["DASHSCOPE_API_KEY"] = "sk-726ae67e535f416bb9cef7c94504f400"

chatLLM = ChatOpenAI(
    api_key="sk-rnwiM44VUccSsNNjFeD12b7226E64548B9250922A936F88e",
    base_url="https://free.v36.cm",
    model="chatgpt",  # 此处以qwen-plus为例，您可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    # other params...
)
embeddings = DashScopeEmbeddings(
    model="text-embedding-v2",
    # other params...
)
#数据获取
loader = WebBaseLoader(
    web_paths=['https://lilanweng.github.io/posts/2023-06-23-agent'],
    bs_kwargs=dict(
        parser_only=bs4.SoupStrainer(class_=("post-content", "post-header"))
    )
)
docs = loader.load()

#数据切割
splitter = RecursiveCharacterTextSplitter(chunk_size=20, chunk_overlap=4)
resp = splitter.split_documents(docs)

#存储
vectorStore = Chroma.from_documents(documents = resp, embedding =QianfanEmbeddingsEndpoint)

#检索器
retriever = vectorStore.as_retriever()

#整合
#创建 一个问题的模板
system_prompt = """
您是回答有关网站问题的有用助手.
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

#创建链
chain1 =create_stuff_documents_chain(chatLLM,prompt)
# chain2 = create_retrieval_chain(retriever,chain1)
# resps = chain2.invoke({"input": "中国的首都是那里"})
# print(resps)


#子链模板
son_prompt = """

"""
retriever_history_temp = ChatPromptTemplate.from_messages(
    [
        ("system", son_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
#创建一个子链
history_chain = create_history_aware_retriever(chatLLM, retriever, retriever_history_temp)
#保存问答的历史记录
store = {

}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    else:
        return store[session_id]

#创建父链
chain = create_retrieval_chain(history_chain, chain1)
result_chain = RunnableWithMessageHistory(chain, get_session_history,
                                          input_messages_key="input",
                                          history_messages_key="chat_history",
                                          output_messages_key="answer")
res1 = result_chain.invoke({"input": "中国的首都是哪里", "session_id": "1"})
res2 = result_chain.invoke({"input": "中国prime minister是谁", "session_id": "1"})
print(res1)
print(res2)

