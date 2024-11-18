import faiss
import numpy as np
import pandas as pd
from llama_index.legacy.vector_stores.faiss import FaissVectorStore
from base.models import *
from base.init_chat import tongyi_embedding


###############################################
# 将知识库数据embedding化，写入到faiss向量库
# 1. documents->embeddings
# 2. embeddings to faiss
###############################################


# 配置初始化

# 流式读取数据，每次读取5行(优化大文件读取)
chunk_size = 5
embeddings = []
texts = []
nodes = []

for chunk in pd.read_csv('../data/运动鞋店铺知识库.txt', sep='\t', names=['passage'], chunksize=chunk_size):
    batch_texts = chunk['passage'].tolist()

    # 批量生成 embeddings
    try:
        batch_embeddings = tongyi_embedding.get_text_embedding_batch(batch_texts)
    except Exception as e:
        print(f"Error in embedding generation: {e}")
        continue

    for i, row in enumerate(chunk.itertuples()):
        doc_text = row.passage
        texts.append(doc_text)
        embedding = batch_embeddings[i]
        embeddings.append(embedding)
        nodes.append(CustomNode(text=doc_text, embedding=embedding))

# 生成 embeddings 并创建 FAISS 索引
embeddings_np = np.array(embeddings).astype('float32')

# 初始化faiss，embedding索引长度embeddings_np.shape[1]=1536
faiss_index = faiss.IndexFlatL2(embeddings_np.shape[1])

# 初始化并写入 FAISS 向量存储
faiss_store = FaissVectorStore(faiss_index=faiss_index)
# 添加节点到 FAISS 向量存储
faiss_store.add(nodes)  # 直接添加节点
# 保存 FAISS 索引到文件
faiss.write_index(faiss_index, '../output/faiss_index_test_shop.index')
print("============write index successfully")
