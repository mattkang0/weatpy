# -*- coding: utf-8 -*-
import logging
from datetime import datetime

import requests

from weatpy import iface, geo

logger = logging.getLogger('weatpy')


class ForecastBackend(iface.Backend):
    def parse_daily(self, resp, numdays):
        forecast = []
        day = None
        for hour_data in resp['hourly']['data']:
            slot = self.parse_cond(hour_data)
            if day and day.date.date() != slot.time.date():
                if len(forecast) > numdays:
                    break
                forecast.append(day)
                day = None
            if not day:
                day = iface.Day(
                    date=slot.time,
                    slots=[],
                )
            day.slots.append(slot)
        return forecast[1:]

    def parse_cond(self, datapoint):
        codemap = {
            "clear-day":           iface.CODE_SUNNY,
            "clear-night":         iface.CODE_SUNNY,
            "rain":                iface.CODE_LIGHT_RAIN,
            "snow":                iface.CODE_LIGHT_SNOW,
            "sleet":               iface.CODE_LIGHT_SLEET,
            "wind":                iface.CODE_PARTLY_CLOUDY,
            "fog":                 iface.CODE_FOG,
            "cloudy":              iface.CODE_CLOUDY,
            "partly-cloudy-day":   iface.CODE_PARTLY_CLOUDY,
            "partly-cloudy-night": iface.CODE_PARTLY_CLOUDY,
            "thunderstorm":        iface.CODE_THUNDERY_SHOWERS,
        }
        dp = datapoint
        ret = iface.Cond(
            time=datetime.fromtimestamp(dp['time']),
            code=codemap.get(dp.get('icon'), iface.CODE_UNKNOWN),
            desc=dp['summary'],
            temp_c=dp['temperature'],
            feels_like_c=dp['apparentTemperature'],
            chance_of_rain_percent=dp['precipProbability'] * 100 if 0 <= dp.get('precipProbability', -1) <= 1 else None,
            precip_m=dp['precipIntensity'] / 1000.0 if 'precipIntensity' in dp else None,
            visible_dist_m=dp['visibility'] * 1000 if 'visibility' in dp else None,
            windspeed_kmph=dp.get('windSpeed'),
            winddir_degree=dp['windBearing'] % 360 if 'windBearing' in dp else None,
            wind_gust_kmph=None,  # wind_gust_kmph not provided by forecast.io
            humidity=dp['humidity'] * 100 if 'humidity' in dp else None
        )
        return ret

    def fetch(self, arg_ns):
        if not arg_ns.api_key:
            print 'No forecast.io API key specified.'
            print 'You have to register for one at https://developer.forecast.io/register'
            exit()

        if ',' in arg_ns.location:
            try:
                loc = arg_ns.location
                lat, lon = loc.split(',')
                float(lat)
                float(lon)
            except ValueError:
                print 'Invalid location'
                exit()
        else:
            loc = geo.CITY_TO_LOCATION.get(arg_ns.location.strip().decode('utf-8').rstrip(u'市')+u'市')
            if not loc:
                print 'Unrecognize location, currently just support some of the China city name, or you can specify coordinates directly. eg. 22.5333,114.1333'
                exit()
        url = ("https://api.forecast.io/forecast/{api_key}/{location}?"
               "units=ca&lang={lang}&exclude=minutely,alerts,flags&extend=hourly".format(
                                                                    api_key=arg_ns.api_key,
                                                                    location=loc,
                                                                    lang=arg_ns.lang
                                                                    ))
        logger.debug('start request from: %s' % url)
        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            print 'ConnectionError. Please make sure your network is ok'
            exit()
        logger.debug('finish request.')
        logger.debug(r)
        if r.status_code != 200:
            print 'Some problem occur when request forecast.io. Please make sure your api key is valid.'
            print
            exit()
        resp = r.json()
        logger.info("The timezone at this location is %s" % resp['timezone'])
        ret = iface.Data(
            current=self.parse_cond(resp['currently']),
            forecast=self.parse_daily(resp, arg_ns.numdays),
            location=None,
            geoloc=None
        )
        return ret


forecast_backend = ForecastBackend()  # singleton
