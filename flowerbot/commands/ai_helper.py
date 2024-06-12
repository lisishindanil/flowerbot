from langchain.chains.llm import LLMChain
from mubble import Dispatch, CallbackQuery, ParseMode, WaiterMachine
from mubble.rules import CallbackData

from flowerbot.database.user import User
from flowerbot.keyboards import ai_helper
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
    response = llm_chain.invoke("Хто ти?")
    await cq.edit_text(
        response.get('text'),
        reply_markup=ai_helper,
        parse_mode=ParseMode.HTML
    )
    await cq.answer()
