from dataclasses import dataclass, field
import datetime
from typing import List

from ICBOT.var_env import WEATHER_API_KEY
from ..constants import Messages, Constants
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


class _WeatherCacher:
    def __init__(self) -> None:
        self._timestamp = datetime.datetime.min

    def cache(self, weathers: List[WeatherEntry]):
        self._cached = weathers
        self._timestamp = datetime.datetime.now()
        return weathers

    def value(self):
        return self._cached

    def needs_refresh(self):
        return (datetime.datetime.now() - self._timestamp) > datetime.timedelta(
            hours=Constants.REFRESH_HOURS_WEATHER
        )


_weather_cacher = _WeatherCacher()


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


def weather_forecasts():
    if not _weather_cacher.needs_refresh():
        logger.info("Using cached data for weather.")
        return _weather_cacher.value()
    url = "http://api.openweathermap.org/data/2.5/forecast"
    payload = {
        "appid": WEATHER_API_KEY,
        "lat": 46.517247,  # EPFL coordinates
        "lon": 6.56885,
        "lang": "fr",
        "units": "metric",
    }
    r = requests.get(url, params=payload)
    response = r.json()
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
    return _weather_cacher.cache(weathers)
