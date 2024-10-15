# ai_course

## 1.准备工作
1. 安装python&pip
2. pip install -r requirements.txt

## 2.chat
**基于知识库实现一个简单的聊天对话**
1. [01_write_to_faiss.py](01_chat%2F01_write_to_faiss.py) 读取知识库数据，写入faiss。运行完后，会生成output/faiss_index_test_shop.index文件
2. [02_chat_with_faiss.py](01_chat%2F02_chat_with_faiss.py) 加载知识库，根据faiss结果组装prompt，调用大模型接口

## 3.simple_http_server
**封装http接口，开放服务给外部调用**

注意：需要先运行[01_write_to_faiss.py](01_chat%2F01_write_to_faiss.py) ，准备faiss文件

测试命令行：curl -X POST http://localhost:8080/chat -H "Content-Type: application/json" -d '{"message": "鞋子有哪些尺码可以选择呢"}'

## 4.http_server
**开放服务给到springboot应用使用**

注意：需要先运行[01_write_to_faiss.py](01_chat%2F01_write_to_faiss.py) ，准备faiss文件

springboot应用地址：https://github.com/9cc9/ai_manager