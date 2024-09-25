import logging
import asyncio
from RealtimeTTS import TextToAudioStream, CoquiEngine

class TTSModule:
    def __init__(self, voice_path, language="zh", speed=1.0, log_level=logging.INFO):
        self.voice_path = voice_path
        self.language = language
        self.speed = speed
        self.engine = None
        self.stream = None
        #self.is_playing = False
        logging.basicConfig(level=log_level)


    
    def initialize(self):
        self.engine = CoquiEngine(voice=self.voice_path, language=self.language, speed=self.speed)
        self.stream = TextToAudioStream(self.engine)
        print("TTS流已准备")
        
    
    def tts_generator(self, answer):
        yield answer
        
    def play_tts(self, generator):
        """播放音频流"""
        self.stream.feed(generator)
        self.stream.play_async()
        
        
    async def play_and_report_status(self, answer_generator):
        """播放音频流，并持续报告播放状态"""
        # 向流中添加音频
        self.stream.feed(answer_generator)
        self.stream.play_async()

        # 持续报告 `is_playing` 的状态
        while self.is_playing():
            await asyncio.sleep(0.1)  # 每 0.1 秒检查一次状态

    def is_playing(self):
        """检查 TTS 是否正在播放"""
        return self.stream.is_playing()
        