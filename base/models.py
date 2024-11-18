from llama_index.legacy.schema import BaseNode


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
