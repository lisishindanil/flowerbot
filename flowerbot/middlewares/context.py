from mubble import Dispatch, ABCMiddleware, Message, CallbackQuery
from mubble.bot.dispatch.context import Context

from flowerbot.database import User

dp = Dispatch()


@dp.message.register_middleware()
class ContextMiddleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: Context) -> bool:
        user = await User.get_or_none(uid=event.from_user.id)

        if user is None:
            user = await User.create(uid=event.from_user.id)
        ctx.set("user", user)

        return True


@dp.callback_query.register_middleware()
class ContextMiddleware(ABCMiddleware[CallbackQuery]):
    async def pre(self, event: Message, ctx: Context) -> bool:
        user = await User.get_or_none(uid=event.from_user.id)

        if user is None:
            user = await User.create(uid=event.from_user.id)
        ctx.set("user", user)

        return True
