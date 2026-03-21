from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, prompt, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableWithMessageHistory

from file_history_store import conversation_chain
from file_history_store import get_history

import config_data as config
from vector_stores import VectorStoresService

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt
class RagService(object):
    def __init__(self):
        self.vector_service=VectorStoresService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name),
        )
        self.prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的已知参考资料为主"
                 "简洁和专业的回答用户问题。参考资料：{context}"),
                ("system","并且我提供用户的对话历史记录，如下："),
                MessagesPlaceholder("history"),
                ("user","请回答用户提问：{input}")
            ]
        )

        self.chat_model=ChatTongyi(model=config.chat_model_name)
        self.chain=self._get_chain()

    def _get_chain(self):
        """获取最终的执行链"""
        retriever = self.vector_service.get_retriever()
        # 使用内部方法 _get_relevant_documents（因为公共方法不存在）
        retrieve_func = retriever._get_relevant_documents

        def format_document(docs: list[Document]):
            if not docs:
                return "无相关参考资料"
            formatted_str = ""
            for doc in docs:
                formatted_str += f'文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n'
            return formatted_str

        def temp2(value):
            # value 结构: {"input": 原始输入字典(含input和history), "context": 格式化后的文档字符串}
            return {
                "input": value["input"]["input"],  # 用户问题字符串
                "context": value["context"],  # 上下文文档（修正键名）
                "history": value["input"]["history"]  # 历史消息列表
            }

        chain = (
                {
                    "input": RunnablePassthrough(),  # 传递整个输入字典
                    "context": RunnableLambda(lambda x: x["input"])  # 提取用户问题字符串
                               | RunnableLambda(retrieve_func)  # 检索文档
                               | RunnableLambda(format_document)  # 格式化文档
                }
                | RunnableLambda(temp2)  # 重组为prompt所需格式
                | self.prompt_template
                | RunnableLambda(print_prompt)  # 可选调试
                | self.chat_model
                | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",  # 注意参数名正确（单下划线）
            output_messages_key="output",
        )
        return conversation_chain
if __name__=="__main__":
    #session id配置
    session_config={
        "configurable":{
            "session_id":"user_001",
        }
    }
    res=RagService().chain.invoke({"input":"我体重52kg，尺码推荐"},session_config)
    print(res)


