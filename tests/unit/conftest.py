from urllib.parse import urlparse

import pytest

from httmock import HTTMock, all_requests, response, urlmatch


def mock_response(
        content, url=None, path='', headers=None, response_url=None, status_code=200, cookies=None, func=None
):
    """Universal handler for specify mocks inplace"""
    if func is None:

        def mocked(url, request):
            mock = response(
                status_code=status_code, content=content, request=request, headers=headers
            )
            if cookies:
                mock.cookies = cookies
            mock.url = response_url if response_url else url
            return mock

    else:
        mocked = func

    if url:
        parsed = urlparse(url)
        return urlmatch(netloc=parsed.netloc, path=parsed.path)(func=mocked)
    elif path:
        return urlmatch(path=path)(func=mocked)
    else:
        return all_requests(func=mocked)


class ResponseMock(HTTMock):
    called = False
    call_count = 0

    def intercept(self, request, **kwargs):
        resp = super(ResponseMock, self).intercept(request, **kwargs)
        if resp and self.log_requests:
            self.called = True
            self.call_count += 1
            self.requests.append(request)
        return resp

    def __init__(self, *args, log_requests=True, **kwargs):
        handler = mock_response(*args, **kwargs)
        self.log_requests = log_requests
        self.requests = []
        super().__init__(handler)


@pytest.fixture
def mocked_response():
    return ResponseMock


@pytest.fixture(scope="module", autouse=True)
def block_network():
    """
    Block all network connections for unittests
    """

    with ResponseMock("BOOM!", status_code=403):
        yield
