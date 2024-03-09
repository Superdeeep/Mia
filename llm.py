import asyncio
import websockets
import json
from asyncio import sleep
import os
import random
import numpy as np
import ollama

def test_ollama():
   response = ollama.chat(model='gemma:2b', messages=[
  {
    'role': 'user',
    'content': 'how is going?',
  },
])
   print(response['message']['content'])
   return response['message']['content']

def dummy_generator():
        myol=test_ollama()
        yield myol



if __name__ == '__main__':
    from RealtimeTTS import TextToAudioStream, CoquiEngine

    coqui_engine = CoquiEngine(voice="neuro.wav", language="en", speed=1.0)
    stream = TextToAudioStream(coqui_engine)
    stream.feed(dummy_generator()).play(log_synthesized_text=True)
    coqui_engine.shutdown()


