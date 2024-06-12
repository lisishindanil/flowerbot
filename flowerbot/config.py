from envparse import env

env.read_envfile(".env")

WEATHER_API_KEY = env.str("WEATHER_API_KEY")
OPENAI_API_KEY = env.str("OPENAI_API_KEY")
