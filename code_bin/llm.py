import asyncio
import websockets
import json
from asyncio import sleep
import os
import random
import numpy as np
import ollama
from RealtimeTTS import TextToAudioStream, CoquiEngine
import time
import speech

answer = ""

def test_ollama(inputdata):
    response = ollama.chat(
        model="gemma:2b",
        messages=[
            {
                "role": "user",
                "content": inputdata,
            },
        ],
    )
    print(response["message"]["content"])
    return response["message"]["content"]


def dummy_generator():
    global answer
    myol = answer
    yield myol
    
async def handle_connection(websocket, path):
    global answer
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(f"Server received ok ")
        
        answer = test_ollama(message)
        speech.say(answer)



# 启动 WebSocket 服务器
start_server = websockets.serve(handle_connection, "localhost", 8777)

# 运行事件循环
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

""" if __name__ == "__main__":
    while True:
        coqui_engine = CoquiEngine(voice="neuro.wav", language="en", speed=1.0)
        stream = TextToAudioStream(coqui_engine)
        stream.feed(dummy_generator())
        stream.play(log_synthesized_text=True)
        coqui_engine.shutdown() """
