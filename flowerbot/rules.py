from mubble import MessageRule, Message

from aioowm import OWM

from flowerbot.config import WEATHER_API_KEY

weather = OWM(WEATHER_API_KEY)


class IsCity(MessageRule):
    async def check(self, message: Message, _) -> bool:
        result = await weather.get(message.text.unwrap())

        return not result.error
