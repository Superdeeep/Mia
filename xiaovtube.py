import os
import json
import logging
import asyncio
import websockets
import ollama
import speech_recognition as sr  # 导入语音识别库
from ollama import AsyncClient
from RealtimeTTS import TextToAudioStream, CoquiEngine
from textblob import TextBlob  # 导入情感分析库

stream = None
engine = None
my_requestID = "VTubeControlPlugin"
my_pluginName = "VTube模型控制插件"
my_apiVersion = "1.0"
pluginDeveloperIstars = "TArs"
VTube_websocket_server_remote = "ws://localhost:8001"
token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.txt")

system_prompt = "Please generate the answer that is as short as possible!!! \
                Now you are a high school girl called Mia ,please speak like a student.Please remember your name is Mia. \
                Your personality is adorable yet a bit mischievous. \
                You like blue, enjoy shopping with friends, adore cute things, have a lively and outgoing nature, and love to communicate. \
                You also enjoy biking.\
                Now let's have a small talk."

# 初始化语音识别器
recognizer = sr.Recognizer()
microphone = sr.Microphone()

async def get_token():
    """获取Vtube的token的值并保存"""
    global my_requestID, my_pluginName, my_apiVersion, VTube_websocket_server_remote, pluginDeveloperIstars, token_path
    uri = "ws://localhost:8001"

    if os.path.exists(token_path):
        with open(token_path, "r") as file:
            authtoken = file.read()
            print(f"已存在token,值为:{authtoken}")
    else:
        print("不存在token,尝试自动获取")
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
            json_data = await websocket.recv()
            pack = json.loads(json_data)
            if "errorID" in pack["data"]:
                errorid = pack["data"]["errorID"]
                authtoken = None
                print("获取token失败,请确保在vtube中允许插件访问")
                print(f"错误ID:{errorid}")
            elif "authenticationToken" in pack["data"]:
                authtoken = pack["data"]["authenticationToken"]
                print(f"已获取token:{authtoken}\n并保存在了本地")
                with open(token_path, "w") as file:
                    file.write(authtoken)
    return authtoken

async def control_talking(authtoken, answer):
    """控制vtube模型的嘴巴说话的快捷键"""
    global stream
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
        response_json_data = await websocket.recv()
        pack = json.loads(response_json_data)
        auth_status = pack["data"]["authenticated"]

        if auth_status:
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
            stream.feed(tts_generator(answer))
            stream.play_async()
            print("send.......")
            while stream.is_playing():
                await websocket.send(json.dumps(control_talking_payload))
                await asyncio.sleep(0.3)
            print("finished")
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
    engine = CoquiEngine(voice="./voice/ttz.wav", language="zh", speed=1.0, level=logging.INFO)
    stream = TextToAudioStream(engine)
    print("tts stream is ready")
    stream.feed(Hi_generator()).play(log_synthesized_text=True)

async def answer_from_ollama_chat(input_data):
    message = {"role": "user", "content": input_data}
    response = ollama.chat(model="gemma2:2b", messages=[message])
    return response["message"]["content"]

async def test_ollama_chat(input_data):
    message = {"role": "system", "content": system_prompt}, {"role": "user", "content": input_data}
    response = await AsyncClient().chat(model="gemma2:2b", messages=[message])
    return response["message"]["content"]

async def answer_from_ollama(input_data):
    """llm的回答"""
    response = await asyncio.to_thread(ollama.chat, model="gemma2:2b", messages=[{"role": "user", "content": input_data}])
    return response["message"]["content"]

async def listen_and_respond():
    """监听语音输入并响应"""
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)  # 自动校准以消除环境噪音
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            # 使用Google的Web语音API进行语音识别
            text = recognizer.recognize_sphinx(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

async def main():
    await play_realtime_tts_ready()  # 准备tts
    authtoken = await get_token()  # 获取token
    await asyncio.sleep(1)

    while True:  # 连续用户输入
        user_input = await listen_and_respond()  # 监听用户语音输入
        if user_input:
            answer = await answer_from_ollama(user_input)  # llm回答
            print(answer)  # 打印回答
            await asyncio.gather(control_talking(authtoken, answer))  # 控制嘴巴
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())  # 主循环
    except KeyboardInterrupt:
        print("bye.")  # 中断后
        engine.shutdown()  # 关闭coqui