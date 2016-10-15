# -*- coding: utf-8 -*-
import ConfigParser
import argparse
import logging
import os.path
from logging.config import dictConfig

from weatpy.backends import forecast_backend
from weatpy.frontends import aat_frontend, json_frontend

logger = logging.getLogger('weatpy')

ALL_BACKENDS = {
    "forecast.io": forecast_backend
}
ALL_FRONTENDS = {
    "ascii-art-table": aat_frontend,
    "json": json_frontend
}

CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.weatpyrc')


class FakeGlobalSectionHead(object):
    def __init__(self, fp):
        self.fp = fp
        self.sechead = '[global]\n'

    def readline(self):
        if self.sechead:
            try:
                return self.sechead
            finally:
                self.sechead = None
        else:
            return self.fp.readline()


def init_logging(level):
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': 'logger %(levelname)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': level,
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
        },
        'loggers': {
            'weatpy': {
                'handlers': ['console'],
                'level': level,
                'propagate': False,
            },
        }
    }
    dictConfig(logging_config)


def get_arg_namespace():
    cp = ConfigParser.ConfigParser()
    cp.readfp(FakeGlobalSectionHead(open(CONFIG_FILE)))
    defaults = dict(cp.items('global'))
    parser = argparse.ArgumentParser(description='weatpy for weather forecast')
    parser.set_defaults(**defaults)
    parser.add_argument('-v', action='count')
    parser.add_argument('-b', '--backend', help='BACKEND to be used. (default "forecast.io")')
    parser.add_argument('-f', '--frontend', help='FRONTEND to be used. (default "ascii-art-table")')
    parser.add_argument('-d', '--numdays', type=int, help='NUMBER of days of weather forecast to be displayed (default 3)')
    parser.add_argument('-l', '--location', help='LOCATION to be queried (default "22.5333,114.1333")')
    parser.add_argument('-u', '--unit', help='UNITSYSTEM to use for output. Choices are: metric, imperial, si (default "metric")')
    parser.add_argument('--api-key', help='the api KEY to use')
    parser.add_argument('--lang', help='LANGUAGE to request from forecast.io (default zh)')
    arg_namespace = parser.parse_args()
    if arg_namespace.v:
        if arg_namespace.v == 1:
            init_logging(logging.INFO)
        else:
            init_logging(logging.DEBUG)
    logger.debug('used config: %s', arg_namespace)
    return arg_namespace


def main():
    arg_ns = get_arg_namespace()
    be = ALL_BACKENDS[arg_ns.backend]
    r = be.fetch(arg_ns)
    fe = ALL_FRONTENDS[arg_ns.frontend]
    fe.render(r, unit=arg_ns.unit)


if __name__ == '__main__':
    main()
