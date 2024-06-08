from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Row, Url, Back, Column, Button
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.start_dialog.getters import get_generations, first_success_get, second_success_get, get_image, input_getter1, ref_getter, generate_getter
from dialogs.start_dialog.payment_getters import get_payment_links, check_pay
from Lexicon.lexicon_ru import messages, buttons
from states.start_group import startSG

start_dialog = Dialog(
    Window(
        DynamicMedia('photo'),
        Const(messages['hello']),
        Column(
            SwitchTo(text=Const(buttons['generates']), id='generates', state=startSG.generates),
            SwitchTo(text=Const(buttons['chose_rates']), id='chose_rates', state=startSG.chose_generates),
            SwitchTo(text=Const(buttons['generate']), id='generate', state=startSG.generate),
            SwitchTo(text=Const(buttons['ref_program']), id='ref_program', state=startSG.ref_program),
            Url(Const('Помощь'), url=Const(text='https://t.me/chslicadm')),
        ),
        getter=get_image,
        state=startSG.start
    ),
    Window(
        Format('{generations}'),
        Column(
            SwitchTo(text=Const('Приобрести генерации'), id='chose_rates', state=startSG.chose_generates),
            SwitchTo(text=Const(buttons['ref_program']), id='ref_program', state=startSG.ref_program),
            Back(Const('Назад'), id='back'),
        ),
        getter=get_generations,
        state=startSG.generates
    ),
    Window(
        Const('<b>Хочешь больше генераций и без водяных знаков?</b> \n\n'
              'Выбери один из тарифов ниже по кнопке. Цена смешная и дешевле большинства нейросетей + у нас лучшее качество.\n\n'
              'Оплата доступна пока через кошелек Юмани или банковскую карту \n\n'
              '<b>Сколько генераций хочешь купить? 👇</b>\n\n'
              '❗️Важно! После оплаты обязательно нажми кнопку «Проверить пополнение», иначе генерации не поступят.'),
        Column(
            Url(text=Const('5 генераций = 50₽'), url=Format('{1_payment}'),  id='rate_1'),
            Url(text=Const('20 генераций = 165₽'), url=Format('{2_payment}'),  id='rate_2'),
            Url(text=Const('100 генераций = 470₽'), url=Format('{3_payment}'),  id='rate_3'),
            Button(text=Const('Проверить пополнение'), id='check_pay', on_click=check_pay),
            SwitchTo(Const('Назад'), id='back', state=startSG.start)
        ),
        getter=get_payment_links,
        state=startSG.chose_generates
    ),
    Window(
        Format('<b>Хочешь получить 3 генерации (без водяных знаков) бесплатно? </b>\n\n'
               '❤️ Просто пригласи 2 друзей, чтобы они воспользовались ботом. Вот твоя специальная пригласительная ссылка: {link}\n\n'
               '<em>(генерации автоматически начисляются, как только 2+ твоих друга запустят бота и сделают минимум 1 генерацию, даже бесплатную)</em>'),
        SwitchTo(Const('Назад'), id='back', state=startSG.start),
        getter=ref_getter,
        state=startSG.ref_program

    ),
    Window(
        DynamicMedia(selector='photo', when='is_generations'),
        Format('{text}'),
        Url(Const('Помощь'), url=Const(text='https://t.me/chslicadm')),
        SwitchTo(Const('Назад'), id='back', state=startSG.start),
        MessageInput(
            func=first_success_get,
            content_types=ContentType.PHOTO
        ),
        # Реализация разных сообщений с форматированием для количества использований
        # Так же реализация сбора информации для работы с апи
        getter=input_getter1,
        state=startSG.generate
    ),
    Window(
        MessageInput(
            func=second_success_get,
            content_types=ContentType.PHOTO
        ),
        state=startSG.generate_2
    ),
    Window(
        Const('✅ Оплата пришла.\n\nСпасибо! Теперь мы сможем купить себе хлеб, а ты можешь начать <b>«Генерировать»</b>'),
        Column(
            SwitchTo(text=Const(buttons['generates']), id='generates', state=startSG.generates),
            SwitchTo(text=Const(buttons['generate']), id='generate', state=startSG.generate),
            SwitchTo(text=Const(buttons['ref_program']), id='ref_program', state=startSG.ref_program),
            Url(Const('Помощь'), url=Const(text='https://t.me/chslicadm')),
            SwitchTo(text=Const('Назад'), id='back', state=startSG.start)
        ),
        state=startSG.success_payment
    ),
    Window(
        Const('❌ Не вижу оплату!\n\nПодождите еще немного и еще раз нажмите кнопку для проверки.\n\n'
              'Если есть сложности, позовите на <b>«Помощь»</b>'),
        Column(
            SwitchTo(text=Const(buttons['generates']), id='generates', state=startSG.generates),
            SwitchTo(text=Const(buttons['generate']), id='generate', state=startSG.generate),
            SwitchTo(text=Const(buttons['ref_program']), id='ref_program', state=startSG.ref_program),
            Url(Const('Помощь'), url=Const(text='https://t.me/chslicadm')),
            SwitchTo(text=Const('Назад'), id='back', state=startSG.start)
        ),
        state=startSG.unsuccess_payment
    ),
    Window(
        DynamicMedia(selector='image', when='is_image'),
        Format('{text}'),
        Column(
            SwitchTo(text=Const(buttons['generates']), id='generates', state=startSG.generates),
            SwitchTo(text=Const(buttons['chose_rates']), id='chose_rates', state=startSG.chose_generates),
            SwitchTo(text=Const(buttons['generate']), id='generate', state=startSG.generate),
            SwitchTo(text=Const(buttons['ref_program']), id='ref_program', state=startSG.ref_program),
            Url(Const('Помощь'), url=Const(text='https://t.me/chslicadm'))
        ),
        getter=generate_getter,
        state=startSG.success_generate
    )
)
