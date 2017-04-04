# Summary

This solution for the Insight Coding Challenge [Fansite Analytics](https://github.com/InsightDataScience/fansite-analytics-challenge) is composed by the following modules(source code in folder `src`):
- [process_log](src/process_log.py): main method of the package.
- [lineparser](src/lineparser.py): utility functions for parsing lines of logs and timestamp.
- [fansiteheap](src/fansiteheap.py): min-heap implementation.
- [logintracker](src/logintracker.py): class that tracks the failed logins from each host, used for feature 4.
- [hours](src/hours.py): class that collects all the events for each timestamp to compute the 10 most active 60-min windows.
- [disjointhours](src/disjointhours.py): similar to the module `hours`. Includes a class to compute the 10 most active and **disjoint** 60-min windows(optional feature).

The solution depends on the package nose for testing. Tests are locate in the unit_tests and integration_tests folder.
The integration tests are simple verifications that the statistics collected while computing the top 10 lists are correct.
To run the tests:
```
nosetests <unit_tests|integration_tests>
```

## General structure of the main method

The main method in `process_log.py` does the following:
1. read the log.txt file
2. for each line updates a set of statistics
3. reduce each set of statistics to the results that are written to the output files

The only exception is feature 4 (blocked requests) which are computed and written to the corresponding output file on the fly.


## Description of the implementation


### Feature 1

While reading the file we track how many request there have been for each host and we store this in a dictionary.

After collecting this statistic, we loop over all the key, value pairs in the dictionary and update an instance of FansiteHeap (min-heap of length 10). The sorted heap will be the result written to the hosts output file.


### Feature 2

This is very similar to Feature 1, in this case we use a dictionary to keep track of the total number of bytes returned for each resource.

The heap is used as before to collect the 10 resources that consume the most bandwidth.

**Note** also a file with the total bytes count is produced if it is passed as input to process_log.py.

### Feature 3

For this feature we use an instance of the class SixtyMinuteTracker.

While reading the file, for each timestamp found in a line of log we collect the accumulated number of requests received before that timestamps, including the requests received at that timestamp.

So if we received 5 requests at "01/Aug/1995:00:00:01 -0400", 10 at "01/Aug/1995:00:00:05 -0400", 15 at "01/Aug/1995:00:00:30 -0400"
we would have that the statistic would be respectively 5, 5 + 10 = 15, 5 + 10 + 15 = 30.

Internally we store also an artificial first timestamp equal to -1 with a count of 0.

To compute the number of requests in some 60 min window we will use this statistic by finding the last timestamp which is out of the window (base_timestamp) and the last timestamp which is inside the window. The difference between the two counts will be the number of requests in the window. Also we will track the list of timestamp with requests in an instance attribute of the SixtyMinuteTracker class.

To find the top window, we begin with the window starting at the first received timestamp (base_count = 0), we find the last index in the first-hour window (using binary search in the first 3600 timestamps).

We then slide the start second of the window until we reach the last timestamp with requests

Finally the sorted heap is returned.


### Feature 4

This feature was implemented in the LoginTracker class of logintracker module. For each request, we check if it is a failed or successful login and we update the tracked state of the host.

For each request, we check first if it should be blocked, that is we have a state with 3 timestamps and the last timestamp is less than 5 minutes before the current request timestamp. If it is blocked, no modification to the state is done, but we write the line of the request to the blocked file.

For the other requests we do the following:

- If it is a failed request, we update the state appending the timestamp of the request and excluding from the state all the timestamp that are out of the previous 20 seconds window.
- If it is a success request, we clear the state of the host.
- No action is done for all other requests.


### Optional Feature

Implemented **disjoint** 60-minute most active time windows.
It has been tested only with integration tests (checking basic statistics for the top 10 timestamps).

The idea was to consider 2 hours intervals [start, end] with distance of one hour between two adjacent interval:
[00:00:00-01:59:59], [01:00:00-02:59:59], [02:00:00-03:59:59], [03:00:00-04:59:59] and so on.

All the 60 minutes windows within one such interval are overlapping.
So we need to find the top window for each of them.

Then all the window are sorted, we extract the top window, we check the neighbors 2-hours intervals (the top windows of these interval may be overlapping with the window we have chosen), we update the sorted list of windows and we extract the top window again (until we have the top 10 windows).


#### Clarification on the time windows used

All the time windows of 20 seconds, 5 minutes, 60 minutes from `starttime` to `endtime` include `starttime` and `endtime` and `endtime - starttime` is equal to the duration of the time window.

Examples:

00:00:01 - 00:00:21 is a 20 seconds window

00:00:01 - 00:05:01 is a 5 minute window

00:00:01 - 01:00:01 is a 60 minute window
