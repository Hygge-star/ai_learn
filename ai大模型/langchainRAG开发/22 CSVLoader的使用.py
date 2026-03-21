from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path=",/data/stu.csv",
    csv_args={
        "delimiter": ",", #指定分隔符
        "quotechar": "|",
        #如果数据原本有表头，就不要用下面的代码
        "fieldnnames":['a','b','c','d','e','f','g','h','i'],
    },
    encoding="utf-8"
)

#批量加载 。load()->[Document,Document,...]
#documents = loader.load()

#for document in documents:
#    print(type(document),document)

#懒加载 lazy_loader()   #迭代器
for document in loader.lazy_load():
    print(type(document),document)