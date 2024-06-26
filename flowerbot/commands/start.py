from mubble import Dispatch, Message, CallbackQuery
from mubble.rules import StartCommand, CallbackData
from mubble.tools import ParseMode

from flowerbot.keyboards import menu

dp = Dispatch()


@dp.message(StartCommand())
async def start_handler(message: Message):
    text = (
        "<b>🙉 Дорогий друже, вітаю тебе!</b>\n\n"
        "🌺 Я спеціалізуюсь на замовленнях квітів! Ми пропонуємо широкий асортимент квіткових композицій, які можуть стати чудовим подарунком для будь-якої події.\n\n"
        "Квіти завжди були символом любові, ніжності та поваги, тому ми прагнемо забезпечити найвищу якість обслуговування та доставку квітів.\n\n"
        "<blockquote>💡 Перед замовленням не забудь вказати місто в налаштуваннях. Це дуже важливо, адже ми хочемо бути впевненими, що твоє замовлення буде доставлено вчасно і в потрібне місце. Завжди перевіряй, щоб усі дані були вказані правильно.</blockquote>\n\n"
        "З радістю допоможемо тобі обрати найкращий букет! Якщо у тебе є які-небудь питання або потрібна допомога, не соромся звертатися до нашої служби підтримки.\n\n"
        "Бажаємо тобі гарного дня та чудового настрою! 😊\n\n"
        "З найкращими побажаннями, твоя команда з доставки квітів."
    )

    await message.answer(
        text,
        reply_markup=menu,
        parse_mode=ParseMode.HTML
    )


@dp.callback_query(CallbackData("menu"))
async def menu_handler(cq: CallbackQuery):
    await cq.delete()

    text = (
        "<b>🙉 Дорогий друже, вітаю тебе!</b>\n\n"
        "🌺 Я спеціалізуюсь на замовленнях квітів! Ми пропонуємо широкий асортимент квіткових композицій, які можуть стати чудовим подарунком для будь-якої події.\n\n"
        "Квіти завжди були символом любові, ніжності та поваги, тому ми прагнемо забезпечити найвищу якість обслуговування та доставку квітів.\n\n"
        "<blockquote>💡 Перед замовленням не забудь вказати місто в налаштуваннях. Це дуже важливо, адже ми хочемо бути впевненими, що твоє замовлення буде доставлено вчасно і в потрібне місце. Завжди перевіряй, щоб усі дані були вказані правильно.</blockquote>\n\n"
        "З радістю допоможемо тобі обрати найкращий букет! Якщо у тебе є які-небудь питання або потрібна допомога, не соромся звертатися до нашої служби підтримки.\n\n"
        "Бажаємо тобі гарного дня та чудового настрою! 😊\n\n"
        "З найкращими побажаннями, твоя команда з доставки квітів."
    )
    await cq.ctx_api.send_message(
        chat_id=cq.chat_id,
        text=text,
        reply_markup=menu,
        parse_mode=ParseMode.HTML
    )