from flask import Flask, request, jsonify, Response
from llama_index.core.base.llms.types import MessageRole, ChatMessage
from base.init_chat import dashscope_llm, retrieve
import faiss
import time

app = Flask(__name__)

##########################
# how to use
# 完整功能的http_server
# 支持steam chat
##########################

# 加载faiss
faiss_read_index = faiss.read_index('../output/faiss_index_test_shop.index')

# 初始化模型和索引
system_content = f"""
The following context contains the only factual information you should consider.
You must strictly use the information from the context to answer the question.
Do not use any outside knowledge. If the context does not have the answer,
respond with "The answer is not provided in the context."
如果用户对你表达了希望对话结束或者没有问题的含义，请给用户返回:感谢您的咨询，再见！"""

# 流式响应生成器
def stream_response(messages):
    # 调用LLM的流式接口
    responses = dashscope_llm.stream_chat(messages)
    for response in responses:
        # 每次获取到新生成的部分，发送给客户端
        tmp = response.delta
        print(tmp)
        yield tmp + '\n'  # 使用 yield 将结果逐步返回
        time.sleep(0.1)  # 模拟延迟，可以根据实际情况调整

@app.route('/streamChat', methods=['POST'])
def streamChat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided.'}), 400

    # 初始化本次请求
    messages = [
        ChatMessage(role=MessageRole.SYSTEM, content=system_content)
    ]

    for message in request.json.get('historyMessages'):
        messages.append(ChatMessage(role=message.get("role"), content=message.get("content")))

    messages.append(ChatMessage(role=MessageRole.USER, content=user_input))

    # 检索上下文
    context = retrieve(user_input, faiss_read_index)
    context_str = system_content + "\nContext:".join(context)
    messages.append(ChatMessage(role=MessageRole.SYSTEM, content=context_str))

    # 返回流式响应
    return Response(stream_response(messages), mimetype='text/plain')

# 保留非流式接口，创建会话时使用
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided.'}), 400

    # 初始化本次请求
    messages = [
        ChatMessage(role=MessageRole.SYSTEM, content=system_content)
    ]

    for message in request.json.get('historyMessages'):
        messages.append(ChatMessage(role=message.get("role"), content=message.get("content")))

    messages.append(ChatMessage(role=MessageRole.USER, content=user_input))

    # 检索上下文
    context = retrieve(user_input, faiss_read_index)
    context_str = system_content + "\nContext:".join(context)
    messages.append(ChatMessage(role=MessageRole.SYSTEM, content=context_str))

    # 调用 LLM 生成答案
    llm_response = dashscope_llm.chat(messages)
    response_content = llm_response.message.content
    messages.append(ChatMessage(role=MessageRole.ASSISTANT, content=response_content))

    # 检查退出条件
    if "再见" in response_content or "退出" in response_content:
        print("===========conversation finish!")
        return jsonify({'response': response_content, 'status': 'end'})

    print(f"助手: {response_content}")
    return jsonify({'response': response_content}), 200, {'Content-Type': 'application/json; charset=utf-8'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)