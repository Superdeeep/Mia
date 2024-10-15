import asyncio
from vtube_control import VTubeControl
#from tts import TTSModule
from llm import LLMModule

import logging
from RealtimeTTS import TextToAudioStream, CoquiEngine
import re

def remove_emoji(text):
    # 只匹配 emoji 的正则表达式
    emoji_pattern = re.compile(
        u"[\U00010000-\U0010FFFF]",  # 匹配所有 emoji 字符
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

async def vtube_talking_control(vtube_control, token, should_talk_event):
    """Simulates controlling talking in VTube Studio."""

    while True:
        if should_talk_event.is_set():
            await vtube_control.control_talking(token)
            #print("VTube is talking...")
        await asyncio.sleep(0.1)
    
def tts_feed_generator(answer):
    yield answer

async def main():
    # 初始化各模块
    vtube_control = VTubeControl(
        ws_address="ws://localhost:8001",
        Vtube_id="VTubeControlPlugin",
        Vtube_plugin_name="VTube模型控制插件",
        Vtube_plugin_developer="TArs"
    )
    


    llm_module = LLMModule(system_prompt="你的名字叫妙芽，你喜欢骑自行车")

    # 获取VTube的token
    token = await vtube_control.get_token()
    #logging.basicConfig(level=logging.INFO)
    
    engine = CoquiEngine(voice="./voice/ttz.wav", language="zh", speed=1.0, level=logging.INFO)
    stream = TextToAudioStream(engine)
    print("TTS流已准备")
    
    stream.feed(tts_feed_generator("你好，欢迎！")).play(log_synthesized_text=True)

    should_talk_event = asyncio.Event()
    asyncio.create_task(vtube_talking_control(vtube_control, token, should_talk_event))

    while True:
        # 获取用户输入
        message = input("> ")
        # LLM获取回答
        answer = await llm_module.get_llm_answer(message)
        print(f"LLM回答: {answer}")
        print(f"LLM回答no emoji: {remove_emoji(answer)}")

        should_talk_event.set()
        stream.feed(tts_feed_generator(remove_emoji(answer)))
        stream.play_async()


        while stream.is_playing():
            should_talk_event.set()  # VTube should talk while audio is playing
            await asyncio.sleep(0.1)

        should_talk_event.clear()

        
        

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序中断，关闭TTS引擎")
