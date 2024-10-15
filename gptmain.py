import asyncio
from vtube_control import VTubeControl
from RealtimeTTS import TextToAudioStream, CoquiEngine

def tts_feed_generator():
    yield "你好你好你好你好你好你好你好你好你好你好你好你好"

async def vtube_talking_control(vtube_control, token, should_talk_event):
    """Simulates controlling talking in VTube Studio."""

    while True:
        if should_talk_event.is_set():
            await vtube_control.control_talking(token)
            print("VTube is talking...")
        await asyncio.sleep(0.3)

async def main():
    # Create a flag for controlling when VTube should talk
#####

    engine = CoquiEngine(voice="./voice/ttz.wav", language="zh", speed=1.0)
    stream = TextToAudioStream(engine)
#####

    vtube_control = VTubeControl(
        ws_address="ws://localhost:8001",
        Vtube_id="VTubeControlPlugin",
        Vtube_plugin_name="VTube模型控制插件",
        Vtube_plugin_developer="TArs"
    )
    token = await vtube_control.get_token()

    should_talk_event = asyncio.Event()

    # Start the talking control task
    asyncio.create_task(vtube_talking_control(vtube_control, token, should_talk_event))

    while True:
        # Simulate user input and TTS playback
        input("Press Enter to simulate TTS playback...")

        # Simulate TTS is playing
        
        print("TTS is playing...")

        # Simulate waiting for TTS to finish
        stream.feed(tts_feed_generator())  # Wait for 2 seconds as if TTS is playing
        stream.play_async()

        while stream.is_playing():
            should_talk_event.set()  # VTube should talk while audio is playing
            await asyncio.sleep(0.1)  # Yield control

        # Double-check the state after exiting the loop
        await asyncio.sleep(0.1)
        if not stream.is_playing():
            should_talk_event.clear()  # Stop VTube talking if playback has stopped
            print("TTS playback finished.")

if __name__ == "__main__":
    asyncio.run(main())
