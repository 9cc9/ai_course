# coding=utf-8

import dashscope
from dashscope.audio.tts_v2 import *

dashscope.api_key = "sk-6267c004c2ac41d69c098628660f41d0"
model = "cosyvoice-v1"
voice = "longxiaochun"


synthesizer = SpeechSynthesizer(model=model, voice=voice)

audio = synthesizer.call("how are you？I am fine,thank you.")
print('requestId: ', synthesizer.get_last_request_id())
with open('output.mp3', 'wb') as f:
    f.write(audio)