import numpy as np
from llama_index.llms.dashscope import DashScope
from base.db_models import AiContext
from llama_index.embeddings.dashscope import (
    DashScopeEmbedding,
    DashScopeTextEmbeddingModels,
    DashScopeTextEmbeddingType,
)

LLM_MODEL = "qwen-turbo"
EMBED_MODEL = "text-embedding-v1"
API_KEY = "sk-6267c004c2ac41d69c098628660f41d0"

# 配置初始化

# 使用通义千问的 API 初始化嵌入模型
tongyi_embedding = DashScopeEmbedding(
    model_name=DashScopeTextEmbeddingModels.TEXT_EMBEDDING_V2,
    text_type=DashScopeTextEmbeddingType.TEXT_TYPE_DOCUMENT,
    api_key='sk-6267c004c2ac41d69c098628660f41d0'
)

# 创建 DashScope LLM
dashscope_llm = DashScope(
    model_name=LLM_MODEL,
    api_key=API_KEY
)


# 定义检索函数
def retrieve(query_text, faiss_read_index, k=2):
    # 获取查询的 embedding
    query_embedding = tongyi_embedding.get_text_embedding_batch([query_text])[0]
    distances, indices = faiss_read_index.search(np.array([query_embedding]).astype('float32'), k)
    # print("===========faiss search begin")
    # print(distances)

    retrieved_texts = [AiContext.get(AiContext.id == i + 1).text for i in indices[0]]
    # print(retrieved_texts)
    # print("===========faiss search end")
    return retrieved_texts
