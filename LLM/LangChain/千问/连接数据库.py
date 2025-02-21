import os

from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import chat_agent_executor

os.environ["OPENAI_API_KEY"] = "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"
os.environ["https://proxy"] = "127.0.0.1:7890"
os.environ["https://proxy"] = "127.0.0.1:7890"
os.environ["LANGCAHIN__TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KE"]= "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"

# 调用大预言模型
LLM = ChatOpenAI(
    api_key="sk-rnwiM44VUccSsNNjFeD12b7226E64548B9250922A936F88e",
    base_url="https://free.v36.cm",
    model="gpt-3.5-turbo",  # 此处以qwen-plus为例，您可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    # other params...
)


MYSQL_URL = "mysql+pymysql://root:123456@localhost:3306/llm?charset=utf8"
db = SQLDatabase.from_uri(MYSQL_URL)
#创建工具

toolkit =  SQLDatabaseToolkit(db = db ,llm = LLM)
tools = toolkit.get_tools()

#使用agent 整合数据库
system_prompt = """
是一个被设计用来与SQL数据库交互的代理。
定一个输入问题，创建一个语法正确的S0L语句并执行，然后查看查询结果并返回答案。
除非用户指定了他们想要获得的示例的具体数量，否则始终将S0L查询限制为最多10个结果。
你可以按相关列对结果进行排序，以返回MySQL数据库中最匹配的数据。
您可以使用与数据库交互的工具。在执行査询之前，你必须仔细检査。如果在执行査询时出现错误，请重写査询并重试。
不要对数据库做任何DML语句(插入，更新，删除，删除等)
首先，你应该查看数据库中的表，看看可以查询什么。
不要跳过这一步。
然后查询最相关的表的模式

"""
system_message = SystemMessage(content=system_prompt)

#创建爱你代理
agent_executor = chat_agent_executor.create_tool_calling_executor(LLM, tools,system_message)

resp = agent_executor.invoke({
    'message':[HumanMessage(content="用户表中有多少条数据")]
})
result = resp['messages']
print(result)
print(len(result))