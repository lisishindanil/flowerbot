from mubble import Token, API, Dispatch, Mubble, LoopWrapper
from tortoise import Tortoise

from flowerbot import dps

api = API(Token.from_env(path_to_envfile=".env"))
dispatch = Dispatch()
for dp in dps:
    dispatch.load(dp)


async def setup_database():
    models = ["flowerbot.database.user", "flowerbot.database.flower"]

    await Tortoise.init(
        db_url=f"sqlite://db.sqlite3",
        modules={"models": models},
    )
    await Tortoise.generate_schemas()
    Tortoise.init_models(
        models,
        "models",
    )


bot = Mubble(api, dispatch=dispatch)

lw = LoopWrapper()
lw.add_task(setup_database())
bot.loop_wrapper = lw
bot.run_forever()
