from lineparser import ParsedRequest
from logintracker import LoginTracker

TEST_HOST = 'test.login.test'
NUM_BYTES = 1420
LOGIN_RESOURCE = '/login'
NON_LOGIN_RESOURCE = '/notalogin'


def get_request(timestamp, login, success):
    http_code = 200 if success else 401
    resource = LOGIN_RESOURCE if login else NON_LOGIN_RESOURCE
    return ParsedRequest(
        host=TEST_HOST,
        timestamp=timestamp,
        request_method='POST',
        resource=resource,
        http_code=http_code,
        bytes=1420)


def exec_one(request, tracker_instance, expected_result, expected_state):
    result = tracker_instance.receive(request)
    assert result == expected_result, (
        '{} != {}'.format(result, expected_result)
        )
    assert tracker_instance.tracked.get(TEST_HOST) == expected_state


def tracker(state=None):
    t = LoginTracker()
    if state is not None:
        t.tracked[TEST_HOST] = state
    return t


def test_none_state():
    expected_result = False
    expected_state = None
    yield (
        exec_one, get_request(0, True, True), tracker(),
        expected_result, expected_state)
    expected_result = False
    expected_state = [0]
    yield (
        exec_one, get_request(0, True, False), tracker(),
        expected_result, expected_state)
    expected_result = False
    expected_state = None
    yield (
        exec_one, get_request(0, False, False), tracker(),
        expected_result, expected_state)
    expected_result = False
    expected_state = None
    yield (
        exec_one, get_request(0, False, True), tracker(),
        expected_result, expected_state)


def test_one_state():
    one_state = [0]
    for t in (10, 20):
        expected_result = False
        expected_state = None
        yield (
            exec_one, get_request(t, True, True), tracker(one_state),
            expected_result, expected_state)
        expected_result = False
        expected_state = [0, t]
        yield (
            exec_one, get_request(t, True, False), tracker(one_state),
            expected_result, expected_state)
        expected_result = False
        expected_state = one_state
        yield (
            exec_one, get_request(t, False, False), tracker(one_state),
            expected_result, expected_state)
        expected_result = False
        expected_state = one_state
        yield (
            exec_one, get_request(t, False, True), tracker(one_state),
            expected_result, expected_state)
    t = 21
    expected_result = False
    expected_state = None
    yield (
        exec_one, get_request(t, True, True), tracker(one_state),
        expected_result, expected_state)
    expected_result = False
    expected_state = [t]
    yield (
        exec_one, get_request(t, True, False), tracker(one_state),
        expected_result, expected_state)
    expected_result = False
    expected_state = one_state
    yield (
        exec_one, get_request(t, False, False), tracker(one_state),
        expected_result, expected_state)
    expected_result = False
    expected_state = one_state
    yield (
        exec_one, get_request(t, False, True), tracker(one_state),
        expected_result, expected_state)


def test_two_state():
    two_state = [0, 8]
    for t in (10, 20):
        expected_result = False
        expected_state = None
        yield (
            exec_one, get_request(t, True, True), tracker(two_state),
            expected_result, expected_state)
        expected_result = False
        expected_state = [0, 8, t]
        yield (
            exec_one, get_request(t, True, False), tracker(two_state),
            expected_result, expected_state)
        expected_result = False
        expected_state = two_state
        yield (
            exec_one, get_request(t, False, False), tracker(two_state),
            expected_result, expected_state)
        expected_result = False
        expected_state = two_state
        yield (
            exec_one, get_request(t, False, True), tracker(two_state),
            expected_result, expected_state)
    t = 21
    expected_result = False
    expected_state = None
    yield (
        exec_one, get_request(t, True, True), tracker(two_state),
        expected_result, expected_state)
    expected_result = False
    expected_state = [8, t]
    yield (
        exec_one, get_request(t, True, False), tracker(two_state),
        expected_result, expected_state)
    expected_result = False
    expected_state = two_state
    yield (
        exec_one, get_request(t, False, False), tracker(two_state),
        expected_result, expected_state)
    expected_result = False
    expected_state = two_state
    yield (
        exec_one, get_request(t, False, True), tracker(two_state),
        expected_result, expected_state)
    t = 29
    expected_result = False
    expected_state = None
    yield (
        exec_one, get_request(t, True, True), tracker(two_state),
        expected_result, expected_state)
    expected_result = False
    expected_state = [t]
    yield (
        exec_one, get_request(t, True, False), tracker(two_state),
        expected_result, expected_state)
    expected_result = False
    expected_state = two_state
    yield (
        exec_one, get_request(t, False, False), tracker(two_state),
        expected_result, expected_state)
    expected_result = False
    expected_state = two_state
    yield (
        exec_one, get_request(t, False, True), tracker(two_state),
        expected_result, expected_state)


def test_blocked_state():
    blocked_state = [0, 8, 15]
    for t in (15, 50, 315):
        expected_result = True
        expected_state = blocked_state
        yield (
            exec_one, get_request(t, True, True), tracker(blocked_state),
            expected_result, expected_state)
        expected_result = True
        expected_state = blocked_state
        yield (
            exec_one, get_request(t, True, False), tracker(blocked_state),
            expected_result, expected_state)
        expected_result = True
        expected_state = blocked_state
        yield (
            exec_one, get_request(t, False, False), tracker(blocked_state),
            expected_result, expected_state)
        expected_result = True
        expected_state = blocked_state
        yield (
            exec_one, get_request(t, False, True), tracker(blocked_state),
            expected_result, expected_state)
    t = 330
    expected_result = False
    expected_state = None
    yield (
        exec_one, get_request(t, True, True), tracker(blocked_state),
        expected_result, expected_state)
    expected_result = False
    expected_state = [t]
    yield (
        exec_one, get_request(t, True, False), tracker(blocked_state),
        expected_result, expected_state)
    expected_result = False
    expected_state = blocked_state
    yield (
        exec_one, get_request(t, False, False), tracker(blocked_state),
        expected_result, expected_state)
    expected_result = False
    expected_state = blocked_state
    yield (
        exec_one, get_request(t, False, True), tracker(blocked_state),
        expected_result, expected_state)
