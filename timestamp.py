# -*- encoding: utf-8 -*-


import os
import sys
from workflow import Workflow3
from datetime import datetime, timedelta, timezone


def main(wf:Workflow3):
    result = []
    query = wf.args[0]
    query_time, _timezone = parse_input(query)

    if query_time == 'now':
        now_timestamp = int(datetime.now().timestamp())
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
        time_data = time_data.replace(tzinfo=_timezone)
        time_result = int(time_data.timestamp())
        append_timestamp_result(wf, time_result)
    return result


def append_datetime_result(wf: Workflow3, time_result: str):
    title = 'datetime: %s' % (time_result,)
    wf.add_item(title=title)


def append_timestamp_result(wf: Workflow3, timestamp: int):
    title = '{}: {}'.format('timestamp', timestamp)
    wf.add_item(title=title)


def parse_input(key: str) -> (str, timezone):
    input = key.strip()
    params = input.split(' ', 1)
    is_set_timezone = len(params) == 2 and params[0].startswith('utc')
    if is_set_timezone:
        aimed_timezone_str = params[0]
        aimed_timezone_offset = 0
        if len(aimed_timezone_str) > 3:
            aimed_timezone_offset = int(aimed_timezone_str[3:])
        used_timezone = timezone(timedelta(hours=aimed_timezone_offset))
        query_time = params[1]
    else:
        used_timezone = None
        query_time = input
    return query_time, used_timezone


def format_timestamp(timestamp: int, _timezone: timezone) -> str:
    return datetime.fromtimestamp(timestamp, tz=_timezone).strftime("%Y-%m-%d %H:%M:%S")


def copy_to_clipboard(value):
    command = 'echo ' + str(value).strip() + '| clip'
    os.system(command)


def is_timestamp(value: str) -> bool:
    strlen = len(value)
    '''support 10 or 13 length unixtime |支持10位或者13位unixtime'''
    if strlen != 10 and strlen != 13:
        return False
    try:
        int(value)
    except:
        return False
    return True


def parse_timestamp(value: str) -> int:
    data = int(value)
    strlen = len(value)
    if strlen == 13:
        data = data / 1000.0
    return data


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
