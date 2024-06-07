import datetime

from mubble import Dispatch, CallbackQuery, ParseMode
from mubble.rules import CallbackData

from flowerbot.database.user import User
from flowerbot.keyboards import cart, cart_order, menu

dp = Dispatch()


def get_products_text(cart: list[dict]) -> list[str, int | float, int | float]:
    text, order_price, total_count = "", 0, 0
    for i, product in enumerate(cart, 1):
        text += f"{i}.| Назва: {product['name']}, ціна - {product['total_price']}, кількість букетів - {product['count']} \n"
        order_price += product['total_price']
        total_count += product['count']

    return [text, order_price, total_count]


@dp.callback_query(CallbackData("cart"))
async def cart_handler(cq: CallbackQuery, user: User):
    products_text, _, _ = get_products_text(user.cart)

    await cq.edit_text(
        "<b>💫 Кошик:</b>\n\n"
        "Ось ваші обрані товари:\n"
        f"<blockquote>{products_text if products_text else 'Ви ще не додали товари'}</blockquote>"
        "\n\n<b>Що далі?</b>\n"
        "1. Перевірте ваш кошик.\n"
        "2. Якщо все вірно, натисніть «Замовити».",
        reply_markup=cart,
        parse_mode=ParseMode.HTML
    )
    await cq.answer()


@dp.callback_query(CallbackData("cart_order"))
async def order_handler(cq: CallbackQuery, user: User):
    _, order_price, total_count = get_products_text(user.cart)

    if not total_count:
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
        await cq.answer("У вас немає товарів в корзині!\nПерехід в меню...")
        return

    await cq.edit_text(
        "<b>💫 Ваше замовлення:</b>\n\n"
        "Дякуємо за ваше замовлення! Ось підсумок:\n"
        f"<blockquote>💐 Кількість букетів - <i>{total_count}</i></blockquote>\n"
        f"<blockquote>💳 Загальна сума - <i>{order_price}</i> грн</blockquote>"
        "\n\n<b>Що далі?</b>\n"
        "1. Перевірте всі дані.\n"
        "2. Підтвердіть замовлення.",
        reply_markup=cart_order,
        parse_mode=ParseMode.HTML
    )
    await cq.answer()


@dp.callback_query(CallbackData("cart_order_confirm"))
async def order_confirm_handler(cq: CallbackQuery, user: User):
    cart_text, order_price, total_count = get_products_text(user.cart)

    current_time = datetime.datetime.now().isoformat()
    user.order.append({
        "description": cart_text,
        "order_price": order_price,
        "total_count": total_count,
        "city": user.city,
        "date": current_time
    })
    user.cart = []
    await user.save()

    await cq.edit_text(
        text="🌺 Ваше замовлення в обробці, дякую за покупку!",
        reply_markup=menu,
        parse_mode=ParseMode.HTML
    )
    await cq.answer()


@dp.callback_query(CallbackData("cart_remove_all"))
async def cart_remove_all_handler(cq: CallbackQuery, user: User):
    user.cart = []
    await user.save()

    await cq.edit_text(
        "<b>🧹 Ви успішно очистили корзину!</b>",
        reply_markup=menu,
        parse_mode=ParseMode.HTML
    )
