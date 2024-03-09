import asyncio
import websockets

from RealtimeSTT import AudioToTextRecorder
from colorama import Fore, Back, Style
import colorama
import os



async def send_message(messageinput):
    if messageinput.strip():  # Check if the message is not empty after stripping whitespace
        uri = "ws://localhost:8777"
        async with websockets.connect(uri) as websocket:
            await websocket.send(messageinput)
            response = await websocket.recv()
            print(f"Server response: {response}")
    else:
        print("Warning: Attempted to send an empty message.")

        
asyncio.get_event_loop().run_until_complete(send_message(" "))