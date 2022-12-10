# -*- encoding: utf-8 -*-


import os
import sys
import pytz
import time
from workflow import Workflow3
from datetime import datetime


def main(wf):
    query = wf.args[0]
    query_time, _timezone, timezone_offset = parse_input(query)

    if query_time == 'now':
        now_timestamp = int(time.time())
        append_timestamp_result(wf, now_timestamp)
        time_result = format_timestamp(now_timestamp, _timezone)
        append_datetime_result(wf, time_result)
    elif is_timestamp(query_time):
        query_timestamp = parse_timestamp(query_time)
        time_result = format_timestamp(query_timestamp, _timezone)
        append_datetime_result(wf, time_result)
    else:
        if ":" in query_time:
            time_data = datetime.strptime(query_time, "%Y-%m-%d %H:%M:%S")
        else:
            time_data = datetime.strptime(query_time, "%Y-%m-%d")
        time_result = int(convert_datetime_to_timestamp_with_timezone_offset(time_data, timezone_offset))
        append_timestamp_result(wf, time_result)
    wf.send_feedback()


def append_datetime_result(wf, time_result):
    title = 'datetime: %s' % (time_result,)
    wf.add_item(title=title, arg=time_result, valid=True)


def append_timestamp_result(wf, timestamp):
    title = '{}: {}'.format('timestamp', timestamp)
    wf.add_item(title=title, arg=timestamp, valid=True)


def parse_input(key):
    input = key.strip()
    params = input.split(' ', 1)
    is_set_timezone = len(params) == 2 and params[0].startswith('utc')
    if is_set_timezone:
        aimed_timezone_str = params[0]
        aimed_timezone_offset = 0
        if len(aimed_timezone_str) > 3:
            aimed_timezone_offset = int(aimed_timezone_str[3:])
        used_timezone = pytz.FixedOffset(aimed_timezone_offset * 60)
        timezone_offset = aimed_timezone_offset * 60 * 60
        query_time = params[1]
    else:
        used_timezone = None
        query_time = input
        timezone_offset = get_local_offset_from_utc()
    return query_time, used_timezone, timezone_offset


def format_timestamp(timestamp, _timezone):
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


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
