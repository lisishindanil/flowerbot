import datetime

from mubble import Dispatch, CallbackQuery, ParseMode
from mubble.rules import CallbackData

from flowerbot.database.user import User
from flowerbot.keyboards import cart, cart_order, menu

dp = Dispatch()


@dp.callback_query(CallbackData("cart"))
async def cart_handler(cq: CallbackQuery, user: User):
    user = await User.get(uid=cq.from_user.id)

    products_text = ""

    for i, product in enumerate(user.cart, 1):
        products_text += f"{i}.| Назва: {product['name']}, ціна - {product['total_price']}, кількість букетів - {product['count']} \n"

    await cq.edit_text(
        "<b>💫 Кошик:</b>\n\n"
        "Ось ваші обрані товари:\n"
        f"<blockquote>{products_text}</blockquote>"
        "\n\n<b>Що далі?</b>\n"
        "1. Перевірте ваш кошик.\n"
        "2. Якщо все вірно, натисніть 'Замовити'.",
        reply_markup=cart,
        parse_mode=ParseMode.HTML
    )
    await cq.answer()


@dp.callback_query(CallbackData("cart_order"))
async def order_handler(cq: CallbackQuery, user: User):
    user = await User.get(uid=cq.from_user.id)

    order_price = 0
    total_count = 0

    for i, product in enumerate(user.cart, 1):
        order_price += product['total_price']
        total_count += product['count']

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
    user = await User.get(uid=cq.from_user.id)
    
    order_price = 0
    total_count = 0

    cart_text = ""
    
    for i, product in enumerate(user.cart, 1):
        cart_text += f"{i}.| Назва: {product['name']}, ціна - {product['total_price']}, кількість букетів - {product['count']} \n"
        order_price += product['total_price']
        total_count += product['count']

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


@dp.callback_query(CallbackData("cart_remove_all"))
async def cart_remove_all_handler(cq: CallbackQuery, user: User):
    user = await User.get(uid=cq.from_user.id)

    user.cart = []
    await user.save()

    await cq.edit_text(
        "<b>🧹 Ви успішно очистили корзину!</b>",
        reply_markup=menu,
        parse_mode=ParseMode.HTML
    )
