from collections import namedtuple


class LoginTracker(object):
    """
    LoginTracker tracks failed login requests.
    If there have been, more than 3 failed login requests from a single host
    in the last 20 seconds, it marks all the request within 5 minutes from
    the last failure as blocked.

    attributes
    ---------------
    tracked:
    A dictionary tracking the state of each host
    The state is updated to keep track of how many login failure there have
    been in the last 20 seconds.
    """

    def __init__(self):
        self.tracked = {}

    def receive(self, request):
        """
        Handle a request and dispatch it to the right handler.
        ---------------------
        The return value is a boolean telling if the request should
        have been blocked or not.
        """
        if request.resource == '/login' and request.request_method == 'POST':
            if 400 <= request.http_code < 500:
                return self.failed_login(request.host, request.timestamp)
            else:
                return self.successful_login(request.host, request.timestamp)
        else:
            return self.standard_request(request.host, request.timestamp)

    def failed_login(self, host, timestamp):
        """
        Handle a failed login.
        -----------------------
        If there are already 3 failed requests in the host state, we check
        if the last failed request triggering the block, happened less than
        300 seconds before.
        """
        state = self.tracked.get(host)
        if state is None:
            self.tracked[host] = [timestamp]
            return False
        elif len(state) == 3 and (timestamp - state[2]) <= 300:
            return True
        else:
            new_state = state + [timestamp]
            self.tracked[host] = filter(
                lambda t: (timestamp - t) <= 20,
                new_state)
            return False

    def successful_login(self, host, timestamp):
        """
        Handle a successful login.
        -----------------------
        If requests are not being marked as blocked in the input timestamp,
        we clear the state of the host in self.tracked.
        """
        state = self.tracked.get(host)
        if state is None:
            return False
        elif len(state) == 3 and (timestamp - state[2]) <= 300:
            return True
        else:
            del self.tracked[host]
            return False

    def standard_request(self, host, timestamp):
        """
        Handle a standard request.
        -----------------------
        Depending on the tracked state of the host a request is marked as
        blocked or not.
        """
        state = self.tracked.get(host)
        if state is None:
            return False
        elif len(state) == 3 and (timestamp - state[2]) <= 300:
            return True
        else:
            return False
