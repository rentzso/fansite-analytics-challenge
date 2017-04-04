import re
import datetime
from collections import namedtuple


ParsedRequest = namedtuple(
    'ParsedRequest',
    ['host', 'timestamp', 'request_method', 'resource', 'http_code', 'bytes']
)
epoch = datetime.datetime.utcfromtimestamp(0)

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
    """
    Parse log lines extracting host, timestamp, request, http_code, bytes

    example:
    in24.inetnebr.com - - [01/Aug/1995:00:00:01 -0400] "GET /shuttle/missions/sts-68/news/sts-68-mcc-05.txt HTTP/1.0" 200 1839
    208.271.69.50 - - [01/Aug/1995:00:00:02 -0400] "POST /login HTTP/1.0" 401 1420
    208.271.69.50 - - [01/Aug/1995:00:00:04 -0400] "POST /login HTTP/1.0" 200 1420
    uplherc.upl.com - - [01/Aug/1995:00:00:07 -0400] "GET / HTTP/1.0" 304 0
    uplherc.upl.com - - [01/Aug/1995:00:00:08 -0400] "GET /images/ksclogo-medium.gif HTTP/1.0" 304 0

    if possible the request_method and the the resource will be extracted.

    We don't use regex to optimize for speed.
    """
    request_extractor = line.split('"')

    head = request_extractor[0]
    tail = request_extractor[-1]
    request = '"'.join(request_extractor[1:-1])

    head, timestamp = head.split('[')
    timestamp = parse_date(timestamp[:-2])
    host = head.split()[0]

    http_code, num_bytes = tail.split()
    num_bytes = 0 if num_bytes == '-' else int(num_bytes)

    request_fields = request.split()
    if len(request_fields) > 1:
        request_method = request_fields[0]
        resource = request_fields[1]
    else:
        request_method = None
        resource = None
    return ParsedRequest(
        host, timestamp, request_method,
        resource, int(http_code), num_bytes)


def parse_date(date_str):
    """
    Parses date (faster than datetime.datetime.strptime)
    and convert it to seconds since the epoch.

    Equivalent to dateformat '%d/%b/%Y:%H:%M:%S -0400'

    Timezone are ignored as they are the same (-0400) for each record
    """
    dt = datetime.datetime(
        int(date_str[7:11]),
        month[date_str[3:6]],
        int(date_str[0:2]),
        int(date_str[12:14]),
        int(date_str[15:17]),
        int(date_str[18:20]),
    )
    return int((dt - epoch).total_seconds())


dateformat = '%d/%b/%Y:%H:%M:%S -0400'


def retrieve_date(seconds):
    """
    From a timestamps with seconds since the epoch
    retrieve the original date.
    """
    timedelta = datetime.timedelta(seconds=seconds)
    dt = epoch + timedelta
    return datetime.datetime.strftime(dt, dateformat)
