from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Row, Url, Back, Column, Button
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput

from states.start_group import adminSG
from dialogs.admin_dialog.getters import send_static, save_message, send_message


admin_dialog = Dialog(
    Window(
        Const('Админская панель'),
        Column(
            Button(Const('Получить статистику'), id='get_static', on_click=send_static),
            SwitchTo(Const('Сделать рассылку'), id='malling', state=adminSG.malling)
        ),
        state=adminSG.start
    ),
    Window(
        Const('Отправьте сообщение которое хотите разослать'),
        SwitchTo(Const('Отмена'), id='cancel', state=adminSG.start),
        MessageInput(
            func=save_message,
            content_types=ContentType.ANY
        ),
        state=adminSG.malling
    ),
    Window(
        Const('Вы подтверждаете рассылку данного сообщения?'),
        Row(
            Button(Const('Да'), id='accept', on_click=send_message),
            SwitchTo(Const('Нет'), id='back', state=adminSG.start)
        ),
        state=adminSG.accept
    )
)