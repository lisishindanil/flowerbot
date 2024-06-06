from mubble import InlineKeyboard, InlineButton

menu = (
    InlineKeyboard()
    .add(InlineButton("🌷 Каталог квітів", callback_data="catalog"))
    .add(InlineButton("🛒 Кошик", callback_data="cart"))
    .row()
    .add(InlineButton("⚙️ Налаштування", callback_data="settings"))
).get_markup()

back_to_menu = (
    InlineKeyboard().add(InlineButton("↩️ Назад", callback_data="menu"))
).get_markup()

settings = (
    InlineKeyboard()
    .add(InlineButton("🏡 Редагувати дані доставки", callback_data="settings_city"))
    .row()
    .add(InlineButton("↩️ Назад", callback_data="menu"))
).get_markup()

cart = (
    InlineKeyboard()
    .add(InlineButton("🧹 Очистити кошик", callback_data="cart_remove_all"))
    .add(InlineButton("💳 Замовити", callback_data="cart_order"))
    .row()
    .add(InlineButton("↩️ Назад", callback_data="menu"))
).get_markup()

