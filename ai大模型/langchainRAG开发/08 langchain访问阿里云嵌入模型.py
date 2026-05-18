from langchain_community.embeddings import DashScopeEmbeddings

# 创建模型对象 不传默认用的是 text-embeddings-v1
model=DashScopeEmbeddings()

#不用invoke stream
#embed_query\embed_documents
print(model.embed_query("今天AI的资讯有哪些"))
print(model.embed_documents(["晚上吃啥","天气怎么样"]))