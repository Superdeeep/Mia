import asyncio
from vtube_control import VTubeControl
from tts import TTSModule
from llm import LLMModule

async def main():
    # 初始化各模块
    vtube_control = VTubeControl(
        ws_address="ws://localhost:8001",
        Vtube_id="VTubeControlPlugin",
        Vtube_plugin_name="VTube模型控制插件",
        Vtube_plugin_developer="TArs"
    )
    
    tts_module = TTSModule(voice_path="./voice/ttz.wav")
    tts_module.initialize()

    llm_module = LLMModule(system_prompt="你的名字叫妙芽，你喜欢骑自行车")

    # 获取VTube的token
    token = await vtube_control.get_token()

    while True:
        # 获取用户输入
        message = input("> ")
        # LLM获取回答
        answer = await llm_module.get_llm_answer(message)
        print(f"LLM回答: {answer}")
        
        await vtube_control.control_talking(token,tts_module,answer)
        
        
        
        
        #tts_module.play_tts(tts_module.tts_generator(answer))
        #
        #while tts_module.is_playing():
        #    print("TTS is playing...")
        #    await asyncio.sleep(0.3)  # 每隔0.3秒检查一次状态
#
        # 控制VTube Studio模型说话
         #   await vtube_control.control_talking(token)#, tts_module.stream, tts_module.tts_generator(answer))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序中断，关闭TTS引擎")
