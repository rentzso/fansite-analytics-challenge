from random import randint
import hours
from fansiteheap import HeapRecord, FansiteHeap
import lineparser


class TestBinarySearch(hours.SixtyMinuteTracker):

    def __init__(self):
        super(TestBinarySearch, self).__init__()
        counts = [3,  20, 25,  40,  50,   80]
        timestamps = [20, 50, 100, 800, 3600, 9000]
        for count, timestamp in zip(counts, timestamps):
            self.counts[timestamp] = count
            self.timestamps.append(timestamp)

    def test_before_last(self):
        result = self.search_timestamp_before(5400, 5, 6)
        assert result == 5, result

    def test_3600(self):
        result = self.search_timestamp_before(3600, 0, 6)
        assert result == 4, result

    def test_in_between(self):
        result = self.search_timestamp_before(300, 0, 5)
        assert result == 3, result

    def test_equal_to_timestamp(self):
        result = self.search_timestamp_before(100, 0, 5)
        assert result == 2, result


def exec_one_tracker(timestamps, num_events_list, expected_result):
    print 'timestamps = ', timestamps
    print 'num_events_list = ', num_events_list
    hours_tracker = hours.SixtyMinuteTracker()
    for num_events, timestamp in zip(num_events_list, timestamps):
        for i in xrange(num_events):
            hours_tracker.receive(timestamp)
    result = hours_tracker.result()
    assert result == expected_result, (
        '{} != {}'.format(result, expected_result)
    )


def naive_tracker(timestamps, num_events_list):
    reverse_index = {}
    for i, t in enumerate(timestamps):
        reverse_index[t] = i
    t0 = timestamps[0]
    counts = FansiteHeap()
    base_index = 0
    while t0 <= timestamps[-1]:
        count = 0
        j = base_index
        while j < len(timestamps) and timestamps[j] <= (t0 + 3600):
            count += num_events_list[j]
            j += 1
        counts.checkAndUpdate(HeapRecord(count, lineparser.retrieve_date(t0)))
        if reverse_index.get(t0) is not None:
            base_index += 1
        t0 += 1
    counts.sort(reverse=True)
    return counts


def test_tracker():
    num_events_list = [
        3,  17, 5,   15,  40,   200,   40,    10,    230]
    timestamps = [
        20, 50, 100, 800, 6400, 10000, 13595, 20001, 23601]
    expected_result = [
        HeapRecord(statistic=240, key=lineparser.retrieve_date(6400)),
        HeapRecord(statistic=240, key=lineparser.retrieve_date(9995)),
        HeapRecord(statistic=240, key=lineparser.retrieve_date(9996)),
        HeapRecord(statistic=240, key=lineparser.retrieve_date(9997)),
        HeapRecord(statistic=240, key=lineparser.retrieve_date(9998)),
        HeapRecord(statistic=240, key=lineparser.retrieve_date(9999)),
        HeapRecord(statistic=240, key=lineparser.retrieve_date(10000)),
        HeapRecord(statistic=240, key=lineparser.retrieve_date(20001)),
        HeapRecord(statistic=230, key=lineparser.retrieve_date(20002)),
        HeapRecord(statistic=230, key=lineparser.retrieve_date(20003))
    ]
    exec_one_tracker(timestamps, num_events_list, expected_result)
    assert expected_result == naive_tracker(timestamps, num_events_list)


def test_tracker_1():
    num_events_list = [
        3,  17, 5,   15,  40,   200,   40,    4,     10,    230]
    timestamps = [
        20, 50, 100, 800, 6400, 10000, 13595, 13600, 20001, 23601]
    expected_result = [
        HeapRecord(statistic=244, key=lineparser.retrieve_date(10000)),
        HeapRecord(statistic=240, key=lineparser.retrieve_date(6400)),
        HeapRecord(statistic=240, key=lineparser.retrieve_date(9995)),
        HeapRecord(statistic=240, key=lineparser.retrieve_date(9996)),
        HeapRecord(statistic=240, key=lineparser.retrieve_date(9997)),
        HeapRecord(statistic=240, key=lineparser.retrieve_date(9998)),
        HeapRecord(statistic=240, key=lineparser.retrieve_date(9999)),
        HeapRecord(statistic=240, key=lineparser.retrieve_date(20001)),
        HeapRecord(statistic=230, key=lineparser.retrieve_date(20002)),
        HeapRecord(statistic=230, key=lineparser.retrieve_date(20003))
    ]
    exec_one_tracker(timestamps, num_events_list, expected_result)
    assert expected_result == naive_tracker(timestamps, num_events_list)


def generate(size):
    timestamp = 0
    timestamps = []
    num_events_list = []
    for i in range(size):
        timestamp += randint(1, 101)
        num_events = randint(1, 101)
        timestamps.append(timestamp)
        num_events_list.append(num_events)
    return (
        timestamps, num_events_list,
        naive_tracker(timestamps, num_events_list))


def test_randomly_generated():
    for i in range(30):
        size = 10 if i < 3 else 100
        size = size if i < 10 else 1000
        timestamps, num_events_list, expected_result = generate(size)
        yield exec_one_tracker, timestamps, num_events_list, expected_result
