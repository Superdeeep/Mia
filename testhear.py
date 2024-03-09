import asyncio
import websockets

from RealtimeSTT import AudioToTextRecorder
from colorama import Fore, Back, Style
import colorama
import os

async def send_message(ini):
    uri = "ws://localhost:8777"
    async with websockets.connect(uri) as websocket:
        await websocket.send(ini)
        response = await websocket.recv()
        print(f"Server response: {response}")
        
asyncio.get_event_loop().run_until_complete(send_message("hello"))