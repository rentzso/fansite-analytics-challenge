import os
from lineparser_integration import parse_log_entry, parse_date, retrieve_date


def exec_one(log_file, output_file):
    log = open(log_file, 'rU')
    out = open(output_file, 'rU')
    timestamps = {}
    for line in out:
        timestamp, events = line.split(',')
        timestamps[parse_date(timestamp)] = int(events)
    for req in log:
        parsed = parse_log_entry(req)
        for k in timestamps.keys():
            if 3600 >= parsed.timestamp - k >= 0:
                timestamps[k] -= 1
    for k, v in timestamps.iteritems():
        assert v == 0, retrieve_date(k)
    log.close()
    out.close()


def test_full_file():
    exec_one('log_input/log.txt', 'log_output/hours.txt')


def test_full_file():
    exec_one('log_input/log.txt', 'log_output/disjointhours.txt')


def test_insight_testsuite():
    base_folder = 'insight_testsuite/tests'
    testfolders = os.listdir(base_folder)
    for folder in testfolders:
        log_file = os.path.join(
            base_folder, folder, 'log_input/log.txt')
        output_file = os.path.join(
            base_folder, folder, 'log_output/hours.txt')
        yield exec_one, log_file, output_file


def test_insight_testsuite_disjoints():
    base_folder = 'insight_testsuite/tests'
    testfolders = os.listdir(base_folder)
    for folder in testfolders:
        log_file = os.path.join(
            base_folder, folder, 'log_input/log.txt')
        output_file = os.path.join(
            base_folder, folder, 'log_output/disjointhours.txt')
        yield exec_one, log_file, output_file
