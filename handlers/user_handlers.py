from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from database.db_conf import database

from states.start_group import startSG, adminSG
from utils.moduls import add_deeplink
from config_data.config import load_config, Config

config: Config = load_config()


db = database('users')
user_router = Router()

@user_router.message(CommandStart())
async def start_dialog(msg: Message, dialog_manager: DialogManager, command: CommandObject):
    if not db.check_user(msg.from_user.id):
        args = command.args
        db.add_user(msg.from_user.id)
        add_deeplink(user_id=msg.from_user.id)
        if args:
            db.add_referral(msg.from_user.id, referral=int(args))
    if msg.from_user.id in config.bot.admin_ids:
        await dialog_manager.start(state=adminSG.start, mode=StartMode.RESET_STACK)
    await dialog_manager.start(state=startSG.start, mode=StartMode.NEW_STACK)


