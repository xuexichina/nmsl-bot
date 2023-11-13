import hashlib
import logging
import os
import random
from typing import List

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChosenInlineResult, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from httpx import AsyncClient

from .corpus import Corpus, UpdateException
from .logger import InlineLogger

API_TOKEN = os.environ["API_TOKEN"]
PROXY = os.environ.get("PROXY", None)

bot = Bot(token=API_TOKEN, proxy=PROXY)
dp = Dispatcher(bot)

answer_map = {}


async def update_corpus():
    try:
        logging.warning("Updating corpus.")
        await corpus.update()
        logging.info("Corpus updated.")
    except UpdateException:
        logging.exception("Failed to update corpus.")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Hi!\nI'm bot")

@dp.message_handler(commands=['location'])
async def send_welcome(message: types.Message):
    await message.answer("Sending your location via map here!")

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    reply = "latitude:  {}\nlongitude: {}".format(lat, lon)
    await message.answer(reply, reply_markup=types.ReplyKeyboardRemove())

@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    text = inline_query.query
    answers: List[str] = [sentence for sentence in corpus.common if text in sentence] if text else corpus.common
    try:
        answers = sorted(random.sample(answers, 5))
    except ValueError:
        answers = sorted(answers[:5])

    answers_hash = {answer: hashlib.md5(answer.encode()).hexdigest() for answer in answers}
    for answer, _hash in answers_hash.items():
        answer_map[_hash] = answer

    items = [InlineQueryResultArticle(
        id=_hash,
        title=answer,
        input_message_content=InputTextMessageContent(answer)
    ) for answer, _hash in answers_hash.items()]

    await bot.answer_inline_query(inline_query.id, results=items, cache_time=10, is_personal=True)


@dp.chosen_inline_handler()
async def inline_choice(result: ChosenInlineResult):
    await logger.log(answer_map.get(result.result_id, -1),
                     hashlib.md5(result.from_user.id.to_bytes(16, "little", signed=False)).hexdigest())


logger = InlineLogger(os.environ["LOG_FILE"])
scheduler = AsyncIOScheduler()
scheduler.add_job(update_corpus, "interval", minutes=10)
scheduler.add_job(update_corpus)
corpus = Corpus()
http = AsyncClient()
scheduler.start()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
