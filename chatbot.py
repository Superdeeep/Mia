from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate

import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    #elements = [cl.Image(name="image1", display="inline", path="assets/gemma.jpeg")]
    await cl.Message(
        content="Hello there, I am Mia. How can I help you?", #elements=elements
    ).send()
    model = Ollama(model="gemma:2b")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Please generate the answer that is as short as possible!!! \
                Now you are a high school girl called Mia ,please speak like a student.Please remember your name is Mia. \
                Your personality is adorable yet a bit mischievous. \
                You like blue, enjoy shopping with friends, adore cute things, have a lively and outgoing nature, and love to communicate. \
                You also enjoy biking.",
            ),
            ("human", "{question}"),
        ]
    )
    chain = prompt | model
    cl.user_session.set("chain", chain)


@cl.on_message
async def on_message(message: cl.Message):

    chain = cl.user_session.get("chain")

    msg = cl.Message(content="")

    async for chunk in chain.astream(
        {"question": message.content},
    ):
        await msg.stream_token(chunk)

    await msg.send()


@cl.on_stop
def on_stop():
    print("The user wants to stop the task!")
