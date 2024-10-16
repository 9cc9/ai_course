from llama_index.core.base.llms.types import MessageRole, ChatMessage
from base.init_chat import dashscope_llm, retrieve
import faiss

#################################################
# 根据faiss结果组装prompt，咨询llm
# 1. 对咨询的问题embeddings
# 2. query faiss
# 3. 从mysql查到对应context
# 4. contract prompt by context
# 5. 调用llm
#################################################

# 加载faiss
faiss_read_index = faiss.read_index('../output/faiss_index_test_shop.index')

# 构造prompt
system_content = f"""
The following context contains the only factual information you should consider.
You must strictly use the information from the context to answer the question.
Do not use any outside knowledge. If the context does not have the answer,
respond with "The answer is not provided in the context.
如果用户对你表达了希望对话结束或者没有问题的含义，请给用户返回:感谢您的咨询，再见！"""
messages = [
    ChatMessage(role=MessageRole.SYSTEM, content=system_content)
]

while True:
    # 获取用户输入
    user_input = input("用户: ")

    messages.append(ChatMessage(role=MessageRole.USER, content=user_input))

    # 检索上下文（根据需要调整为实际检索函数）
    context = retrieve(user_input, faiss_read_index)  # 假设 retrieve_context 函数已定义
    context_str = system_content + "\nContext:".join(context)

    # 将上下文添加到消息中
    messages.append(ChatMessage(role=MessageRole.SYSTEM, content=context_str))

    # 调用 LLM 生成答案
    llm_response = dashscope_llm.chat(messages)
    print(f"助手: {llm_response.message.content}")

    # 将助手的回复添加到消息中
    messages.append(ChatMessage(role=MessageRole.ASSISTANT, content=llm_response.message.content))

    # 检查 LLM 的响应是否包含退出关键词
    if "再见" in llm_response.message.content or "退出" in llm_response.message.content:
        print("===========conversation finish!")
        break
