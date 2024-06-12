from langchain.chains.llm import LLMChain

from mubble import Dispatch, CallbackQuery, ParseMode, WaiterMachine, MessageReplyHandler
from mubble.rules import CallbackData, HasText

from flowerbot.database import User, Catalog
from flowerbot.keyboards import menu, back_to_menu
from flowerbot.config import OPENAI_API_KEY
from flowerbot.prompts.prompts import flowerbot_assitant_prompt

from langchain_openai import OpenAI

dp = Dispatch()
wm = WaiterMachine()

llm = OpenAI(
    model='gpt-3.5-turbo-instruct',
    temperature=0.7,
    openai_api_key=OPENAI_API_KEY
)

llm_chain = LLMChain(prompt=flowerbot_assitant_prompt, llm=llm)


@dp.callback_query(CallbackData("ai_helper"))
async def ai_helper_handler(cq: CallbackQuery, user: User):
    print(wm.storage)
    text = (
        "🌷 Я бот, який спеціалізується на квітах з каталогу та допомагає користувачам вибирати букети."
        "Ваше завдання — надавати інформацію про квіти з каталогу, рекомендувати букети для різних випадків, "
        "а також допомагати з вибором на основі уподобань користувачів.\n\n"
        "Напишіть ваше повідомлення..."
    )

    await cq.edit_text(
        text,
        reply_markup=back_to_menu,
        parse_mode=ParseMode.HTML
    )

    msg, _ = await wm.wait(
        dp.message,
        (cq.ctx_api, cq.chat_id.unwrap()),
        HasText(),
        default=MessageReplyHandler("Напишіть саме текст!")

    )

    catalog_text = "\n".join([f"Назва: {p.name} Ціна: {p.price} Наявність: {p.count}" for p in await Catalog.all()])
    response = llm_chain.invoke(input={"question": msg.text.unwrap(), "catalog": catalog_text})

    await cq.ctx_api.delete_message(chat_id=cq.chat_id, message_id=msg.message_id)
    await cq.edit_text(
        response.get('text'),
        reply_markup=menu,
        parse_mode=ParseMode.HTML
    )
    await cq.answer()