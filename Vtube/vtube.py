import os
import json
import ollama
import logging
import asyncio
import websockets
from ollama import AsyncClient
from RealtimeTTS import TextToAudioStream, CoquiEngine

# import random
# import numpy as np
# import requests
# import time

stream = None
engine = None
my_requestID = "VTubeControlPlugin"
my_pluginName = "VTube模型控制插件"
my_apiVersion = "1.0"
pluginDeveloperIstars = "TArs"
VTube_websocket_server_remote = (
    "ws://localhost:8001"  # VTube Studio WebSocket服务器地址
)
token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.txt")


system_prompt = "Please generate the answer that is as short as possible!!! \
                Now you are a high school girl called Mia ,please speak like a student.Please remember your name is Mia. \
                Your personality is adorable yet a bit mischievous. \
                You like blue, enjoy shopping with friends, adore cute things, have a lively and outgoing nature, and love to communicate. \
                You also enjoy biking.\
                Now let's have a small talk."


# system_prompt="The assistant replies to the user in a playful and sarcastic manner."


async def get_token():
    """获取Vtube的token的值并保存"""

    global my_requestID, my_pluginName, my_apiVersion, VTube_websocket_server_remote, pluginDeveloperIstars, token_path
    uri = "ws://localhost:8001"

    # 判断是否存在已经获取的token
    if os.path.exists(token_path):
        with open(token_path, "r") as file:
            authtoken = file.read()
            print(f"已存在token,值为:{authtoken}")

    else:
        print("不存在token,尝试自动获取")
        # 发送验证控制载荷

        async with websockets.connect(uri) as websocket:

            request_token_payload = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": my_apiVersion,
                "requestID": my_requestID,
                "messageType": "AuthenticationTokenRequest",
                "data": {
                    "pluginName": my_pluginName,
                    "pluginDeveloper": pluginDeveloperIstars,
                },
            }

            await websocket.send(json.dumps(request_token_payload))

            # 处理返回的数据
            json_data = await websocket.recv()
            pack = json.loads(json_data)

            # 如果拒绝插件访问
            if "errorID" in pack["data"]:
                errorid = pack["data"]["errorID"]  # 解析data中的errorid
                authtoken = None
                print("获取token失败,请确保在vtube中允许插件访问")
                print(f"错误ID:{errorid}")
            # 如果允许插件访问
            elif "authenticationToken" in pack["data"]:
                authtoken = pack["data"]["authenticationToken"]
                print(f"已获取token:{authtoken}\n并保存在了本地")

                with open(token_path, "w") as file:
                    file.write(authtoken)
    # 返回获取到的token
    return authtoken


async def control_talking(authtoken, answer):
    """控制vtube模型的嘴巴说话的快捷键"""

    global stream
    # 验证=========================
    async with websockets.connect(VTube_websocket_server_remote) as websocket:
        authentication_payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": my_apiVersion,
            "requestID": my_requestID,
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": my_pluginName,
                "pluginDeveloper": pluginDeveloperIstars,
                "authenticationToken": authtoken,
            },
        }
        await websocket.send(json.dumps(authentication_payload))
        # ============================

        # 处理接收的数据=================
        response_json_data = await websocket.recv()
        pack = json.loads(response_json_data)
        auth_status = pack["data"]["authenticated"]
        # ============================

        # 判断=========================
        if auth_status == True:  # 这里的判断可能是有问题的，应该为try catch

            # 发送快捷键数据
            control_talking_payload = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": my_requestID,
                "messageType": "HotkeyTriggerRequest",
                "data": {
                    "hotkeyID": "hotkey_talk",
                },
            }
            await websocket.send(json.dumps(control_talking_payload))

            # 往tts流中丢入llm返回的数据
            stream.feed(tts_generator(answer))

            # 并发，同步和检测是否正在播放
            stream.play_async()
            print("send.......")

            while stream.is_playing():  # 如果tts没有停止
                await websocket.send(
                    json.dumps(control_talking_payload)
                )  # 发送控制嘴巴的快捷键
                print("send....")
                await asyncio.sleep(0.3)  # 等待0.3s
            print("finished")  # tts停止后发送

        else:
            print(f"Received response:\n{response_json_data}")


def Hi_generator():
    yield "hello this is a test sentence"


def test_voice_generator():
    yield "Hello! I'm an avid learner and explorer of ideas, constantly seeking to expand my horizons and embrace new challenges."


def tts_generator(answer):
    yield answer


async def play_realtime_tts_ready():
    """初始化coqui并说出测试句子"""

    global stream, engine
    logging.basicConfig(level=logging.INFO)
    engine = CoquiEngine(
        voice="./voice/neuro.wav", language="en", speed=1.0, level=logging.INFO
    )

    stream = TextToAudioStream(engine)

    print("tts stream is ready")
    stream.feed(Hi_generator()).play(log_synthesized_text=True)


async def answer_from_ollama_chat(input_data):
    message = {"role": "user", "content": input_data}
    response = ollama.chat(model="gemma:2b", messages=[message])
    return response["message"]["content"]


async def test_ollama_chat(input_data):
    message = {"role": "system", "content": system_prompt}, {
        "role": "user",
        "content": input_data,
    }
    response = await AsyncClient().chat(model="gemma:2b", messages=[message])
    return response["message"]["content"]


async def answer_from_ollama(input_data):
    """llm的回答"""

    response = await asyncio.to_thread(
        ollama.chat,
        model="gemma:2b",
        messages=[{"role": "user", "content": input_data}],
    )
    return response["message"]["content"]


async def main():
    # 测试功能部分
    # authtoken=await get_token()
    # await asyncio.gather(test_talk(authtoken))
    # await asyncio.sleep(100)
    # ollama.embeddings(model='gemma:2b', prompt=system_prompt)
    # system_answer=await test_ollama_chat()
    # print(system_answer)

    # while True:
    #    message = input(">")
    #
    #    answer=await answer_from_ollama_chat(message)
    #    print(answer)
    ##########

    await play_realtime_tts_ready()  # 准备tts
    authtoken = await get_token()  # 获取token
    await asyncio.sleep(1)

    # systemanswer = await answer_from_ollama(
    #    system_prompt
    # )  # 输入系统提示词，塑造角色个性。
    # print(f"This is System prompt return:\n{systemanswer}")

    while True:  # 连续用户输入
        message = input(">")  # 输入等待
        answer = await answer_from_ollama(message)  # llm回答
        print(answer)  # 打印回答
        await asyncio.gather(control_talking(authtoken, answer))  # 控制嘴巴
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    try:

        asyncio.get_event_loop().run_until_complete(main())  # 主循环
        # asyncio.get_event_loop().run_until_complete(get_token())
        # asyncio.get_event_loop().run_forever()

    except KeyboardInterrupt:
        print("bye.")  # 中断后
        engine.shutdown()  # 关闭coqui
