# -*- coding: utf-8 -*-
import re

from weatpy import iface

CODE_TO_ICON = {
        iface.CODE_UNKNOWN: [
            "    .-.      ",
            "     __)     ",
            "    (        ",
            "     `-᾿     ",
            "      •      ",
        ],
        iface.CODE_CLOUDY: [
            "             ",
            "\033[38;5;250m     .--.    \033[0m",
            "\033[38;5;250m  .-(    ).  \033[0m",
            "\033[38;5;250m (___.__)__) \033[0m",
            "             ",
        ],
        iface.CODE_FOG: [
            "             ",
            "\033[38;5;251m _ - _ - _ - \033[0m",
            "\033[38;5;251m  _ - _ - _  \033[0m",
            "\033[38;5;251m _ - _ - _ - \033[0m",
            "             ",
        ],
        iface.CODE_HEAVY_RAIN: [
            "\033[38;5;240;1m     .-.     \033[0m",
            "\033[38;5;240;1m    (   ).   \033[0m",
            "\033[38;5;240;1m   (___(__)  \033[0m",
            "\033[38;5;21;1m  ‚ʻ‚ʻ‚ʻ‚ʻ   \033[0m",
            "\033[38;5;21;1m  ‚ʻ‚ʻ‚ʻ‚ʻ   \033[0m",
        ],
        iface.CODE_HEAVY_SHOWERS: [
            "\033[38;5;226m _`/\"\"\033[38;5;240;1m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;240;1m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;240;1m(___(__) \033[0m",
            "\033[38;5;21;1m   ‚ʻ‚ʻ‚ʻ‚ʻ  \033[0m",
            "\033[38;5;21;1m   ‚ʻ‚ʻ‚ʻ‚ʻ  \033[0m",
        ],
        iface.CODE_HEAVY_SNOW: [
            "\033[38;5;240;1m     .-.     \033[0m",
            "\033[38;5;240;1m    (   ).   \033[0m",
            "\033[38;5;240;1m   (___(__)  \033[0m",
            "\033[38;5;255;1m   * * * *   \033[0m",
            "\033[38;5;255;1m  * * * *    \033[0m",
        ],
        iface.CODE_HEAVY_SNOW_SHOWERS: [
            "\033[38;5;226m _`/\"\"\033[38;5;240;1m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;240;1m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;240;1m(___(__) \033[0m",
            "\033[38;5;255;1m    * * * *  \033[0m",
            "\033[38;5;255;1m   * * * *   \033[0m",
        ],
        iface.CODE_LIGHT_RAIN: [
            "\033[38;5;250m     .-.     \033[0m",
            "\033[38;5;250m    (   ).   \033[0m",
            "\033[38;5;250m   (___(__)  \033[0m",
            "\033[38;5;111m    ʻ ʻ ʻ ʻ  \033[0m",
            "\033[38;5;111m   ʻ ʻ ʻ ʻ   \033[0m",
        ],
        iface.CODE_LIGHT_SHOWERS: [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;111m     ʻ ʻ ʻ ʻ \033[0m",
            "\033[38;5;111m    ʻ ʻ ʻ ʻ  \033[0m",
        ],
        iface.CODE_LIGHT_SLEET: [
            "\033[38;5;250m     .-.     \033[0m",
            "\033[38;5;250m    (   ).   \033[0m",
            "\033[38;5;250m   (___(__)  \033[0m",
            "\033[38;5;111m    ʻ \033[38;5;255m*\033[38;5;111m ʻ \033[38;5;255m*  \033[0m",
            "\033[38;5;255m   *\033[38;5;111m ʻ \033[38;5;255m*\033[38;5;111m ʻ   \033[0m",
        ],
        iface.CODE_LIGHT_SLEET_SHOWERS: [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;111m     ʻ \033[38;5;255m*\033[38;5;111m ʻ \033[38;5;255m* \033[0m",
            "\033[38;5;255m    *\033[38;5;111m ʻ \033[38;5;255m*\033[38;5;111m ʻ  \033[0m",
        ],
        iface.CODE_LIGHT_SNOW: [
            "\033[38;5;250m     .-.     \033[0m",
            "\033[38;5;250m    (   ).   \033[0m",
            "\033[38;5;250m   (___(__)  \033[0m",
            "\033[38;5;255m    *  *  *  \033[0m",
            "\033[38;5;255m   *  *  *   \033[0m",
        ],
        iface.CODE_LIGHT_SNOW_SHOWERS: [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;255m     *  *  * \033[0m",
            "\033[38;5;255m    *  *  *  \033[0m",
        ],
        iface.CODE_PARTLY_CLOUDY: [
            "\033[38;5;226m   \\  /\033[0m      ",
            "\033[38;5;226m _ /\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m   \\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "             ",
        ],
        iface.CODE_SUNNY: [
            "\033[38;5;226m    \\   /    \033[0m",
            "\033[38;5;226m     .-.     \033[0m",
            "\033[38;5;226m  ‒ (   ) ‒  \033[0m",
            "\033[38;5;226m     `-᾿     \033[0m",
            "\033[38;5;226m    /   \\    \033[0m",
        ],
        iface.CODE_THUNDERY_HEAVY_RAIN: [
            "\033[38;5;240;1m     .-.     \033[0m",
            "\033[38;5;240;1m    (   ).   \033[0m",
            "\033[38;5;240;1m   (___(__)  \033[0m",
            "\033[38;5;21;1m  ‚ʻ\033[38;5;228;5m⚡\033[38;5;21;25mʻ‚\033[38;5;228;5m⚡\033[38;5;21;25m‚ʻ   \033[0m",
            "\033[38;5;21;1m  ‚ʻ‚ʻ\033[38;5;228;5m⚡\033[38;5;21;25mʻ‚ʻ   \033[0m",
        ],
        iface.CODE_THUNDERY_SHOWERS: [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;228;5m    ⚡\033[38;5;111;25mʻ ʻ\033[38;5;228;5m⚡\033[38;5;111;25mʻ ʻ \033[0m",
            "\033[38;5;111m    ʻ ʻ ʻ ʻ  \033[0m",
        ],
        iface.CODE_THUNDERY_SNOW_SHOWERS: [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;255m     *\033[38;5;228;5m⚡\033[38;5;255;25m *\033[38;5;228;5m⚡\033[38;5;255;25m * \033[0m",
            "\033[38;5;255m    *  *  *  \033[0m",
        ],
        iface.CODE_VERY_CLOUDY: [
            "             ",
            "\033[38;5;240;1m     .--.    \033[0m",
            "\033[38;5;240;1m  .-(    ).  \033[0m",
            "\033[38;5;240;1m (___.__)__) \033[0m",
            "             ",
        ],
    }


class AatFrontend(iface.Frontend):
    unitsys = None

    def aatpad(self, s, must_len=15):
        real_s = re.sub(r"\033.*?m", "", s).decode('utf-8')
        real_len = len(real_s)
        extra_len = len(re.findall(u'[\u4e00-\u9fa5]', real_s))  # 中文每个字符占用2个宽度
        need_len = must_len - real_len - extra_len  # 区分字符长度与字节长度, 显示是按字符来的
        s += need_len * ' '
        return s

    def format_temp(self, cond):
        def color(temp):
            col = 196
            colmap = [
                iface.ThresholdColor(-15, 21),
                iface.ThresholdColor(-12, 27),
                iface.ThresholdColor(-9, 33),
                iface.ThresholdColor(-6, 39),
                iface.ThresholdColor(-3, 45),
                iface.ThresholdColor(0, 51),
                iface.ThresholdColor(2, 50),
                iface.ThresholdColor(4, 49),
                iface.ThresholdColor(6, 48),
                iface.ThresholdColor(8, 47),
                iface.ThresholdColor(10, 46),
                iface.ThresholdColor(13, 82),
                iface.ThresholdColor(16, 118),
                iface.ThresholdColor(19, 154),
                iface.ThresholdColor(22, 190),
                iface.ThresholdColor(25, 226),
                iface.ThresholdColor(28, 220),
                iface.ThresholdColor(31, 214),
                iface.ThresholdColor(34, 208),
                iface.ThresholdColor(37, 202),
            ]
            for candidate in colmap:
                if temp < candidate.threshold:
                    col = candidate.color
                    break
            return "\033[38;5;%03dm%d\033[0m" % (col, self.unitsys.temp(temp)[0])
        _, u = self.unitsys.temp(0.0)
        if cond.feels_like_c:
            if cond.feels_like_c < cond.temp_c:
                return self.aatpad("%s - %s %s" % (color(cond.feels_like_c), color(cond.temp_c), u))
            elif cond.feels_like_c > cond.temp_c:
                return self.aatpad("%s - %s %s" % (color(cond.temp_c), color(cond.feels_like_c), u))
        return self.aatpad("%s %s" % (color(cond.temp_c), u))

    def format_wind(self, cond):
        def wind_dir(deg):
            if not deg:
                return '?'
            arrows = ["↓", "↙", "←", "↖", "↑", "↗", "→", "↘"]
            return "\033[1m" + arrows[((deg+22) % 360)/45] + "\033[0m"

        def color(spd_kmph):
            col = 196
            colmap = [
                iface.ThresholdColor(0, 46),
                iface.ThresholdColor(4, 82),
                iface.ThresholdColor(7, 118),
                iface.ThresholdColor(10, 154),
                iface.ThresholdColor(13, 190),
                iface.ThresholdColor(16, 226),
                iface.ThresholdColor(20, 220),
                iface.ThresholdColor(24, 214),
                iface.ThresholdColor(28, 208),
                iface.ThresholdColor(32, 202),
            ]
            for candidate in colmap:
                if spd_kmph < candidate.threshold:
                    col = candidate.color
                    break
            return "\033[38;5;%03dm%d\033[0m" % (col, self.unitsys.speed(spd_kmph)[0])
        _, u = self.unitsys.speed(0.0)
        if not cond.windspeed_kmph:
            return self.aatpad(wind_dir(cond.windspeed_kmph))
        if cond.wind_gust_kmph:
            if cond.wind_gust_kmph > cond.windspeed_kmph:
                return self.aatpad("%s %s – %s %s" % (wind_dir(cond.winddir_degree), color(cond.windspeed_kmph), color(cond.wind_gust_kmph), u))
        return self.aatpad("%s %s %s" % (wind_dir(cond.winddir_degree), color(cond.windspeed_kmph), u))

    def format_visibility(self, cond):
        if not cond.visible_dist_m:
            return self.aatpad("")
        v, u = self.unitsys.distance(cond.visible_dist_m)
        return self.aatpad("%d %s" % (v, u))

    def format_rain(self, cond):
        if cond.precip_m is not None:
            v, u = self.unitsys.distance(cond.precip_m)
            if cond.chance_of_rain_percent is not None:
                return self.aatpad("%.1f %s | %d%%" % (v, u, cond.chance_of_rain_percent))
            return self.aatpad("%.1f %s" % (v, u))
        elif cond.chance_of_rain_percent:
            return self.aatpad("%d%%" % cond.chance_of_rain_percent)
        return self.aatpad("")

    def format_cond(self, cur, cond, is_current=False):
        icon = CODE_TO_ICON[cond.code]
        border = ' ' if is_current else '|'
        cur[0] = '%s%-s%-s%s' % (cur[0], icon[0], self.aatpad(cond.desc.encode('utf8')), border)
        cur[1] = '%s%-s%s%s' % (cur[1], icon[1], self.format_temp(cond), border)
        cur[2] = '%s%-s%s%s' % (cur[2], icon[2], self.format_wind(cond), border)
        cur[3] = '%s%-s%s%s' % (cur[3], icon[3], self.format_visibility(cond), border)
        cur[4] = '%s%-s%s%s' % (cur[4], icon[4], self.format_rain(cond), border)

    def print_day(self, day):
        desired_times_of_day = [8, 12, 19, 23]
        cols = [cand for cand in day.slots if cand.time.hour in desired_times_of_day]

        ret = ['|', '|', '|', '|', '|']
        date_fmt = "┤ %11s ├" % day.date.strftime('%a %d. %b')
        s = (
            "                                                   ┌─────────────┐ ",
            "┌────────────────────────────┬─────────────────────" + date_fmt + "─────────────────────┬────────────────────────────┐",
            "│           Morning          │            Noon     └──────┬──────┘    Evening          │            Night           │",
            "├────────────────────────────┼────────────────────────────┼────────────────────────────┼────────────────────────────┤",
        )
        for line in s:
            print line
        for cond in cols:
            self.format_cond(ret, cond)
        for line in ret:
            print line
        print "└────────────────────────────┴────────────────────────────┴────────────────────────────┴────────────────────────────┘"

    def render(self, data, unit):
        self.unitsys = iface.UnitSystem(unit)
        ret = ['', '', '', '', '']
        self.format_cond(ret, data.current, is_current=True)
        for line in ret:
            print line
        for day in data.forecast:
            self.print_day(day)


aat_frontend = AatFrontend()  # singleton
