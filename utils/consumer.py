import asyncio
import json
import os

import aiormq
from aiogram import Bot
from aiogram.types import FSInputFile
from aiormq.abc import DeliveredMessage

from generate_proccess import generate_process, add_watermark


async def on_message(message: DeliveredMessage):
    body: dict = json.loads(message.body.decode('utf-8'))
    print(body)
    bot: Bot = Bot(token='7198512177:AAH4cQW_nvA0L6p5-3WcL8BZQXN8FfvV25A')
    path = os.path.abspath('')
    target_image = open(fr'{path[0:-5]}\{body["target_image"]}', 'rb')
    swap_image = open(fr'{path[0:-5]}\{body["swap_image"]}', 'rb')
    print(type(target_image))
    image_url = generate_process(target_image, swap_image)
    if body['watermark']:
        text = 'Твоя генерация готова!\nОна бесплатная, доступна 1 раз в сутки. Чтобы убрать вотермарк и получить это и другие фото в хорошем качестве, нажми на кнопку "Купить генерации"'
        img_path = add_watermark(image_url)
        await bot.send_photo(chat_id=body['user_id'], photo=FSInputFile(path=img_path), caption=text)
    else:
        await bot.send_photo(chat_id=body['user_id'], photo=image_url, caption='Твоя генерация готова!')
    try:
        os.remove(fr'{path[0:-5]}\{body["target_image"]}')
        os.remove(fr'{path[0:-5]}\{body["swap_image"]}')
    except Exception as err:
        print(err)

    await message.channel.basic_ack(delivery_tag=message.delivery.delivery_tag)


async def main():
    connection = await aiormq.connect("amqp://quest:quest@localhost/")

    channel = await connection.channel()

    await channel.exchange_declare("basic_exchange", exchange_type="direct")

    declare_ok = await channel.queue_declare('basic_queue')

    await channel.queue_bind(
        queue=declare_ok.queue,
        exchange="basic_exchange",
        routing_key="routing_key"
    )

    await channel.basic_qos(prefetch_count=1)
    await channel.basic_consume(declare_ok.queue, on_message, no_ack=False)
    await asyncio.Future()


asyncio.run(main())
