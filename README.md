# ai_course

## 准备工作
1. 安装python&pip
2. pip install -r requirements.txt
3. 安装mysql server
4. 导入知识库数据到mysql
    * 新建数据库
    * [schema.sql](data%2Fschema.sql) 执行建表语句
    * [ai_context.sql](data%2Fai_context.sql) 导入数据
    * 参考[db_models.py](base%2Fdb_models.py)文件，按需修改db连接配置

## [00_chat](00_chat)
**一个简单的聊天对话,直接使用llama_index对接大模型API**

## [01_chat_with_faiss](01_chat_with_faiss)
**基于知识库实现一个简单的聊天对话**
1. [01_write_to_faiss.py](01_chat%2F01_write_to_faiss.py) 读取知识库数据，写入faiss。运行完后，会生成output/faiss_index_test_shop.index文件
2. [02_chat_with_faiss.py](01_chat%2F02_chat_with_faiss.py) 加载知识库，根据faiss结果组装prompt，调用大模型接口

## [02_simple_http_server](02_simple_http_server)
**封装http接口，开放服务给外部调用**

注意：需要先运行[01_write_to_faiss.py](01_chat%2F01_write_to_faiss.py) ，准备faiss文件

测试命令行：curl -X POST http://localhost:8080/chat -H "Content-Type: application/json" -d '{"message": "鞋子有哪些尺码可以选择呢"}'

## [03_http_server](03_http_server)
**开放服务给到springboot应用使用**

注意：需要先运行[01_write_to_faiss.py](01_chat%2F01_write_to_faiss.py) ，准备faiss文件

springboot应用地址：https://github.com/9cc9/ai_manager