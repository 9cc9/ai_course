import faiss
import numpy as np
import pandas as pd
from llama_index.legacy.vector_stores.faiss import FaissVectorStore
from base.models import *
from base.init_chat import tongyi_load_embedding


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

# TODO：考虑多线程并发执行
for chunk in pd.read_csv('../data/运动鞋店铺知识库.txt', sep='\t', names=['passage'], chunksize=chunk_size):
    batch_texts = chunk['passage'].tolist()

    # 批量生成 embeddings
    try:
        batch_embeddings = tongyi_load_embedding.get_text_embedding_batch(batch_texts)
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
# IndexFlat：最基础的索引类型，直接存储所有向量并进行精确的搜索，适合小规模数据集或对精度要求非常高的场景。
# IndexFlatL2 是一种基于欧式距离（L2 距离）的索引类型，用于精确地进行向量的最近邻搜索，适合小规模数据集或对精度要求较高的场景。
# IndexAnnoy 基于树的近似最近邻搜索方法（Annoy），适合中等规模的数据集，查询速度较快，适用于内存和速度的平衡需求。
# IndexIVFPQ：将倒排文件（IVF）和产品量化（PQ）结合的索引类型，通过量化压缩向量并对簇内数据进行检索，适合大规模数据集且对内存和查询速度有双重要求。
faiss_index = faiss.IndexFlatL2(embeddings_np.shape[1])

# 初始化并写入 FAISS 向量存储
faiss_store = FaissVectorStore(faiss_index=faiss_index)
# 添加节点到 FAISS 向量存储
faiss_store.add(nodes)  # 直接添加节点
# 保存 FAISS 索引到文件
faiss_store.persist(persist_path='../output/faiss_index_test_shop.index')
# faiss.write_index(faiss_index, '../output/faiss_index_test_shop.index')
print("============write index successfully")
