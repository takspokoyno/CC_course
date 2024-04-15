import config
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

openai.api_key = config.OPENAI_API_KEY

MAX_MESSAGE_LENGTH = 3000

@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply('Hello! I\'m GPT chat bot. Ask me something')

@dp.message_handler()
async def gpt(message: types.Message):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message.text}
        ],
        temperature=0.01,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    response = completion.choices[0].message["content"].strip()

    if len(response) > MAX_MESSAGE_LENGTH:
        chunks = [response[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(response), MAX_MESSAGE_LENGTH)]
        for chunk in chunks:
            await message.reply(chunk)
    else:
        await message.reply(response)



if __name__ == "__main__":
    executor.start_polling(dp)