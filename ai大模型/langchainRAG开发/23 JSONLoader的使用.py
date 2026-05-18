from langchain_community.document_loaders import JsonLoader
from onnxruntime.transformers.shape_infer_helper import file_path

loader=JsonLoader(
    file_path="./data/stu.json",
    #jp_schema=".name"
    jp_schema=".",
    text_content=False, #告知JSONLoader 抽取的内容不是字符串
    json_lines=True     #告知JSONLoader 这是一个JSONLines文件（每一行都是一个独立的标准JSON）
)

document=loader.load()
print(document)