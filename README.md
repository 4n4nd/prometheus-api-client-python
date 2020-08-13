# prometheus-api-client

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7d838be9b51e4daaa20be1772f5c9ad2)](https://www.codacy.com/manual/4n4nd/prometheus-api-client-python?utm_source=github.com&utm_medium=referral&utm_content=AICoE/prometheus-api-client-python&utm_campaign=Badge_Grade) [![PyPI version](https://badge.fury.io/py/prometheus-api-client.svg)](https://badge.fury.io/py/prometheus-api-client) [![PyPI download month](https://img.shields.io/pypi/dm/prometheus-api-client.svg)](https://pypi.python.org/pypi/prometheus-api-client/)

A Python wrapper for the Prometheus http api and some tools for metrics processing.

## Installation

To install the latest release:

`pip install prometheus-api-client`

To install directly from this branch:

`pip install https://github.com/AICoE/prometheus-api-client-python/zipball/master`

## Links

- [Documentation](https://prometheus-api-client-python.readthedocs.io/en/master/source/prometheus_api_client.html)

## Running tests

`PROM_URL="http://prometheus-route-aiops-prod-prometheus-predict.cloud.paas.psi.redhat.com/" pytest`

## Code Styling and Linting

Prometheus Api client uses [pre-commit](https://pre-commit.com) framework to maintain the code linting and python code styling.<br>
The AICoE-CI would run the pre-commit check on each pull request.<br>
We encourage our contributors to follow the same pattern, while contributing to the code.<br>
we would like to keep the same standard and maintain the code for better quality and readability.

The pre-commit configuration file is present in the repository `.pre-commit-config.yaml`<br>
It contains the different code styling and linting guide which we use for the application.

we just need to run [pre-commit](https://pre-commit.com/#install) before raising a Pull Request.<br>
Following command can be used to run the pre-commit:<br>
`pre-commit run --all-files`

If pre-commit is not installed in your system, it can be install with : `pip install pre-commit`
