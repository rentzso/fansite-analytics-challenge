"""
For testing we use this module to parse lines of logs instead of
src/loginparser.py This is to protect us from bugs of our parsing logic
"""
import re
import datetime
from collections import namedtuple


ParsedRequest = namedtuple(
    'ParsedRequest',
    ['host', 'timestamp', 'request_method', 'resource', 'http_code', 'bytes'])
epoch = datetime.datetime.utcfromtimestamp(0)
dateformat = '%d/%b/%Y:%H:%M:%S -0400'


month = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}


def parse_log_entry(line):
    """parse log lines extracting host, timestamp, request, http_code, bytes

    example:
    in24.inetnebr.com - - [01/Aug/1995:00:00:01 -0400] "GET /shuttle/missions/sts-68/news/sts-68-mcc-05.txt HTTP/1.0" 200 1839
    208.271.69.50 - - [01/Aug/1995:00:00:02 -0400] "POST /login HTTP/1.0" 401 1420
    208.271.69.50 - - [01/Aug/1995:00:00:04 -0400] "POST /login HTTP/1.0" 200 1420
    uplherc.upl.com - - [01/Aug/1995:00:00:07 -0400] "GET / HTTP/1.0" 304 0
    uplherc.upl.com - - [01/Aug/1995:00:00:08 -0400] "GET /images/ksclogo-medium.gif HTTP/1.0" 304 0

    if possible the request_method and the the resource will be extracted
    """

    line_pattern = r"^(?P<host>.*) - - \[(?P<timestamp>.*)\] " \
        "\"(?P<request>.*)\" (?P<http_code>\d\d\d) (?P<bytes>.*)$"
    line_groups = re.match(line_pattern, line)
    request_pattern = r"^(?P<request_method>[A-Z]*) (?P<resource>\S+) ?.*$"
    request_groups = re.match(request_pattern, line_groups.group('request'))
    host = line_groups.group('host')
    timestamp = line_groups.group('timestamp')
    timestamp = parse_date(line_groups.group('timestamp'))
    http_code = int(line_groups.group('http_code'))
    num_bytes = line_groups.group('bytes')
    num_bytes = 0 if num_bytes == '-' else int(num_bytes)
    if request_groups:
        request_method = request_groups.group('request_method')
        resource = request_groups.group('resource')
    else:
        request_method = None
        resource = None
    return ParsedRequest(
        host, timestamp, request_method,
        resource, http_code, num_bytes)


def parse_date(date_str):
    dt = datetime.datetime(
        int(date_str[7:11]),
        month[date_str[3:6]],
        int(date_str[0:2]),
        int(date_str[12:14]),
        int(date_str[15:17]),
        int(date_str[18:20]),
    )
    return int((dt - epoch).total_seconds())


def retrieve_date(seconds):
    timedelta = datetime.timedelta(seconds=seconds)
    dt = epoch + timedelta
    return datetime.datetime.strftime(dt, dateformat)
