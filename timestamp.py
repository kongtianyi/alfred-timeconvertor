# -*- encoding: utf-8 -*-


import os
import sys
import pytz
import time
from enum import Enum
from workflow import Workflow3
from datetime import datetime

LOCAL_TIME = "local time"
TIMESTAMP = "timestamp"


class QueryType(Enum):
    INVALID = "invalid"
    NOW = "now"
    TIMESTAMP = "timestamp"
    DATETIME = "datetime"


class MyTimezone:
    def __init__(self, offset, is_local=False):
        """
        init
        :param offset: offset from utc timezone, unit: hour
        """
        self.offset = offset
        self.timezone = pytz.FixedOffset(offset * 60)
        if offset == 0:
            self.name = "UTC"
        elif offset > 0:
            self.name = "UTC+" + str(offset)
        else:
            self.name = "UTC" + str(offset)
        self.is_local = is_local

    def get_offset_second(self):
        return self.offset * 3600


def main(wf):
    query = wf.args[0]
    query_type, query_subject, timezone_list = parse_input(query)

    if query_type == QueryType.NOW:
        now_timestamp = int(time.time())
        add_item(wf, TIMESTAMP, now_timestamp)
        time_result = format_timestamp(now_timestamp)
        add_item(wf, LOCAL_TIME, time_result)
        for _timezone in timezone_list:
            time_result = format_timestamp(now_timestamp, _timezone.timezone)
            add_item(wf, _timezone.name, time_result)
    elif query_type == QueryType.TIMESTAMP:
        query_timestamp = parse_timestamp(query_subject)
        time_result = format_timestamp(query_timestamp)
        add_item(wf, LOCAL_TIME, time_result)
        for _timezone in timezone_list:
            time_result = format_timestamp(query_timestamp, _timezone.timezone)
            add_item(wf, _timezone.name, time_result)
    elif query_type == QueryType.DATETIME:
        sharp_index = query_subject.find("#")
        if sharp_index != -1:
            query_datetime = query_subject[0: sharp_index]
            from_timezone = MyTimezone(get_utc_offset_hour(query_subject[sharp_index + 1:]))
        else:
            query_datetime = query_subject
            from_timezone = MyTimezone(get_local_offset_hour_from_utc(), is_local=True)
        time_data = datetime.strptime(query_datetime, "%Y-%m-%d %H:%M:%S")
        timestamp = int(
            convert_datetime_to_timestamp_with_timezone_offset(time_data, from_timezone.get_offset_second()))
        add_item(wf, TIMESTAMP, timestamp)
        for _timezone in timezone_list:
            time_result = format_timestamp(timestamp, _timezone.timezone)
            add_item(wf, _timezone.name, time_result)
    else:
        add_item(wf, "unknown pattern", query)
    wf.send_feedback()


def add_item(wf, prefix, result):
    title = '{}: {}'.format(prefix, result)
    wf.add_item(title=title, arg=result, valid=True)


def parse_input(key):
    input = key.strip()
    params = input.split(' ')
    if params[0] == "now":
        query_type = QueryType.NOW
        query_subject = "now"
        tzs = params[1:]
    elif is_timestamp(params[0]):
        query_type = QueryType.TIMESTAMP
        query_subject = params[0]
        tzs = params[1:]
    elif is_datetime(params):
        query_type = QueryType.DATETIME
        query_subject = " ".join([params[0], params[1]])
        tzs = params[2:]
    else:
        query_type = QueryType.INVALID
        query_subject = ""
        tzs = []

    aimed_timezone_list = list()
    for tz in tzs:
        tz = tz.strip()
        if tz.find('#') != -1:
            continue
        if tz.find('utc') == -1:
            continue
        offset_hour = get_utc_offset_hour(tz)
        aimed_timezone_list.append(MyTimezone(offset_hour))

    return query_type, query_subject, aimed_timezone_list


def get_utc_offset_hour(tz):
    return int(tz[3:]) if len(tz) > 3 else 0


def format_timestamp(timestamp, _timezone=None):
    return datetime.fromtimestamp(timestamp, tz=_timezone).strftime("%Y-%m-%d %H:%M:%S")


def copy_to_clipboard(value):
    command = 'echo ' + str(value).strip() + '| clip'
    os.system(command)


def is_timestamp(value):
    strlen = len(value)
    '''support 10 or 13 length unixtime |支持10位或者13位unixtime'''
    if strlen != 10 and strlen != 13:
        return False
    try:
        int(value)
    except:
        return False
    return True


def is_datetime(params):
    if len(params) < 2:
        return False
    dt = " ".join([params[0], params[1]])
    sharp_index = dt.find('#')
    if sharp_index != -1:
        dt = dt[:sharp_index]
    try:
        datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    except:
        return False
    return True


def parse_timestamp(value):
    data = int(value)
    strlen = len(value)
    if strlen == 13:
        data = data / 1000.0
    return data


def convert_datetime_to_timestamp_with_timezone_offset(_datetime, offset_second):
    return time.mktime(_datetime.timetuple()) + get_local_offset_from_utc() - offset_second


def get_local_offset_from_utc():
    now = time.time()
    return (datetime.fromtimestamp(now) - datetime.utcfromtimestamp(now)).total_seconds()


def get_local_offset_hour_from_utc():
    second = get_local_offset_from_utc()
    return int(second / 3600)


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
