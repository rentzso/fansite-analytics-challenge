import heapq
from collections import namedtuple


class HeapRecord(namedtuple('HeapRecord', ['statistic', 'key'])):
    """
    namedtuple to store records contained in a FansiteHeap.
    """

    def __lt__(self, other):
        return (
            self.statistic < other.statistic or
            (self.statistic == other.statistic and self.key > other.key)
        )

    def __gt__(self, other):
        return (
            self.statistic > other.statistic or
            (self.statistic == other.statistic and self.key < other.key)
        )

    def __le__(self, other):
        return (
            self.statistic < other.statistic or
            (self.statistic == other.statistic and self.key >= other.key)
        )

    def __ge__(self, other):
        return (
            self.statistic > other.statistic or
            (self.statistic == other.statistic and self.key <= other.key)
        )


class FansiteHeap(list):
    """
    Wrap a list using heapq to implement a min-heap with 10 elements
    """
    max_size = 10

    def checkAndUpdate(self, element):
        if len(self) < self.max_size:
            heapq.heappush(self, element)
            return True
        elif element > self[0]:
            heapq.heapreplace(self, element)
            return True
        else:
            return False


def heap_postprocessing(statistics):
    """
    Iterate through a list of key, statistic pairs and uses a FansiteHeap
    to collect the 10 keys with the top statistic.
    """
    stats_heap = FansiteHeap()
    for key, statistic in statistics.iteritems():
        stats_heap.checkAndUpdate(HeapRecord(statistic, key))
    stats_heap.sort(reverse=True)
    return stats_heap
