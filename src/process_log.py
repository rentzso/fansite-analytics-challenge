#! /usr/bin/env python
import sys
import lineparser
from fansiteheap import FansiteHeap, HeapRecord, heap_postprocessing
from hours import SixtyMinuteTracker
from disjointhours import DisjointSixtyMinuteTracker
from logintracker import LoginTracker
import time


def write_result_to_file(lines, output_filename):
    with open(output_filename, 'w') as output_file:
        output_file.write('\n'.join(lines))


def main():
    time_0 = time.time()
    if len(sys.argv) < 7:
        print 'Arguments are missing. Usage:'
        print (
            'process_log.py <input_file> <hosts_output_file> '
            '<hours_output_file> <disjoint_hours_output_file> '
            '<resources_output_file> <blocked_output_file> '
            '<(optional) resources_with_bytes_file>'
        )
    input_filename = sys.argv[1]
    hosts_filename = sys.argv[2]
    hours_filename = sys.argv[3]
    disjoint_hours_filename = sys.argv[4]
    resources_filename = sys.argv[5]
    blocked_filename = sys.argv[6]
    if len(sys.argv) > 7:
        resources_with_bytes_filename = sys.argv[7]
    # "hosts_activity" keeps track of the number of requests for each host
    hosts_activity = {}
    # "resources_bandwidth" keeps track of the total bytes returned
    # to requests for each resource
    resources_bandwidth = {}

    disjoint_hours_tracker = DisjointSixtyMinuteTracker()
    hours_tracker = SixtyMinuteTracker()
    login_tracker = LoginTracker()
    with open(input_filename, 'rU') as input_file,\
            open(blocked_filename, 'w') as blocked_file:
        for line in input_file:
            parsed = lineparser.parse_log_entry(line)
            # update host activity
            hosts_activity[parsed.host] = hosts_activity.get(parsed.host, 0) + 1
            # update resource bandwidth usage
            resources_bandwidth[parsed.resource] = (
                resources_bandwidth.get(parsed.resource, 0) + parsed.bytes
            )
            # collect the timestamp of the event in the two sixty
            # minutes trackers
            hours_tracker.receive(parsed.timestamp)
            disjoint_hours_tracker.receive(parsed.timestamp)
            # pass the full request to the login tracker and write the
            # line to the blocked file if the request is marked.
            if login_tracker.receive(parsed):
                blocked_file.write(line)

    # After collecting the data we compute the result of each feature.
    # For the hours and disjointhours features, the tracker classes define a
    # special instance method "result" to compute the top 10 statistic.
    # For the hosts and resources features we use the heap_postprocessing
    # method to collect the key, value pairs in the respective tracker
    # dictionaries.

    hours_lines = [
        '{},{}'.format(record.key,
                       str(record.statistic))
        for record in hours_tracker.result()]
    write_result_to_file(hours_lines, hours_filename)

    disjoint_hours_lines = [
        '{},{}'.format(lineparser.retrieve_date(record.key),
                       str(record.statistic))
        for record in disjoint_hours_tracker.result()]
    write_result_to_file(disjoint_hours_lines, disjoint_hours_filename)

    hosts_result = heap_postprocessing(hosts_activity)
    hosts_lines = [
        '{},{}'.format(record.key, str(record.statistic))
        for record in hosts_result]
    write_result_to_file(hosts_lines, hosts_filename)

    resources_result = heap_postprocessing(resources_bandwidth)
    resources_lines = [record.key for record in resources_result]
    write_result_to_file(resources_lines, resources_filename)

    if resources_with_bytes_filename:
        resources_with_bytes_lines = [
            '{},{}'.format(record.key, str(record.statistic))
            for record in resources_result]
        write_result_to_file(
            resources_with_bytes_lines, resources_with_bytes_filename)

    print "Total runtime: {} seconds".format(time.time() - time_0)


if __name__ == '__main__':
    main()
