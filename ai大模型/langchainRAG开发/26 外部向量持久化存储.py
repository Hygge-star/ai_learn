from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
#Chroma向量数据库（轻量级）

vector_store=Chroma(
    collection_name="test",  #当前向量存储起个名字，类似数据库的表名称
    embedding_function=DashScopeEmbeddings(), #嵌入模型
    persist_directory="./chroma_db" #指定存放的 文件夹

)

loader=CSVLoader(
    file_path="/data/stu.csv",
    encoding="utf-8",
    source_column="source"
)

documents=loader.load()

#向量存储的 新增、删除、检索
vector_store.add_documents(
    documents=documents,
    ids=["id"+str(i) for i in range(1,len(documents)+1)]
)

#删除 传入["id1",...]
vector_store.delete("id1")
vector_store.delete("id2")
vector_store.delete("id3")

#检索 返回类型list[Document]
result=vector_store.similarity_search(
    "Python是不是简单易学呀",
    3,  #检索的结果要几个
    filter={"source":"Python"},
)

print(result)