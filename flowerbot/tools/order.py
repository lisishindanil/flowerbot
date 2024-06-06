from aioowm import OWM
from flowerbot.config import WEATHER_API_KEY

weather = OWM(WEATHER_API_KEY)

WEATHER_PRICE = {
    2: 60,
    3: 50,
    5: 40,
    6: 100,
    7: 80,
    8: 0,
}


async def calculate(price: int | float, city: str) -> bool | dict[str, int | float]:
    total_price = price
    result = await weather.get(city)

    if result.error:
        return False

    city_price = WEATHER_PRICE[int(str(result.weather.id)[0])]

    total_price += city_price

    return {'price': price, 'total_price': total_price, 'city_price': city_price}
