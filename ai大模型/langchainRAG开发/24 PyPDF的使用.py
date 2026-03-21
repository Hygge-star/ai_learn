from langchain_community.document_loaders import PyPDFLoaders
from onnxruntime.transformers.shape_infer_helper import file_path

loader=PyPDFLoaders(
    file_path="。/data/pdf1.pdf",
    mode="page", #默认是page模式，每一个页面形成一个Document文档对象
    #mode="single" #single模式，不管有多少也，只返回1个DDocument对象
    password="itheima"
)

i=0
for doc in loader.lazy_load():
   i+=1
   print(doc)
   print("="*20,i)