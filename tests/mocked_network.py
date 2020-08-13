"""Test module for Base Mock Network."""

from urllib.parse import urlparse

from unittest import TestCase

from httmock import HTTMock, all_requests, response, urlmatch


def mock_response(
    content,
    url=None,
    path="",
    headers=None,
    response_url=None,
    status_code=200,
    cookies=None,
    func=None,
):
    """Universal handler for specify mocks inplace."""
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


class ResponseMock(HTTMock):  # noqa D101
    called = False
    call_count = 0

    def intercept(self, request, **kwargs):  # noqa D102
        resp = super(ResponseMock, self).intercept(request, **kwargs)
        if resp is not None and self.log_requests:
            self.called = True
            self.call_count += 1
            self.requests.append(request)
        return resp

    def __init__(self, *args, **kwargs):  # noqa D102
        log_requests = kwargs.pop("log_requests", True)
        handler = mock_response(*args, **kwargs)
        self.log_requests = log_requests
        self.requests = []
        super().__init__(handler)


class BaseMockedNetworkTestcase(TestCase):  # noqa D101
    def run(self, result=None):  # noqa D102
        with ResponseMock("BOOM!", status_code=403):
            return super().run(result)

    @property
    def mock_response(self):  # noqa D102
        return ResponseMock
