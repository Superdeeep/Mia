#约定,
#websocket服务器缩写为WS_SERVER代表此处为服务器本身
#websocket客户端缩写为WS_CLIENT代表此处为客户端本身


import asyncio
import websockets
from RealtimeTTS import TextToAudioStream, CoquiEngine
import ollama
from asyncio import sleep
from Vtube.vtube import *

# WebSocket 服务器配置

Speakcontrol_Websocket_Host_Local = "localhost"
Speakcontrol_Websocket_Server_Port_Local = 8777
authtoken = ""

# 全局变量，用于控制语音引擎的状态
voice_engine_coqui = None


async def answer_from_ollama(input_data):
    response = await asyncio.to_thread(
        ollama.chat,
        model="gemma:2b",
        messages=[{"role": "user", "content": input_data}],
    )
    return response["message"]["content"]


def tts_generator(answer):
    yield answer


async def voice(answer):
    stream = TextToAudioStream(voice_engine_coqui)
    stream.feed(tts_generator(answer))
    stream.play(log_synthesized_text=True)
    
def count_words(text):
    words = text.split()
    return len(words)
    
async def control_N_talking_WS_CLIENT(messageinput):
    #这里是websocket客户端,把说话次数发送给vtube服务器
    uri = "ws://localhost:8788"
    async with websockets.connect(uri) as websocket:
        await websocket.send(messageinput)
        response = await websocket.recv()
        print(f"Server response: {response}")


async def control_vtube_AND_voice_WS_SERVER(websocket, path):
    #这里包含了websocket服务器和客户端
    global voice_engine_coqui

    #这里是服务器,接收来自用户输入的数据
    async for message in websocket:
        print(f"Receive from client: {message}")
        await websocket.send(f"Server respond OK ")

        #将接受到的数据发送给Gemma模型
        answer = await answer_from_ollama(message)# 异步调用Gemma模型
        print(f"Answer from Gemma: {answer}")
        
        
        n = count_words(answer)#统计单词数,确定控制说话开合次数
        print(f"Number of words: {n}")
        
#FLAG_HERE       #获取token!!!此处需要优化!!!
        with open("token.json", "r") as file:
            authtoken = file.read()
        await control_talking_single(authtoken)
        
        #发送说话次数给vtube服务器
        await control_N_talking_WS_CLIENT(str(n))
        await voice(answer)
        


if __name__ == "__main__":
    try:
        # 启动 WebSocket 服务器
        start_server = websockets.serve(
            control_vtube_AND_voice_WS_SERVER, Speakcontrol_Websocket_Host_Local, Speakcontrol_Websocket_Server_Port_Local
        )

        # 创建语音引擎
        voice_engine_coqui = CoquiEngine(voice="./voice/neuro.wav", language="en", speed=1.0)
        print("CoquiEngine initialized.")

        # 启动 WebSocket 服务器的事件循环
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    except KeyboardInterrupt:
        # 捕获 Ctrl+C 信号，关闭语音引擎并退出程序
        if voice_engine_coqui:
            voice_engine_coqui.shutdown()
        print("Program terminated.")
