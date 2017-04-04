from fansiteheap import FansiteHeap, HeapRecord
from hours import SixtyMinuteTracker
import pdb

class SimpleSixtyMinuteTracker(SixtyMinuteTracker):

    def result(self, start_timestamp=None, base_index=0, end_index=None):
        if end_index is None:
            end_index = len(self.timestamps)
        if start_timestamp is None:
            start_timestamp = self.timestamps[1]
        last_index = self.search_timestamp_before(
            start_timestamp + 3600,
            0, min(3601, end_index))
        if (len(self.timestamps) > last_index + 1 and
                self.timestamps[last_index + 1] == start_timestamp + 3600):
            last_index = last_index + 1
        base_count = self.counts[self.timestamps[base_index]]
        last_count = self.counts[self.timestamps[last_index]]
        top_window = HeapRecord(last_count - base_count, start_timestamp)
        i = last_index + 1
        while i < end_index:
            start_timestamp = self.timestamps[i] - 3600
            base_index = self.search_timestamp_before(
                start_timestamp, base_index, i)
            base_count = self.counts[self.timestamps[base_index]]
            last_count = self.counts[self.timestamps[i]]
            if (last_count - base_count > top_window.statistic):
                top_window = HeapRecord(
                    last_count - base_count,
                    start_timestamp)
            i += 1
        return top_window

    def slice_result(self, min_timestamp, max_timestamp=None,
                     base_index=None, end_index=None):
        if (max_timestamp is not None and
                min_timestamp is not None and
                max_timestamp - min_timestamp < 3600):
            return HeapRecord(-1, min_timestamp)
        if base_index is None:
            base_index = self.search_timestamp_before(
                min_timestamp, 0, len(self.timestamps))
        if end_index is None and max_timestamp is not None:
            end_index = self.search_timestamp_before(
                max_timestamp, 0, len(self.timestamps))
            if max_timestamp == self.timestamps[end_index + 1]:
                end_index += 1
        return self.result(min_timestamp, base_index, end_index)


class DisjointSixtyMinuteTracker(object):

    def __init__(self):
        self.trackers = []
        self.base_timestamp = None

    def receive(self, timestamp):
        if self.base_timestamp is None:
            self.base_timestamp = timestamp
        tracker_index = (timestamp - self.base_timestamp)/3600
        if len(self.trackers) <= tracker_index:
            for i in range(tracker_index - len(self.trackers)):
                self.trackers.append(None)
            self.trackers.append(SimpleSixtyMinuteTracker())
        self.trackers[tracker_index].receive(timestamp)
        if tracker_index > 0:
            self.trackers[tracker_index - 1].receive(timestamp)

    def result(self):
        heap = FansiteHeap()
        heap.max_size = 30
        for i, tracker in enumerate(self.trackers):
            start_timestamp = self.base_timestamp + i * 3600
            if tracker:
                heap.checkAndUpdate((tracker.result(start_timestamp), i))
        temporary_list = sorted(heap)
        return self.compute_final_list(temporary_list)

    def compute_final_list(self, temporary_list):
        i = 0
        final_list = []
        modify = {
            'min_timestamps': {},
            'max_timestamps': {},
            'marked': set()
        }
        while len(final_list) < 10 and len(temporary_list) != 0:
            result, index = temporary_list.pop()
            if index in modify['marked']:
                modify['marked'].remove(index)
                min_timestamp = modify['min_timestamps'].get(index)
                max_timestamp = modify['max_timestamps'].get(index)
                base_index = None
                end_index = None
                if min_timestamp is None:
                    min_timestamp = self.base_timestamp + index*3600
                    base_index = 0
                elif max_timestamp is None:
                    end_index = len(self.trackers[index].timestamps)
                new_result = self.trackers[index].slice_result(
                    min_timestamp, max_timestamp, base_index, end_index)
                self.insert_sorted(temporary_list, (new_result, index))
            else:
                final_list.append(result)
                start_timestamp = result.key
                modify['min_timestamps'][index + 1] = start_timestamp + 3601
                modify['max_timestamps'][index - 1] = start_timestamp - 1
                modify['marked'].add(index + 1)
                modify['marked'].add(index - 1)
        return final_list

    @staticmethod
    def insert_sorted(temporary_list, element):
        min_index = 0
        max_index = len(temporary_list)
        while min_index < max_index:
            i = (min_index + max_index)/2
            if element < temporary_list[i]:
                max_index = i
            else:
                min_index = i + 1
        temporary_list.insert(min_index, element)
