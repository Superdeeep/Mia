import re
import logging
import asyncio
from multiprocessing import Process, Queue
from llm import LLMModule
from vtube_control import VTubeControl
from RealtimeTTS import TextToAudioStream, CoquiEngine
import time

def remove_emoji(text):
    emoji_pattern = re.compile("[\U00010000-\U0010FFFF]", flags=re.UNICODE)
    return emoji_pattern.sub(r"", text)

def llm_worker(input_queue, output_queue):
    llm_module = LLMModule()
    while True:
        message = input_queue.get()
        if message == "STOP":
            break
        answer = asyncio.run(llm_module.get_llm_answer(message))
        output_queue.put(answer)

def tts_worker(tts_queue, status_queue):
    engine = CoquiEngine(voice="./voice/ttz.wav", language="zh", speed=1.0, level=logging.INFO)
    stream = TextToAudioStream(engine)
    print("TTS流已准备")
    
    while True:
        text = tts_queue.get()
        if text == "STOP":
            break
        
        # Start playback and notify the main process
        stream.feed((text,)).play(log_synthesized_text=True)
        status_queue.put(True)  # Signal that playback has started
        
        # Monitor playback and update status_queue when finished
        while stream.is_playing():
            time.sleep(0.1)  # Small delay to avoid excessive polling
        status_queue.put(False)  # Signal that playback has finished

def vtube_worker(control_queue):
    vtube_control = VTubeControl(
        ws_address="ws://localhost:8001",
        Vtube_id="VTubeControlPlugin",
        Vtube_plugin_name="VTube模型控制插件",
        Vtube_plugin_developer="TArs",
    )
    token = asyncio.run(vtube_control.get_token())
    while True:
        command = control_queue.get()
        if command == "STOP":
            break
        asyncio.run(vtube_control.control_talking(token))

def main():
    message_queue = Queue()
    response_queue = Queue()
    tts_queue = Queue()
    control_queue = Queue()
    status_queue = Queue()

    llm_process = Process(target=llm_worker, args=(message_queue, response_queue))
    tts_process = Process(target=tts_worker, args=(tts_queue, status_queue))
    vtube_process = Process(target=vtube_worker, args=(control_queue,))

    llm_process.start()
    tts_process.start()
    vtube_process.start()

    try:
        while True:
            message = input("> ")
            if message == "exit":
                message_queue.put("STOP")
                tts_queue.put("STOP")
                control_queue.put("STOP")
                break
            message_queue.put(message)

            # Get response from LLM
            answer = response_queue.get()
            clean_answer = remove_emoji(answer)
            print(f"LLM回答: {clean_answer}")

            # Send clean_answer to TTS
            tts_queue.put(clean_answer)

            # VTube talking during TTS playback
            playback_active = True
            while playback_active:
                if not status_queue.empty():
                    playback_active = status_queue.get()

                if playback_active:
                    control_queue.put("TALK")
                    time.sleep(0.7)

    except KeyboardInterrupt:
        print("程序中断，关闭各模块！")
        message_queue.put("STOP")
        tts_queue.put("STOP")
        control_queue.put("STOP")

    llm_process.join()
    tts_process.join()
    vtube_process.join()

if __name__ == "__main__":
    main()
