import datetime
import os

from aiogram import Bot
from aiogram.types import User, Message, ContentType
from aiogram_dialog import ShowMode, DialogManager
from aiogram_dialog.api.entities import MediaId, MediaAttachment
from aiogram_dialog.widgets.input import MessageInput

from config_data.config import load_config, Config
from database.db_conf import database
from states.start_group import startSG
from utils.date_func import get_succes
from utils.generate_proccess import generate_process, add_watermark

config: Config = load_config()
db = database('users')


async def get_image(event_from_user: User, **kwargs):
    refferals: int = db.get_referrals(event_from_user.id)
    if refferals >= 2:
        db.update_generates(user_id=event_from_user.id, generates=3)
        db.add_referrals(event_from_user.id, -2)

    try:
        os.remove(f'{event_from_user.id}.png')
    except Exception as err:
        print(err)

    img_id = 'AgACAgIAAxkBAAIBqWZRrEc_J44bQuI55Vrknx5AUt3fAAJ33TEb_yqJSisYFsX9wwL6AQADAgADcwADNQQ'
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(img_id))
    return {'photo': image}


async def get_generations(event_from_user: User, **kwargs):
    generates: int = db.get_generates(event_from_user.id)
    free_generations: int | bool = get_succes(user_id=event_from_user.id, db=db)
    if generates:
        text = f'<b>Тебе доступно {generates} генераций без водяных знаков</b>\n\n' \
               f'Если нужно больше, нажми кнопку <b>«Купить генерации»</b> или получи 🎁 подарочные.'
        return {'generations': text}
    elif free_generations:
        text = '<b>Так, я вижу, что у тебя есть 1 генерация и она бесплатная 😌</b>\n\n' \
               'Это значит, что ты можешь за сутки сделать всего 1 фото с заменой лица и водяным знаком.\n\n' \
               'Чтобы снять ограничение и делать фото без водяных знаков, нажми кнопку <b>«Купить генерации»</b> или получи 🎁 подарочные.'
        return {'generations': text}
    else:
        text = '<b>А все, генераций нет. Одна генерация будет тебе начислена в течение 24 часов, но с водяным знаком.</b>\n\n' \
               'Чтобы снять ограничение и делать фото без водяных знаков, нажми кнопку <b>«Купить генерации»</b> или получи 🎁 подарочные.'
        return {'generations': text}


async def input_getter1(event_from_user: User, **kwargs):
    img_id = 'AgACAgIAAxkBAAIBvGZRt0MsdcI3vr1H4yLtOnoTtGG6AAI81zEb7sSQSgxq-zz1tt9pAQADAgADcwADNQQ'
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(img_id))
    if db.get_generates(event_from_user.id) or get_succes(event_from_user.id, db=db):
        text = 'Иууууу! Поехали!\n\n1️⃣ Для начала, отправь фотографию, на которой хочешь изменить лицо.\n\n' \
               '<em>* фото нигде не хранится и его никто не увидит, мы обещаем</em> \n\n<b>🔥 Важные рекомендации:</b>\n\n' \
               '<em>— Фотография должна быть хорошего качество</em>\n\n' \
               '<em>— Обрати внимание, чтобы на фото хорошо было видно само лицо. Желательно без лишних объектов, рук, засветов</em>\n\n' \
               '<em>— Отправляй фотографией, а не файлом </em>\n\n<b>Жду фото 👇</b>'
        return {'text': text,
                'photo': image,
                'is_generations': True}
    text = '<b>А все, генераций нет. Одна генерация будет тебе начислена в течение 24 часов, но с водяным знаком.</b>\n\n' \
           'Чтобы снять ограничение и делать фото без водяных знаков, нажми кнопку <b>«Купить генерации»</b> или получи 🎁 подарочные.'
    return {'text': text,
            'photo': image,
            'is_generations': False}


async def ref_getter(event_from_user: User, **kwargs):
    return {'link': db.get_deeplink(user_id=event_from_user.id)}


async def first_success_get(message: Message, widget: MessageInput, dialog_manager: DialogManager, *args,
                            **kwargs) -> None:
    if not get_succes(message.from_user.id, db=db) and not db.get_generates(message.from_user.id):
        await message.answer('У вас отсутствуют генерации')
        return

    referral: int = db.get_referral(message.from_user.id)
    if referral:
        db.add_referrals(referral, refferals=1)
        db.add_referral(user_id=message.from_user.id, referral=0)

    if db.get_generates(message.from_user.id):
        db.update_generates(message.from_user.id, -1)
        dialog_manager.dialog_data['watermark'] = 0
    else:
        db.update_data(data=str(datetime.date.today()), user_id=message.from_user.id)
        dialog_manager.dialog_data['watermark'] = 1

    dialog_manager.show_mode = ShowMode.NO_UPDATE  # Вот эту строку нужно добавить
    bot: Bot = dialog_manager.middleware_data.get('bot')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, f'first_{message.from_user.id}.jpg')
    dialog_manager.dialog_data['target_image'] = f'first_{message.from_user.id}.jpg'

    text = 'Хорошо. Теперь последний шаг!\n\n2️⃣ Отправь фотографию лица, которое ты хочешь наложить.\n\n' \
           '<em>* фото нигде не хранится и его никто не увидит, мы обещаем</em>\n\n<b>🔥 Важные рекомендации:</b>\n\n' \
           '<em>— Фотография должна быть хорошего качества</em>\n\n' \
           '<em>— Обрати внимание, чтобы на фото хорошо было видно само лицо. Желательно без лишних объектов, рук, засветов </em>\n\n' \
           '<em>— Отправляй фотографией, а не файлом </em>\n\n<em>— Желательно фото лица делать с прямого ракурса </em>\n\n<b>Жду лицо 👇</b>'
    await message.answer_photo(
        photo='AgACAgIAAxkBAAIBvmZRt0WP7Xg9-Tjn-4SDLGjcbyAOAAI91zEb7sSQSsnYdQYhl6IyAQADAgADcwADNQQ', caption=text)
    await dialog_manager.next()


async def second_success_get(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.show_mode = ShowMode.AUTO
    bot: Bot = dialog_manager.middleware_data.get('bot')

    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, f'second_{message.from_user.id}.jpg')

    dialog_manager.dialog_data['swap_image'] = f'second_{message.from_user.id}.jpg'
    # dialog_manager.dialog_data['user_id'] = message.from_user.id
    await dialog_manager.switch_to(state=startSG.success_generate)


async def generate_getter(dialog_manager: DialogManager, **kwargs):
    event_from_user: User = dialog_manager.middleware_data.get('event_from_user')
    bot: Bot = dialog_manager.middleware_data.get('bot')
    info = dict(dialog_manager.dialog_data.items())
    print(info)

    await bot.send_message(chat_id=event_from_user.id,
                           text='Все! Теперь дай минутку нашему пластическому хирургу, чтобы он заменил лицо ❤️')

    target_img_path = dialog_manager.dialog_data.get("target_image")
    swap_img_path = dialog_manager.dialog_data.get("swap_image")

    target_image = open(target_img_path, 'rb')
    swap_image = open(swap_img_path, 'rb')
    image_url = await generate_process(target_image, swap_image)

    target_image.close()
    swap_image.close()

    try:
        os.remove(target_img_path)
        os.remove(swap_img_path)
    except Exception as err:
        print(err)

    if not image_url:
        if dialog_manager.dialog_data.get("watermark"):
            db.update_data(None, user_id=event_from_user.id)
        else:
            db.update_generates(event_from_user.id, 1)
        text = '😢 К сожалению, нейросеть не смогла рассмотреть лицо. Попробуйте сгенерировать с другими фото'
        return {'text': text,
                'is_image': False}

    if dialog_manager.dialog_data.get("watermark"):
        img_path = add_watermark(image_url, event_from_user.id)
        text = '<b>Твоя генерация готова 🥳</b>\n\nНо она с водяным знаком(((\n\n' \
               'Чтобы снять ограничение и делать фото без водяных знаков, нажми кнопку <b>«Купить генерации»</b> или получи 🎁 подарочные.'
        image = MediaAttachment(ContentType.PHOTO, path=img_path)
        return {'text': text,
                'image': image,
                'is_image': True}
    else:
        image = MediaAttachment(ContentType.PHOTO, url=image_url)
        text = f'<b>Твоя генерация готова 🥳</b>\n\nУ тебя осталось: {db.get_generates(event_from_user.id) if db.get_generates(event_from_user.id) else 1} генераций\n\n' \
               f'Нажми кнопку ниже «Сгенерировать» и давай сделаем еще.\n\n' \
               f'Самые интересные работы мы можем выложить на канал <a href="https://t.me/choslic">«Че с лицом?»</a> и подарить за это доп. генерации.'
        return {'text': text,
                'image': image,
                'is_image': True}
