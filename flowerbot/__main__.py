from mubble import Token, API, Dispatch, Mubble

from flowerbot import dps


api = API(Token.from_env(path_to_envfile=".env"))
dispatch = Dispatch()
for dp in dps:
    dispatch.load(dp)


bot = Mubble(api, dispatch=dispatch)

bot.run_forever()
