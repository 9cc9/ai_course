from flask import Flask, request, jsonify
from llama_index.core.base.llms.types import MessageRole, ChatMessage

from base.init_chat import dashscope_llm, retrieve
import faiss

app = Flask(__name__)

##########################
# how to use
# curl -X POST http://localhost:8080/chat -H "Content-Type: application/json" -d '{"message": "鞋子有哪些尺码可以选择呢"}'
##########################

# 加载faiss
faiss_read_index = faiss.read_index('../output/faiss_index_test_shop.index')

# 初始化模型和索引（省略初始化代码）
system_content = f"""
The following context contains the only factual information you should consider.
You must strictly use the information from the context to answer the question.
Do not use any outside knowledge. If the context does not have the answer,
respond with "The answer is not provided in the context.
如果用户对你表达了希望对话结束或者没有问题的含义，请给用户返回:感谢您的咨询，再见！"""
messages = [
    ChatMessage(role=MessageRole.SYSTEM, content=system_content)
]


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided.'}), 400

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
    return jsonify({'response': response_content})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
