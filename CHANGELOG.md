# Changelog

## Release 0.2.1 (2019-10-18T12:38:12)

- Using env var set in zuul config
- Revert "[WIP]Use .zuul.yaml for pytest env vars instead of .env"
- Use .zuul.yaml for pytest env vars instead of .env
- Update Version number to create a new release
- Initial dependency lock
- Add Pipfile for dependency management
- Add .env file for prometheus url to run pytest
- Update README.md
- Add a .coafile And fix coala errors
- py linting and coala fixes
- Added kebechet support
- Delete .stickler.yml
- added Thoth's Zuul and Coala config (#44)
- Remove matplotlib warning
- bump version number to 0.0.2b4 for a new pre-release
- Update example notebook
- Remove dateparser as a dependency and use datetime objects in PrometheusConnect Use datetime objects for metric start_time and end_time. Use timedelta objects for chunk_size. Add tests for class PrometheusConnect Move pretty_print_metric function to utils.py
- Update README.md
- Update .stickler.yml
- Update .stickler.yml
- Create pyproject.toml
- Update .stickler.yml
- Format using black No code changes
- No strings for datetime input for Metric class constructor For `oldest_data_datetime` parameter, the only accepted input types are `datetime.datetime`/`datetime.timedelta` or `NoneType`
- Create .zuul.yaml
- Remove duplicate stored metrics from repo root
- dateparser unexpected behaviour fix, now use the timestamp to convert numpy.datetime64 to datetime.datetime (#23)
- Update MetricsList constructor
- Add unit tests for class `Metric` and `MetricsList`
- Update metric.py
- Add properties `start_time` and `end_time` (datetime objects) to the `Metric` class
- Added optional argument for GET params to all query functions + style fixes
- minor: style fixes
- Added option to specify GET params in custom_query()
- init a Metric object from an existing Metric object
- Update version number for v0.0.2b1 release
- Update Sphinx doc V0.0.2 (#15)
- Update documentation (#14)
- Add example notebook for Metric and MetricsList classes
- Add a Metric Class to make metric data processing easier. Also create a MetricsList class which directly takes the metric data received from prometheus and makes processing it easier
- Update .stickler.yml
- Update .stickler.yml
- Update README.md
- Adding .stickler.yml
- Add Sphinx Documentation configuration
- Change Package name to `prometheus-api-client`
- Update setup.py. Update `__init__.py`
- Add codacy code quality badge to the README.md
- Add a method in class PrometheusConnect for making custom queries to Prometheus. Fix some documentation
- Add documentation for the class and its methods.
- Add example usage in app.py
- Add function to store metrics locally Add function to print metric data Add requirements.txt
- Fix request query for `get_current_metric_value`
- Add basic methods to request data from prometheus

## Release 0.3.0 (2020-06-11T15:21:52)
* Template for issue creation
* :pushpin: Automatic update of dependency pandas from 1.0.3 to 1.0.4
* added numpy to requirements.txt
* added params argument
* added tests for metric_aggregation
* removed metric_aggregation class
* fix linter errors
* fixed import issues
* added doc strings
* fixed doc string
* code cleaning
* code cleaning and adding adding doc strings
* fixed data processing
* added aggregation class
* :pushpin: Automatic update of dependency matplotlib from 3.2.0 to 3.2.1
* :pushpin: Automatic update of dependency pandas from 1.0.2 to 1.0.3
* Add MetricSnapshotDataFrame module to generate docs config. Update docstring. Addresses #93
* Add Coala Linter
* :pushpin: Automatic update of dependency pandas from 1.0.1 to 1.0.2
* :pushpin: Automatic update of dependency dateparser from 0.7.2 to 0.7.4
* Fixed lint error - missing period in summary line
* Fixed lint errors. Replaced assert for better code quality
* Added some tests for MetricSnapshotDataFrame
* Added initial implementation of MetricSnapshotDataFrame. Addresses #86
* :pushpin: Automatic update of dependency matplotlib from 3.1.3 to 3.2.0
* :pushpin: Automatic update of dependency matplotlib from 3.1.3 to 3.2.0
* Fix Lint Errors
* :pushpin: Automatic update of dependency requests from 2.22.0 to 2.23.0
* Update .thoth.yaml
* Update .thoth.yaml
* :pushpin: Automatic update of dependency pandas from 1.0.0 to 1.0.1
* try to make codacy happy
* Base testcase for network mocking, test for PrometheusConnect. solves #38
* :pushpin: Automatic update of dependency matplotlib from 3.1.2 to 3.1.3
* :pushpin: Automatic update of dependency pandas from 0.25.3 to 1.0.0
* add exception module to docs build
* Upd missed Exception rising, upd docstrings
* Replace Exception to internal exception class
* method to access prometheus query_range HTTP API
* :pushpin: Automatic update of dependency matplotlib from 3.1.1 to 3.1.2
* :pushpin: Automatic update of dependency pandas from 0.25.2 to 0.25.3
* :pushpin: Automatic update of dependency pandas from 0.25.1 to 0.25.2

## Release 0.3.1 (2020-06-11T16:13:10)
* Update setup.py setup.py should get version info directly from __init__.py
* :pushpin: Automatic update of dependency dateparser from 0.7.4 to 0.7.5
* Release of version 0.3.0
* Update .coafile
* Template for issue creation
* :pushpin: Automatic update of dependency pandas from 1.0.3 to 1.0.4
* added numpy to requirements.txt
* added params argument
* added tests for metric_aggregation
* removed metric_aggregation class
* fix linter errors
* fixed import issues
* added doc strings
* fixed doc string
* code cleaning
* code cleaning and adding adding doc strings
* fixed data processing
* added aggregation class
* :pushpin: Automatic update of dependency matplotlib from 3.2.0 to 3.2.1
* :pushpin: Automatic update of dependency pandas from 1.0.2 to 1.0.3
* Add MetricSnapshotDataFrame module to generate docs config. Update docstring. Addresses #93
* Add Coala Linter
* :pushpin: Automatic update of dependency pandas from 1.0.1 to 1.0.2
* :pushpin: Automatic update of dependency dateparser from 0.7.2 to 0.7.4
* Fixed lint error - missing period in summary line
* Fixed lint errors. Replaced assert for better code quality
* Added some tests for MetricSnapshotDataFrame
* Added initial implementation of MetricSnapshotDataFrame. Addresses #86
* :pushpin: Automatic update of dependency matplotlib from 3.1.3 to 3.2.0
* :pushpin: Automatic update of dependency matplotlib from 3.1.3 to 3.2.0
* Fix Lint Errors
* :pushpin: Automatic update of dependency requests from 2.22.0 to 2.23.0
* Update .thoth.yaml
* Update .thoth.yaml
* :pushpin: Automatic update of dependency pandas from 1.0.0 to 1.0.1
* try to make codacy happy
* Base testcase for network mocking, test for PrometheusConnect. solves #38
* :pushpin: Automatic update of dependency matplotlib from 3.1.2 to 3.1.3
* :pushpin: Automatic update of dependency pandas from 0.25.3 to 1.0.0
* add exception module to docs build
* Upd missed Exception rising, upd docstrings
* Replace Exception to internal exception class
* method to access prometheus query_range HTTP API
* :pushpin: Automatic update of dependency matplotlib from 3.1.1 to 3.1.2
* :pushpin: Automatic update of dependency pandas from 0.25.2 to 0.25.3
* :pushpin: Automatic update of dependency pandas from 0.25.1 to 0.25.2
* Release of version 0.2.1
* Using env var set in zuul config
* Revert "[WIP]Use .zuul.yaml for pytest env vars instead of .env"
* Use .zuul.yaml for pytest env vars instead of .env
* Update Version number to create a new release
* Initial dependency lock
* Add Pipfile for dependency management
* Add .env file for prometheus url to run pytest
* Update README.md
* Add a .coafile And fix coala errors
* py linting and coala fixes
* Added kebechet support
* Delete .stickler.yml
* added Thoth's Zuul and Coala config (#44)
* Remove matplotlib warning
* bump version number to 0.0.2b4 for a new pre-release
* Update example notebook
* Remove dateparser as a dependency and use datetime objects in PrometheusConnect Use datetime objects for metric start_time and end_time. Use timedelta objects for chunk_size. Add tests for class PrometheusConnect Move pretty_print_metric function to utils.py
* Update README.md
* Update .stickler.yml
* Update .stickler.yml
* Create pyproject.toml
* Update .stickler.yml
* Format using black No code changes
* No strings for datetime input for Metric class constructor For `oldest_data_datetime` parameter, the only accepted input types are `datetime.datetime`/`datetime.timedelta` or `NoneType`
* Create .zuul.yaml
* Remove duplicate stored metrics from repo root
* dateparser unexpected behaviour fix, now use the timestamp to convert numpy.datetime64 to datetime.datetime (#23)
* Update MetricsList constructor
* Add unit tests for class `Metric` and `MetricsList`
* Update metric.py
* Add properties `start_time` and `end_time` (datetime objects) to the `Metric` class
* Added optional argument for GET params to all query functions + style fixes
* minor: style fixes
* Added option to specify GET params in custom_query()
* init a Metric object from an existing Metric object
* Update version number for v0.0.2b1 release
* Update Sphinx doc V0.0.2 (#15)
* Update documentation (#14)
* Add example notebook for Metric and MetricsList classes
* Add a Metric Class to make metric data processing easier. Also create a MetricsList class which directly takes the metric data received from prometheus and makes processing it easier
* Update .stickler.yml
* Update .stickler.yml
* Update README.md
* Adding .stickler.yml
* Add Sphinx Documentation configuration
* Change Package name to `prometheus-api-client`
* Update setup.py. Update __init__.py
* Add codacy code quality badge to the README.md
* Add a method in class PrometheusConnect for making custom queries to Prometheus. Fix some documentation
* Add documentation for the class and its methods.
* Add example usage in app.py
* Add function to store metrics locally Add function to print metric data Add requirements.txt
* Fix request query for `get_current_metric_value`
* Add basic methods to request data from prometheus
