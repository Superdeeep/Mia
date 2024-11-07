import re
import asyncio
import logging

# import from my code
from llm import LLMModule
from vtube_control import VTubeControl

from RealtimeTTS import TextToAudioStream, CoquiEngine


def remove_emoji(text):
    # 只匹配 emoji 的正则表达式
    emoji_pattern = re.compile(
        "[\U00010000-\U0010FFFF]", flags=re.UNICODE  # 匹配所有 emoji 字符
    )
    return emoji_pattern.sub(r"", text)

def tts_feed_generator(answer):
    yield answer


async def main():
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
    token = await vtube_control.get_token()

    engine = CoquiEngine(
        voice="./voice/ttz.wav", language="zh", speed=1.0, level=logging.INFO
    )
    stream = TextToAudioStream(engine)
    print("TTS流已准备")

    stream.feed(tts_feed_generator("你好，欢迎！")).play(log_synthesized_text=True)


    while True:
        # 获取用户输入
        message = input("> ")

        # LLM获取回答
        answer = await llm_module.get_llm_answer(message)
        #print(f"LLM回答: {answer}")

        print(f"LLM回答no emoji: {remove_emoji(answer)}")

        stream.feed(tts_feed_generator(remove_emoji(answer)))
        stream.play_async()

        # 等待TTS播放完毕
        while stream.is_playing():
            await vtube_control.control_talking(token)
            await asyncio.sleep(0.7)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序中断，关闭TTS引擎！")