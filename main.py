import re
import asyncio
import logging
import time


# import from my code
from llm import LLMModule
from vtube_control import VTubeControl

from multiprocessing import Process, Manager, Value
from RealtimeTTS import TextToAudioStream, CoquiEngine


def remove_emoji(text):
    # 只匹配 emoji 的正则表达式
    emoji_pattern = re.compile(
        "[\U00010000-\U0010FFFF]", flags=re.UNICODE  # 匹配所有 emoji 字符
    )
    return emoji_pattern.sub(r"", text)


async def vtube_talking_control(vtube_control, token, should_talk_event):
    """Simulates controlling talking in VTube Studio."""

    while True:
        if should_talk_event.is_set():
            await vtube_control.control_talking(token)
        await asyncio.sleep(0.1)


def tts_feed_generator(answer):
    yield answer


def process_tts(input_text, vtube_control, token,shared_flag):
    engine = CoquiEngine(
        voice="./voice/ttz.wav", language="zh", speed=1.0, level=logging.INFO
    )
    stream = TextToAudioStream(engine)
    print("TTS流已准备")

    stream.feed(tts_feed_generator("你好，欢迎！")).play(log_synthesized_text=True)

    stream.feed(tts_feed_generator(remove_emoji(input_text)))
    stream.play_async()

    while stream.is_playing():
        vtube_control.control_talking(token)
        shared_flag.value = 1
        time.sleep(0.1)

    shared_flag.value = 0
    print("TTS流播放完毕")


async def main():
    should_talk_event = asyncio.Event()
    asyncio.create_task(vtube_talking_control(vtube_control, token, should_talk_event))


if __name__ == "__main__":
    with Manager() as manager:
        try:
            shared_string = manager.Value("s", "初始字符串")
            shared_flag = Value("i", 0)

            # 初始化各模块
            vtube_control = VTubeControl(
                ws_address="ws://localhost:8001",
                Vtube_id="VTubeControlPlugin",
                Vtube_plugin_name="VTube模型控制插件",
                Vtube_plugin_developer="TArs",
            )

            # llm_module = LLMModule(system_prompt="你的名字叫妙芽，你喜欢骑自行车")
            llm_module = LLMModule()

            # 获取VTube的token
            token = vtube_control.get_token()

            while True:

                message = input("> ")

                answer = llm_module.get_llm_answer(message)
                
                print(f"LLM回答: {answer}")
                #print(f"LLM回答no emoji: {remove_emoji(answer)}")
                #shared_string = manager.Value("s", answer)
                #ttstask = Process(target=process_tts, args=(shared_string, vtube_control, token, shared_flag,))
                #ttstask.start()
                #ttstask.join()
        except KeyboardInterrupt:
            print("程序中断！")
