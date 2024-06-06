from mubble import Dispatch, CallbackQuery
from mubble.rules import CallbackData

from flowerbot.keyboards import back_to_menu

dp = Dispatch()

@dp.callback_query(CallbackData("catalog"))
async def catalog_handler(cq: CallbackQuery):
    await cq.edit_text(
        "POSHOL NAHUI",
        reply_markup=back_to_menu
    )
    await cq.answer()