# -*- coding: utf-8 -*-
import collections

(
    CODE_UNKNOWN,
    CODE_CLOUDY,
    CODE_FOG,
    CODE_HEAVY_RAIN,
    CODE_HEAVY_SHOWERS,
    CODE_HEAVY_SNOW,
    CODE_HEAVY_SNOW_SHOWERS,
    CODE_LIGHT_RAIN,
    CODE_LIGHT_SHOWERS,
    CODE_LIGHT_SLEET,
    CODE_LIGHT_SLEET_SHOWERS,
    CODE_LIGHT_SNOW,
    CODE_LIGHT_SNOW_SHOWERS,
    CODE_PARTLY_CLOUDY,
    CODE_SUNNY,
    CODE_THUNDERY_HEAVY_RAIN,
    CODE_THUNDERY_SHOWERS,
    CODE_THUNDERY_SNOW_SHOWERS,
    CODE_VERY_CLOUDY
 ) = range(19)

(
    UNITS_METRIC,
    UNITS_IMPERIAL,
    UNITS_SI
) = ('metric', 'imperial', 'si')

ThresholdColor = collections.namedtuple('ThresholdColor', 'threshold color')


class DataObject(object):
    __slots__ = ()
    default_value = None

    def __init__(self, *args, **kwargs):
        for att in self.__slots__:
            setattr(self, att, self.default_value)
        for k, v in zip(self.__slots__, args):
            setattr(self, k, v)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_json(self):
        return {attr: getattr(self, attr) for attr in self.__slots__}


class Cond(DataObject):
    __slots__ = (
                  'time',
                  'code',
                  'desc',
                  'temp_c',
                  'feels_like_c',
                  'chance_of_rain_percent',
                  'precip_m',
                  'visible_dist_m',
                  'windspeed_kmph',
                  'wind_gust_kmph',
                  'winddir_degree',
                  'humidity'
                )


class Astro(DataObject):
    __slots__ = ('moonrise', 'moonset', 'sunrise', 'sunset')


class Day(DataObject):
    __slots__ = ("date", "slots")


class LatLon(DataObject):
    __slots__ = ("latitude", "longitude")


class Data(DataObject):
    __slots__ = ("current", "forecast", "location", "geoloc")


class UnitSystem(object):
    def __init__(self, unit):
        if unit not in (UNITS_METRIC, UNITS_IMPERIAL, UNITS_SI):
            raise Exception('unsupport unit system %s' % unit)
        self.unit = unit

    def temp(self, temp_c):
        if self.unit == UNITS_METRIC:
            return temp_c, "°C"
        elif self.unit == UNITS_IMPERIAL:
            return temp_c*1.8 + 32, "°F"
        elif self.unit == UNITS_SI:
            return temp_c + 273.16, "°K"

    def speed(self, spd_kmph):
        if self.unit == UNITS_METRIC:
            return spd_kmph, "km/h"
        elif self.unit == UNITS_IMPERIAL:
            return spd_kmph / 1.609, "mph"
        elif self.unit == UNITS_SI:
            return spd_kmph / 3.6, "m/s"

    def distance(self, dist_m):
        if self.unit == UNITS_METRIC or self.unit == UNITS_SI:
            if dist_m < 1:
                return dist_m * 1000, "mm"
            if dist_m < 1000:
                return dist_m, "m"
            return dist_m/1000, "km"
        elif self.unit == UNITS_IMPERIAL:
            res, unit = dist_m/0.0254, "in"
            if res < 3*12:
                return res, unit
            elif res < 8*10*22*36:
                return res / 36, "yd"
            return res / 8 / 10 / 22 / 36, "mi"


class Backend(object):
    def fetch(self, arg_ns):
        raise NotImplementedError


class Frontend(object):
    def render(self, data, unit):
        raise NotImplementedError
