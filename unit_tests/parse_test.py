import nose
import lineparser


def test_parser_with_request():
    line = (
        'in24.inetnebr.com - - [01/Aug/1995:00:00:01 -0400]'
        ' "GET /shuttle/missions/sts-68/news/sts-68-mcc-05.txt HTTP/1.0" '
        '200 1839'
    )
    expected_result = lineparser.ParsedRequest(
        'in24.inetnebr.com', 807235201, 'GET',
        '/shuttle/missions/sts-68/news/sts-68-mcc-05.txt', 200, 1839
        )
    result = lineparser.parse_log_entry(line)
    assert result == expected_result, '{}\n{}'.format(result, expected_result)


def test_parser_bad_request_1():
    line = '208.271.69.50 - - [01/Aug/1995:00:00:04 -0400] "??" 400 0'
    expected_result = lineparser.ParsedRequest(
        '208.271.69.50', 807235204, None, None, 400, 0
        )
    result = lineparser.parse_log_entry(line)
    assert result == expected_result, '{}\n{}'.format(result, expected_result)


def test_parser_bad_request_2():
    line = ('arc.dental.upenn.edu - - [18/Jul/1995:11:53:44 -0400]'
            ' "GET /elv/elvpage.htm/"MISSION" HTTP/1.0" 403 -')
    expected_result = lineparser.ParsedRequest(
        'arc.dental.upenn.edu', 806068424,
        'GET', '/elv/elvpage.htm/"MISSION"', 403, 0)
    result = lineparser.parse_log_entry(line)
    assert result == expected_result, '{}\n{}'.format(result, expected_result)
