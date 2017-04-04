from fansiteheap import FansiteHeap, HeapRecord
import lineparser
import pdb

class SixtyMinuteTracker(object):
    """
    Class to compute the 10 most active 60-min windows.

    After initialization, the method "receive" is called once for each
    event passing the event timestamp.
    When all the events are collected calling the method "result" computes
    the sorted list of the 10 most active windows.

    attributes
    ----------------
    timestamps:
    list to collect all the timestamps for which there was at least one
    event (with an additional artificial -1 at the 0 index)

    counts:
    dictionary that maps each timestamp to the total_count of events until
    that timestamp (to the key -1 corresponds artificially a total_count of 0)
    """

    def __init__(self):
        self.counts = {-1: 0}
        self.timestamps = [-1]
        self._total_count = 0

    def receive(self, timestamp):
        """
        Collect an event occurrence at the second "timestamp"
        """
        self._total_count += 1
        self.counts[timestamp] = self._total_count
        if self.timestamps[-1] != timestamp:
            self.timestamps.append(timestamp)

    def result(self):
        # Create a min-heap to collect the top 60-min windows
        heap = FansiteHeap()
        if len(self.timestamps) == 1:
            return heap
        # The base_index is the index in the self.timestamps immediately
        # before the start timestamp of the 60-min window that is currently
        # evaluated. Using self.counts[self.timestamp[base_index]] returns
        # the number of events before the current window started
        base_index = 0
        # In a similar fashion last_index is the index of the last timestamp
        # that is included in the 60-min window from the difference between
        # the count at this timestamp. The first window we consider is
        # [self.timestamps[1], self.timestamps[1] + 3600]
        last_index = self.search_timestamp_before(
            self.timestamps[1] + 3600, 0, min(3601, len(self.timestamps))
        )
        if (len(self.timestamps) > last_index + 1 and
                self.timestamps[last_index + 1] == self.timestamps[1] + 3600):
            last_index = last_index + 1
        # After collecting the information needed for the first windows we
        # update the heap.


        self._update_heap(heap, self.timestamps[1], base_index, last_index)
        # The result is returned sorted in reverse order from greatest to
        # lowest count.
        return sorted(heap, reverse=True)

    def search_timestamp_before(self, search_timestamp, min_index, max_index):
        """
        Binary search used to find the index of the timestamp in
        self.timestamps occurring at or after "search_timestamp".
        "search_timestamp" is supposed to be between self.timestamps[min_index]
        and self.timestamps[max_index] if max_index is a valid index.
        If not, there is no upper bound).
        """
        while max_index - min_index > 1:
            i = (max_index + min_index)/2
            timestamp = self.timestamps[i]
            if search_timestamp == timestamp:
                return i - 1
            elif search_timestamp < timestamp:
                max_index = i
            else:
                min_index = i
        return min_index

    def _update_heap(self, heap, start_timestamp, base_index, last_index):
        """
        Update the heap with candidate windows.
        This method is called multiple times in self.result().

        inputs
        ---------
        heap:            min-heap tracking the top 60-min windows
        start_timestamp: where the first candidate window begins
        base_index:      the first index falling out of the first window
        last_index:      the last index falling in the first window
        """
        base_count = self.counts[self.timestamps[base_index]]
        last_count = self.counts[self.timestamps[last_index]]
        end_timestamp = start_timestamp + 3600

        max_timestamp = self.timestamps[-1]
        while start_timestamp <= max_timestamp:
            # this computes the number of event within the window
            # starting at start_timestamp.
            count = last_count - base_count
            startdate = lineparser.retrieve_date(start_timestamp)
            heap.checkAndUpdate(HeapRecord(count, startdate))
            # start_timestamp + 1 will go out of the window in the next
            # iteration. We update the base_count if needed.
            # and we update the last_count also if we need to have reached a timestamp
            # with some requests.
            base_count = self.counts.get(start_timestamp, base_count)
            start_timestamp += 1
            end_timestamp += 1
            last_count = self.counts.get(end_timestamp, last_count)
