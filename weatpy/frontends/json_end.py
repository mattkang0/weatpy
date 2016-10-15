# -*- coding: utf-8 -*-
import datetime
import json

from weatpy import iface


class ComplexEncoder(json.JSONEncoder):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        elif isinstance(obj, datetime.datetime):
            return obj.strftime("%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT))
        else:
            return json.JSONEncoder.default(self, obj)


class JSONFrontend(iface.Frontend):
    def render(self, data, unit):
        print json.dumps(data, cls=ComplexEncoder, indent=4, ensure_ascii=False)


json_frontend = JSONFrontend()  # singleton
