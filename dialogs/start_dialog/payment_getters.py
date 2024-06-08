import random
from yoomoney import Quickpay, Client

from aiogram.types import User, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from database.db_conf import database
from states.start_group import startSG
db = database('users')


card: str = '4100118670194784'
price: dict[str, int] = {}
token = '4100118670194784.3BED92B83D591D395C33BD9C'


async def get_payment_links(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    labels = {
        'label_1': f'{event_from_user.id}_{random.randint(10000, 99999)}',
        'label_2': f'{event_from_user.id}_{random.randint(10000, 99999)}',
        'label_3': f'{event_from_user.id}_{random.randint(10000, 99999)}'
    }
    dialog_manager.dialog_data['labels'] = labels
    try:
        quickpay_1 = Quickpay(
            receiver=card,
            quickpay_form="shop",
            targets="Оплата определенной услуги",
            paymentType="SB",
            sum=50,
            label=labels['label_1']
        )
        quickpay_2 = Quickpay(
            receiver=card,
            quickpay_form="shop",
            targets="Оплата определенной услуги",
            paymentType="SB",
            sum=165,
            label=labels['label_2']
        )
        quickpay_3 = Quickpay(
            receiver=card,
            quickpay_form="shop",
            targets="Оплата определенной услуги",
            paymentType="SB",
            sum=470,
            label=labels['label_3']
        )

        return {'1_payment': quickpay_1.base_url,
                '2_payment': quickpay_2.base_url,
                '3_payment': quickpay_3.base_url,
                }
    except Exception as err:
        print(err)


async def check_pay(clb: CallbackQuery, btn: Button, dialog_manager: DialogManager, **kwargs):
    labels = dict(dialog_manager.dialog_data.items())
    print(labels)
    client = Client(token)
    history_1 = client.operation_history(label=labels['labels']['label_1'])
    history_2 = client.operation_history(label=labels['labels']['label_2'])
    history_3 = client.operation_history(label=labels['labels']['label_3'])

    for history in [history_1, history_2, history_3]:
        if not history.operations:
            continue
        else:
            if history.operations[0].status == 'success':
                if history.operations[0].label == labels['labels']['label_1']:
                    db.update_generates(user_id=clb.from_user.id, generates=5)
                elif history.operations[0].label == labels['labels']['label_2']:
                    db.update_generates(user_id=clb.from_user.id, generates=20)
                elif history.operations[0].label == labels['labels']['label_3']:
                    db.update_generates(user_id=clb.from_user.id, generates=100)
                await dialog_manager.switch_to(state=startSG.success_payment)
                return
    await dialog_manager.switch_to(state=startSG.unsuccess_payment)
    dialog_manager.dialog_data.clear()
