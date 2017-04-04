import os
from lineparser_integration import parse_log_entry


def exec_one(log_file, hosts_file):
    log = open(log_file, 'rU')
    res = open(hosts_file, 'rU')
    hosts = {}
    for line in res:
        host, count = line.split(',')
        hosts[host] = int(count)
    for req in log:
        parsed = parse_log_entry(req)
        if hosts.get(parsed.host):
            hosts[parsed.host] -= 1
    for k, v in hosts.iteritems():
        assert v == 0, k
    log.close()
    res.close()


def test_full_file():
    exec_one('log_input/log.txt', 'log_output/hosts.txt')


def test_insight_testsuite():
    base_folder = 'insight_testsuite/tests'
    testfolders = os.listdir(base_folder)
    for folder in testfolders:
        log_file = os.path.join(
            base_folder, folder, 'log_input/log.txt')
        hosts_file = os.path.join(
            base_folder, folder, 'log_output/hosts.txt')
        yield exec_one, log_file, hosts_file
