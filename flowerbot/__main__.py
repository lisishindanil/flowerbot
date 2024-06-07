from pathlib import Path

from mubble import Token, API, Dispatch, Mubble, LoopWrapper
from tortoise import Tortoise

from flowerbot import dps
from flowerbot.database import Catalog

api = API(Token.from_env(path_to_envfile=".env"))
dispatch = Dispatch()
for dp in dps:
    dispatch.load(dp)


async def setup_database():
    models = ["flowerbot.database.user", "flowerbot.database.catalog"]

    await Tortoise.init(
        db_url=f"sqlite://db.sqlite3",
        modules={"models": models},
    )
    await Tortoise.generate_schemas()
    Tortoise.init_models(
        models,
        "models",
    )

    # DEV!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if await Catalog.get_or_none(id=1) is None:
        flowers = [
            {"name": "Rose red", "price": 100, "count": 120, "image_path": "flowerbot/images/rose_red.jpg"},
            {"name": "Rose white", "price": 90, "count": 150, "image_path": "flowerbot/images/rose_white.jpg"},
            {"name": "Rose black", "price": 200, "count": 90, "image_path": "flowerbot/images/rose_black.jpg"},
            {"name": "Rose yellow", "price": 105, "count": 175, "image_path": "flowerbot/images/rose_yellow.jpg"},
        ]

        for flower in flowers:
            await Catalog.create(
                name=flower["name"],
                price=flower["price"],
                count=flower["count"],
                image=Path(flower["image_path"]).read_bytes()
            )

bot = Mubble(api, dispatch=dispatch)

lw = LoopWrapper()
lw.add_task(setup_database())
bot.loop_wrapper = lw
bot.run_forever()
