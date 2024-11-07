import ollama
import asyncio

class LLMModule:
    def __init__(self, model="qwen2.5:0.5b", system_prompt=None):
        self.model = model
        self.system_prompt = system_prompt

    async def get_llm_answer(self, input_data):
        message = [{"role": "user", "content": input_data}]
        if self.system_prompt:
            message.insert(0, {"role": "system", "content": self.system_prompt})
        
        response = await asyncio.to_thread(
            ollama.chat,
            model=self.model,
            messages=message
        )
        return response["message"]["content"]