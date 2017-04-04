#! /usr/bin/env python
import sys
import os
from subprocess import call


def main():
    if len(sys.argv) < 2:
        print 'Usage:\n./run_test.py <test>'
        return
    test = sys.argv[1]
    base_folder = os.path.join(
        'insight_testsuite', 'tests', test)
    if not os.path.isdir(base_folder):
        print 'folder {} for test "{}"" doesn''t exist'.format(base_folder, test)
    dest_folder = os.path.join('temp', 'log_output')
    if not os.path.isdir(dest_folder):
        os.makedirs(dest_folder)
    command = [
        'python', './src/process_log.py',
        os.path.join(base_folder, 'log_input', 'log.txt')]
    dest_files = ['hosts.txt', 'hours.txt',
                  'disjointhours.txt', 'resources.txt',
                  'blocked.txt', 'resources_with_bytes.txt']
    for f in dest_files:
        command.append(os.path.join(dest_folder, f))
    call(command)


if __name__ == '__main__':
    main()
