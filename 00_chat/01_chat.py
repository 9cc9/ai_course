from llama_index.core.base.llms.types import MessageRole, ChatMessage
from base.init_chat import dashscope_llm

#################################################
# 直接调用大模型
#################################################

# 初始化模型和索引（省略初始化代码）
system_content = f"""
如果用户对你表达了希望对话结束或者没有问题的含义，请给用户返回:感谢您的咨询，再见！"""
messages = [
    ChatMessage(role=MessageRole.SYSTEM, content=system_content)
]

while True:
    # 获取用户输入
    user_input = input("\n用户: ")
    messages.append(ChatMessage(role=MessageRole.USER, content=user_input))

    # 调用 LLM 生成答案
    llm_response = dashscope_llm.chat(messages)
    content = llm_response.message.content
    print(f"助手: {content}")

    # llm_response = dashscope_llm.stream_chat(messages)
    # content = ""
    # for response in llm_response:
    #     tmp_resp = response.delta
    #     print(tmp_resp, end="")
    #     content += tmp_resp

    # 将助手的回复添加到消息中
    messages.append(ChatMessage(role=MessageRole.ASSISTANT, content=content))

    # 检查 LLM 的响应是否包含退出关键词
    if "再见" in content:
        break
