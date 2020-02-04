MARKERS = [
    "e2e: tests that communicates with external services, such as Prometheus",
]


def pytest_configure(config):
    # register an additional markers
    for markerline in MARKERS:
        config.addinivalue_line("markers", markerline)
