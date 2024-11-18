import requests
import asyncio
from llama_index.embeddings.openai.base import BaseEmbedding
from pydantic import BaseModel, Field
from llama_index.legacy.schema import BaseNode


# 定义通义千问嵌入模型类^
class TongyiEmbedding(BaseEmbedding, BaseModel):
    api_url: str = Field(...)
    api_key: str = Field(...)
    model_name: str = Field(...)

    def _get_text_embedding(self, text):
        """实现文本嵌入"""
        return self.embed([text])  # 调用 embed 函数来处理单个文本

    def _get_query_embedding(self, query):
        """实现查询嵌入"""
        return self.embed([query])  # 调用 embed 函数来处理查询

    async def _aget_query_embedding(self, query):
        """实现异步查询嵌入"""
        return await asyncio.to_thread(self._get_query_embedding, query)

    def embed(self, texts):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(self.api_url, headers=headers, json={"model": self.model_name, "input": texts})
        response_data = response.json()
        embeddings = [data.get('embedding', []) for data in response_data.get("data", [])]
        return embeddings


# 定义自定义节点类
class CustomNode(BaseNode):
    text: str
    embedding: list

    def get_embedding(self):
        """返回嵌入向量"""
        return self.embedding

    def get_content(self):
        """返回节点的内容"""
        return self.text

    def get_metadata_str(self):
        """返回节点的元数据字符串"""
        return ""  # 可以返回具体的元数据

    def get_type(self):
        """返回节点的类型"""
        return "CustomNode"  # 可以返回特定类型的字符串

    def hash(self):
        """返回节点的哈希值"""
        return hash(self.text)  # 或者使用其他逻辑

    def set_content(self, content):
        """设置节点的内容"""
        self.text = content
