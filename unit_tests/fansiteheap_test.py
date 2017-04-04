import heapq
from fansiteheap import HeapRecord, FansiteHeap


def test_less_than():
    assert HeapRecord(4, 'localhost') < HeapRecord(4, 'amaxon.host')
    assert HeapRecord(3, 'amaxon.host') < HeapRecord(4, 'localhost')


def test_greater_than():
    assert HeapRecord(4, 'localhost') > HeapRecord(3, 'amaxon.host')
    assert HeapRecord(4, 'amaxon.host') > HeapRecord(4, 'localhost')


def test_greater_than_or_equal():
    assert HeapRecord(4, 'localhost') >= HeapRecord(4, 'localhost')
    assert HeapRecord(4, 'amaxon.host') >= HeapRecord(4, 'amaxon.host')
    assert HeapRecord(4, 'localhost') >= HeapRecord(3, 'amaxon.host')
    assert HeapRecord(4, 'amaxon.host') >= HeapRecord(4, 'localhost')


def test_less_than_or_equal():
    assert HeapRecord(4, 'localhost') >= HeapRecord(4, 'localhost')
    assert HeapRecord(4, 'amaxon.host') >= HeapRecord(4, 'amaxon.host')
    assert HeapRecord(4, 'localhost') <= HeapRecord(4, 'amaxon.host')
    assert HeapRecord(3, 'amaxon.host') <= HeapRecord(4, 'localhost')


def test_empty():
    ah = FansiteHeap()
    element = HeapRecord(4, 'localhost')
    ah.checkAndUpdate(element)
    assert ah[0] == element


def test_nine_elements():
    heap = [HeapRecord(i, 'localhost.{}'.format(i)) for i in range(9)]
    heapq.heapify(heap)
    ah = FansiteHeap(heap)
    element = HeapRecord(-4, 'localhost')
    ah.checkAndUpdate(element)
    assert ah[0] == element
    assert len(ah) == 10


def test_ten_elements_no_action():
    heap = [HeapRecord(i, 'localhost.{}'.format(i)) for i in range(10)]
    heapq.heapify(heap)
    ah = FansiteHeap(heap)
    element = HeapRecord(-4, 'localhost')
    ah.checkAndUpdate(element)
    assert ah[0] == (0, 'localhost.0')
    assert len(ah) == 10


def test_ten_elements_with_action():
    heap = [HeapRecord(i, 'localhost.{}'.format(i)) for i in range(10)]
    heapq.heapify(heap)
    ah = FansiteHeap(heap)
    element = HeapRecord(1, 'localhost')
    ah.checkAndUpdate(element)
    assert ah[0] == (1, 'localhost.1')
    assert len(ah) == 10
