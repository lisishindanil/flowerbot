from mubble import Dispatch, CallbackQuery, ParseMode, WaiterMachine
from mubble.bot import MessageReplyHandler
from mubble.rules import CallbackData

from flowerbot.rules import IsCity
from flowerbot.keyboards import settings
from flowerbot.database import User

dp = Dispatch()
wm = WaiterMachine()


@dp.callback_query(CallbackData("settings"))
async def settings_handler(cq: CallbackQuery):
    await cq.edit_text(
        "<b>⚙️ Ви перейшли до налаштувань!</b>\n\n"
        "💡 Оберіть бажану опцію",
        reply_markup=settings,
        parse_mode=ParseMode.HTML
    )
    await cq.answer()


@dp.callback_query(CallbackData("settings_city"))
async def settings_city_handler(cq: CallbackQuery, user: User):
    await cq.edit_text(
        "<b>⚙️ Налаштування адреси доставки </b>\n\n"
        "💡 Введіть ваше місто доставки",
        reply_markup=settings,
        parse_mode=ParseMode.HTML
    )
    msg, _ = await wm.wait(
        dp.message,
        (cq.ctx_api, cq.chat_id.unwrap()),
        IsCity(),
        default=MessageReplyHandler("😔 Ваше місто не знайдено. Спробуйте написати по іншому."),
    )

    user.city = msg.text.unwrap()
    await user.save()

    await cq.edit_text(
        "Успішно!",
        reply_markup=settings,
        parse_mode=ParseMode.HTML
    )
    await cq.ctx_api.delete_message(msg.chat_id, msg.message_id)
    await cq.answer()