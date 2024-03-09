import asyncio
import websockets
import json
import os
import random
from RealtimeTTS import TextToAudioStream, CoquiEngine
import time
import ollama

class ChatServer:
    def __init__(self):
        self.answer = ""
        self.coqui_engine = CoquiEngine(voice="neuro.wav", language="en", speed=1.0)

    async def handle_connection(self, websocket, path):
        async for message in websocket:
            print(f"Received message: {message}")
            self.answer = self.test_ollama(message)
            await websocket.send(f"Server received ok ")

    def test_ollama(self, inputdata):
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

    def dummy_generator(self):
        yield self.answer

    async def run_coqui_engine(self):
        while True:
            await asyncio.sleep(5)
            if self.answer != "":
                stream = TextToAudioStream(self.coqui_engine)
                stream.feed(self.dummy_generator()).play(log_synthesized_text=True)
                self.answer = ""

    async def start_server(self):
        start_server = websockets.serve(self.handle_connection, "localhost", 8765)
        await asyncio.gather(start_server, self.run_coqui_engine())

if __name__ == "__main__":
    chat_server = ChatServer()
    asyncio.run(chat_server.start_server())
