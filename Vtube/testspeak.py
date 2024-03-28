import time
import logging
import asyncio
from RealtimeTTS import TextToAudioStream, CoquiEngine

stream = None

def dummy_generator():
    yield "Hey guys! These here are realtime spoken sentences based on local text synthesis. "

async def play_realtime_tts_ready():
    global stream
    logging.basicConfig(level=logging.INFO)
    engine = CoquiEngine(level=logging.INFO)

    stream = TextToAudioStream(engine)

    print("stream is ready")
    stream.feed(dummy_generator()).play(log_synthesized_text=True)


async def play_realtime_tts():
    global stream
    stream.feed(dummy_generator())
    stream.play_async()
    print("Starting to play stream")
    # 等待音频播放完成
    while stream.is_playing():
        print("no")
        await asyncio.sleep(0.1)
    #stream.play(log_synthesized_text=True)
    print("yes")
    return "finish"

    

if __name__ == '__main__':
    play_realtime_tts_ready()
