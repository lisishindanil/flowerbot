from mubble import Dispatch, CallbackQuery, MessageCute, ParseMode
from mubble.rules import CallbackData

from flowerbot.database import Catalog, User
from flowerbot.keyboards import menu, catalog_nav
from flowerbot.tools.order import calculate

dp = Dispatch()

user_pages = {}


@dp.callback_query(CallbackData("catalog"))
async def catalog_handler(cq: CallbackQuery):
    await cq.delete()

    user_pages[cq.from_user.id] = 1

    catalog = await Catalog.get(id=user_pages[cq.from_user.id])
    flowers_count = len(await Catalog.all())
    text = (
        f"🌷 <b>Сторінка 1/{flowers_count}</b>\n\n"
        f"Назва: <b>{catalog.name}</b>\n"
        f"Ціна: <b>{catalog.price}₴</b>\n"
        f"В наявності: <b>{catalog.count}</b>"
    )

    await cq.ctx_api.send_photo(
        chat_id=cq.chat_id,
        photo=("image.jpg", catalog.image),
        caption=text,
        reply_markup=catalog_nav,
        parse_mode=ParseMode.HTML
    )


@dp.callback_query(CallbackData("catalog_nav_prev") | CallbackData("catalog_nav_next"))
async def catalog_nav_prev_handler(cq: CallbackQuery, user: User):
    catalog = await Catalog.get(id=user_pages[cq.from_user.id])
    flowers_count = len(await Catalog.all())

    if (
            user_pages[cq.from_user.id] == 1
            or flowers_count - user_pages[cq.from_user.id] == 0
    ):
        await cq.answer("Ви не можете перейти назад")
        return
    if cq.data == "catalog_nav_prev":
        user_pages[cq.from_user.id] -= 1
    else:
        user_pages[cq.from_user.id] += 1

    text = (
        f"🌷 <b>Сторінка {user_pages[cq.from_user.id]}/{flowers_count}</b>\n\n"
        f"Назва: <b>{catalog.name}</b>\n"
        f"Ціна: <b>{catalog.price}₴</b>\n"
        f"В наявності: <b>{catalog.count}</b>"
    )
    await cq.delete()

    await cq.ctx_api.send_photo(
        chat_id=cq.chat_id,
        photo=("image.jpg", catalog.image),
        caption=text,
        reply_markup=catalog_nav,
        parse_mode=ParseMode.HTML
    )


@dp.callback_query(CallbackData("catalog_nav_choose"))
async def catalog_nav_choose_handler(cq: CallbackQuery, user: User):
    cart = await Catalog.get(id=user_pages[cq.from_user.id])
    count = 1

    prices = await calculate(cart.price, user.city)
    user.cart.append({"name": cart.name, "count": count, "city": user.city, **prices})
    await user.save()
    await cq.answer("Товар додано до корзини!")

    await cq.delete()
    await cq.ctx_api.send_message(
        chat_id=cq.chat_id,
        text="🌺 Ви в меню!",
        reply_markup=menu,
        parse_mode=ParseMode.HTML
    )
