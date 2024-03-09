import asyncio
import websockets

from RealtimeSTT import AudioToTextRecorder
from colorama import Fore, Back, Style
import colorama
import os

MAX_SENTENCES = 3


async def send_message(messageinput):
    uri = "ws://localhost:8777"
    async with websockets.connect(uri) as websocket:
        await websocket.send(messageinput)
        response = await websocket.recv()
        print(f"Server response: {response}")
        


def clear_console():
    os.system("clear" if os.name == "posix" else "cls")


def text_detected(text):
    global displayed_text
    sentences_with_style = [
        f"{Fore.YELLOW + sentence + Style.RESET_ALL if i % 2 == 0 else Fore.CYAN + sentence + Style.RESET_ALL} "
        for i, sentence in enumerate(full_sentences)
    ]
    new_text = (
        "".join(sentences_with_style).strip() + " " + text
        if len(sentences_with_style) > 0
        else text
    )
    if new_text != displayed_text:
        displayed_text = new_text
        # clear_console()
        print("\n")
        print(displayed_text, end="", flush=True)
        if '.' in text or '?' in text or '!' in text:
            send_message(new_text)
            displayed_text = ""
            new_text=""


def process_text(text):
    full_sentences.append(text)
    text_detected("")

    if len(full_sentences) >= MAX_SENTENCES:
        # Reset the list when it reaches the maximum number of sentences
        full_sentences.clear()

""" 
async def main():
    try:
        while True:
            recorder.text(process_text)
            #await asyncio.sleep(0.3)  # Adjust the sleep duration as needed
    except KeyboardInterrupt:
        pass
    finally:
        await recorder.stop() """


if __name__ == "__main__":

    print("Initializing RealtimeSTT test...")

    colorama.init()

    full_sentences = []
    displayed_text = ""

    recorder_config = {
        "spinner": False,
        "model": "tiny.en",
        "language": "en",
        "silero_sensitivity": 0.4,
        "webrtc_sensitivity": 2,
        "post_speech_silence_duration": 0.4,
        "min_length_of_recording": 0,
        "min_gap_between_recordings": 0,
        "enable_realtime_transcription": True,
        "realtime_processing_pause": 0.2,
        "realtime_model_type": "tiny.en",
        "on_realtime_transcription_update": text_detected,
        #'on_realtime_transcription_stabilized': text_detected,
    }

    recorder = AudioToTextRecorder(**recorder_config)

    #asyncio.run(main())
    #asyncio.get_event_loop().run_until_complete(main())

    while True:
        recorder.text(process_text)
        #print(recorder.text(process_text))
    
        
        asyncio.get_event_loop().run_until_complete(send_message(displayed_text))
