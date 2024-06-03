from mubble import Dispatch, Message
from mubble.rules import StartCommand
from mubble.tools import ParseMode

dp = Dispatch()


@dp.message(StartCommand())
async def start_handler(message: Message):
    text = (
        "HI! 🐷"
    )
    await message.answer(
        text,
        parse_mode=ParseMode.HTML
    )
