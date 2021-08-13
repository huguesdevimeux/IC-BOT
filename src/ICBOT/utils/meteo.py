from dataclasses import dataclass, field
import datetime

from ICBOT.var_env import WEATHER_API_KEY
from ..constants import Messages, ErrorMessages
import locale
from ..utils.logging import logger
import requests

locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")


@dataclass(frozen=True)
class WeatherEntry:
    time: str
    feels_like: int
    description: str
    probability_precipitation: int
    clouds: int
    icon: str
    time_of_day: str = field(init=False)
    emoji_: str = field(init=False)

    def __post_init__(self):
        time = datetime.datetime.fromtimestamp(self.time)
        if time.day == datetime.datetime.today().day:
            time_of_day = f"Aujourd'hui à {time.hour}h"
        elif time.day == (datetime.datetime.today() + datetime.timedelta(days=1)).day:
            time_of_day = f"Demain à {time.hour}h"
        else:
            time_of_day = datetime.datetime.strftime(time, "%a %d à %Hh")
        # workaround for frozen .. python ....
        object.__setattr__(self, "time_of_day", time_of_day)

        object.__setattr__(self, "emoji_weather", icons_to_emoji[self.icon])

    def __str__(self) -> str:
        return Messages.METEO.format_map(vars(self))


class KeyValueCache:
    """
    A simple cache that stores values for given keys in memory.
    """

    def __init__(self) -> None:
        self._values = {}  # key → value
        self._expirations = {}  # key → DateTime of the expiration

    def cache(self, key, value, seconds: int):
        """
        Stores a new value in the cache.

        :param key: the key
        :param value: the value
        :param seconds: how many seconds the value lasts before it needs to be replaced
        :returns: the value
        """

        self._values[key] = value
        self._expirations[key] = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        return value

    def get(self, key):
        """
        Returns the latest stored value for a key, or None if no value was stored.

        :param key: the key
        """

        return self._values[key] if key in self._values else None

    def needs_refresh(self, key):
        """
        Returns whether a new value should be computed for the given key.

        :param key: the key
        :returns: True if there is no suitable value for the given key; False otherwise
        """

        return not (key in self._expirations) or self._expirations[key] <= datetime.datetime.now()


icons_to_emoji = {
    "01d": "☀️",
    "02d": "⛅️",
    "03d": "☁️",
    "04d": "☁️",
    "09d": "\uD83C\uDF27",
    "10d": "\uD83C\uDF26",
    "11d": "⛈",
    "13d": "❄️",
    "50d": "\uD83C\uDF2B",
    "01n": "\uD83C\uDF11",
    "02n": "\uD83C\uDF11 ☁",
    "03n": "☁️",
    "04n": "️️☁☁",
    "09n": "\uD83C\uDF27",
    "10n": "\uD83C\uDF26",
    "11n": "⛈",
    "13n": "❄️",
    "50n": "\uD83C\uDF2B",
}


def weather_forecast(city_name: str):
    """
    Get the weather forecast for a city

    :param city_name: the city name
    :return: the weather forecast message (as a String)
    """

    url = 'https://api.openweathermap.org/data/2.5/forecast'
    payload = {
        "appid": WEATHER_API_KEY,
        "q": city_name,
        "lang": "fr",
        "units": "metric",
    }

    r = requests.get(url, params=payload)
    response = r.json()

    if response['cod'] == '404':
        return ErrorMessages.CITY_NOT_FOUND

    if response['cod'] != '200':
        logger.error(f'Weather update error #{response["cod"]}: “{response["message"]}”')
        return ErrorMessages.WEATHER_ERROR

    weathers = []
    for el in response["list"]:
        weathers.append(
            WeatherEntry(
                time=el["dt"],
                feels_like=el["main"]["feels_like"],
                description=el["weather"][0]["description"],
                probability_precipitation=int(float(el["pop"]) * 100),
                clouds=el["clouds"]["all"],
                icon=el["weather"][0]["icon"],
            )
        )

    return "\n".join(str(v) for v in weathers[:12])
