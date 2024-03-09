import asyncio
import websockets
import json
from asyncio import sleep
import os
import random
import numpy as np
import ollama


def test_ollama(inputdata):
   response = ollama.chat(model='gemma:2b', messages=[
  {
    'role': 'user',
    'content': inputdata,
  },
])
   print(response['message']['content'])
   return response['message']['content']

def dummy_generator():
        myol=test_ollama()
        yield myol
    


async def handle_connection(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        test_ollama(message)
        await websocket.send(f"Server received ok ")

# 启动 WebSocket 服务器
start_server = websockets.serve(handle_connection, "localhost", 8765)

# 运行事件循环
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



