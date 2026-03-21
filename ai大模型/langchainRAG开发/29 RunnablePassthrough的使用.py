"""
提示词：用户的提问+向量库中检索到的参考答案
"""
from click import prompt
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser

model=ChatTongyi(model="qwen3-max")
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料：{context}。"),
        ("user","用户提问：{input}")
    ]
)
vector_store=InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))

#add_text 传入一个list[str]
vector_store.add_texts(["减肥就是要少吃多练","在减肥期间要清淡饮食并运动起来","跑步是很好的运动"])

input_text="怎么减肥？"

#langchain中向量存储对象，有一个方法：as_retriever，可以返回一个Runnable接口的子类实例对象
retriever=vector_store.as_retriever(search_kwargs={"k":2})
def print_prompt(prompt):
    print(prompt.to_string())
    return prompt

def format_func(docs):
    if not docs:
        return "无相关资料"
    formatted_str="["
    for doc in docs:
        formatted_str+=doc.page_content
    formatted_str+="]"
    return formatted_str
#chain
chain=(
    {"input":RunnablePassthrough(),"context":retriever|format_func}|prompt|print_prompt|model|StrOutputParser()
)
res=chain.invoke(input_text)
print(res)
"""
retriever:
 -输入：用户的提问 str
 -输出:向量库的检索结果  list[Document]
prompt：
 -输入：用户的提问+向量库的检索结果 dict 
 -输出：完整的提示词  PromptValue
"""