import asyncio
import websockets
from RealtimeTTS import TextToAudioStream, CoquiEngine
import ollama

# WebSocket 服务器配置
WEBSOCKET_HOST = "localhost"
WEBSOCKET_PORT = 8777

# 全局变量，用于控制语音引擎的状态
coqui_engine = None

async def test_ollama_async(input_data):
    response = await asyncio.to_thread(ollama.chat, model="gemma:2b", messages=[{"role": "user", "content": input_data}])
    return response["message"]["content"]

def dummy_generator(answer):
    yield answer

async def handle_connection(websocket, path):
    global coqui_engine

    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(f"Server received ok ")

        # 异步调用Gemma大模型
        answer = await test_ollama_async(message)

        # 发出声音
        stream = TextToAudioStream(coqui_engine)
        stream.feed(dummy_generator(answer))
        stream.play(log_synthesized_text=True)

if __name__ == "__main__":
    try:
        # 启动 WebSocket 服务器
        start_server = websockets.serve(handle_connection, WEBSOCKET_HOST, WEBSOCKET_PORT)

        # 创建语音引擎
        coqui_engine = CoquiEngine(voice="w.wav", language="en", speed=1.0)

        # 启动 WebSocket 服务器的事件循环
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    except KeyboardInterrupt:
        # 捕获 Ctrl+C 信号，关闭语音引擎并退出程序
        if coqui_engine:
            coqui_engine.shutdown()
        print("Program terminated.")
