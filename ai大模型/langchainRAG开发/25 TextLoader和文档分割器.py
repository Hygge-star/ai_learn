from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
loader = TextLoader(
    "./data/Python.txt",
    encoding="utf-8",
)

document = loader.load()

splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,  #分段的最大字符数
    chunk_overlap=50, #分段之间允许重叠字符数
    #文本自然段落分隔的 依据符号
    separators=["/n/n","/n","!","。"],
    length_function=len, #统计字符的依据函数
)

split_docs=splitter.split_documents(document)
print(len(split_docs))