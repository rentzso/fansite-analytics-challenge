import os
from lineparser_integration import parse_log_entry


def exec_one(log_file, resources_file):
    log = open(log_file, 'rU')
    res = open(resources_file, 'rU')
    resources = {}
    for line in res:
        resource, total_bytes = line.split(',')
        resources[resource] = int(total_bytes)
    for req in log:
        parsed = parse_log_entry(req)
        if resources.get(parsed.resource):
            resources[parsed.resource] -= parsed.bytes
    for k, v in resources.iteritems():
        assert v == 0, k
    log.close()
    res.close()


def test_full_file():
    exec_one(
        'log_input/log.txt',
        'log_output/resources_with_bytes.txt')


def test_insight_testsuite():
    base_folder = 'insight_testsuite/tests'
    testfolders = os.listdir(base_folder)
    for folder in testfolders:
        log_file = os.path.join(
            base_folder, folder, 'log_input/log.txt')
        resources_file = os.path.join(
            base_folder, folder, 'log_output/resources_with_bytes.txt')
        yield exec_one, log_file, resources_file
