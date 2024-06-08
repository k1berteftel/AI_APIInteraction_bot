from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from states.start_group import adminSG
from database.db_conf import database

db = database('users')


async def send_static(clb: CallbackQuery, btn: Button, dialog_manager: DialogManager, **kwargs):
    paid_users = db.get_paid_users()
    free_users = db.get_free_users()
    await clb.message.answer(f'Юзеры без генераций: {free_users}\nЮзеры с приобретенными генерациями: {paid_users}')


async def save_message(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['message'] = message
    await dialog_manager.switch_to(adminSG.accept)


async def send_message(clb: CallbackQuery, btn: Button, dialog_manager: DialogManager, **kwargs):
    message: Message = dialog_manager.dialog_data.get('message')
    users: list[tuple[int]] = db.get_users()

    for user_id in users:
        try:
            await message.send_copy(user_id[0])
        except Exception:
            continue
    await clb.answer('Рассылка прошла успешно')
    await dialog_manager.start(state=adminSG.start, mode=StartMode.RESET_STACK)