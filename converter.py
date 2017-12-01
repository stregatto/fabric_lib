import re


class TimeConverter(object):

    def __init__(self, data):
        self.seconds = self.convert_to_second(data)
        self.string = self.convert_to_string(data)

    def convert_to_second(self, stringtime):
        if isinstance(stringtime, str):
            try:
                re.purge
                data = re.match("(\d+)(\w*)", stringtime)
                num = data.group(2)
                unit = int(data.group(1))
                units = {"s": 1,
                         "m": 60,
                         "h": 3600,
                         "d": 86400,
                         "w": 604800
                         }
                seconds = units[num] * unit
                return seconds
            except:
                print("Some error occurred tranforming %s in seconds" % (stringtime))

    def week(self, seconds):
        return str(seconds / 604800) + 'w'

    def day(self, seconds):
        return str(seconds / 86400) + 'd'

    def hour(self, seconds):
        return str(seconds / 3600) + 'h'

    def minute(self, seconds):
        return str(seconds / 60) + 'm'

    def second(self, seconds):
        return str(seconds / 60) + 's'

    def convert_to_string(self, seconds):
        if isinstance(seconds, int):
            if self.week(seconds) != '0w':
                return self.week(seconds)
            if self.day(seconds) != '0d':
                return self.day(seconds)
            if self.hour(seconds) != '0h':
                return self.hour(seconds)
            if self.minute(seconds) != '0m':
                return self.minute(seconds)
            if self.second(seconds) != '0s':
                return self.second(seconds)
            else:
                print("Some error occurred tranforming %s in string" % (seconds))
                return '666'

# time = TimeConverter('14m').seconds
# print(time)

# time = TimeConverter('0').seconds
# print(time)

# time = TimeConverter(567).string
# print(time)
