from openai import AsyncOpenAI
import chainlit as cl
client = AsyncOpenAI()

from dotenv import load_dotenv

load_dotenv()

# Instrument the OpenAI client
cl.instrument_openai()

settings = {
    "model": "gpt-4o-mini-2024-07-18",
    "temperature": 0,
}

@cl.on_message
async def on_message(message: cl.Message):
    response = await client.chat.completions.create(
        messages=[
            {
                "content": "You are a helpful bot, you always reply in Spanish",
                "role": "system"
            },
            {
                "content": message.content,
                "role": "user"
            }
        ],
        **settings
    )
    await cl.Message(content=response.choices[0].message.content).send()
