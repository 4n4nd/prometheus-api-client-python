# Changelog

## Release 0.5.0 (2021-12-14T17:53:42)
* update deps and change python version in pipfile to 3.8
* Add check to ensure valid input for timestamps in metric range fnc.
* Update .pre-commit-config.yaml
* Fix docs formatting
* README.md example codes fix (#213)
* Update OWNERS file (#212)
* update pytest prom url since operatefirst url is now behind a proxy (#210)
* :hatching_chick: fix of the naming which is causing dependency update failure
* Update test prometheus url to operate-first prometheus (#194)
* :arrow_up: Bump pillow from 8.0.1 to 8.1.1
* Added slack and google chat link (#189)
* fix documentation formatting (#187)
* Release of version 0.4.2 (#186)
* Add method to check connection to Prometheus (#181)
*  feat: replaced exit with ValueError (#182)
* Add MetricRangeDataFrame to RTD. Add sphinx to Pipfile. (#177)
* :pushpin: Automatic update of dependency httmock from 1.3.0 to 1.4.0 (#172)
* :pushpin: Automatic update of dependency numpy from 1.19.2 to 1.19.4 (#171)
* :pushpin: Automatic update of dependency matplotlib from 3.3.2 to 3.3.3 (#170)
* :pushpin: Automatic update of dependency dateparser from 0.7.6 to 1.0.0 (#168)
* :pushpin: Automatic update of dependency requests from 2.24.0 to 2.25.0 (#167)
* Update example notebook (#166)
* Add description of MetricSnapshotDataFrame,MetricRangeDataFrame to README
* :pushpin: Automatic update of dependency numpy from 1.19.1 to 1.19.2 (#162)
* :pushpin: Automatic update of dependency numpy from 1.19.1 to 1.19.2 (#161)
* :pushpin: Automatic update of dependency matplotlib from 3.3.1 to 3.3.2 (#160)
* :pushpin: Automatic update of dependency numpy from 1.19.1 to 1.19.2 (#155)
* :pushpin: Automatic update of dependency matplotlib from 3.3.1 to 3.3.2 (#158)
* :pushpin: Automatic update of dependency pandas from 1.1.1 to 1.1.2 (#154)
* :sparkles: fixes to make pre-commit happy
* :sparkles: now with an OWNERS file, so that Thoth bots can help you even more
* Updating the readme
* Release of version 0.4.1 (#151)
* :pushpin: Automatic update of dependency matplotlib from 3.3.0 to 3.3.1 (#148)
* :pushpin: Automatic update of dependency matplotlib from 3.3.0 to 3.3.1 (#147)
* :pushpin: Automatic update of dependency pandas from 1.1.0 to 1.1.1 (#146)
* Updated the get_metric_aggregations to return global aggregations for both range query and current time query
* :hatching_chick: follow pre-commit compliance for the application
* Make tests pass: ensure ordering of fixtures. (#140)
* :truck: include aicoe-ci configuration file with pytest env vars
* Deduplicate creation of MetricsList.
* add metricrangedf and tests (#137)
* :pushpin: Automatic update of dependency pandas from 1.0.5 to 1.1.0
* Release of version 0.4.0
* Document retry
* :pushpin: Automatic update of dependency numpy from 1.19.0 to 1.19.1
* :pushpin: Automatic update of dependency matplotlib from 3.2.2 to 3.3.0
* Retry the proper way
* Updated the pipfile and the requirement.txt file
* :pushpin: Automatic update of dependency matplotlib from 3.2.1 to 3.2.2
* :pushpin: Automatic update of dependency pandas from 1.0.4 to 1.0.5
* :pushpin: Automatic update of dependency requests from 2.23.0 to 2.24.0
* :pushpin: Automatic update of dependency dateparser from 0.7.5 to 0.7.6
* Update README.md
* Update README.md
* Update README.md
* Release of version 0.3.1
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

## Release 0.4.0 (2020-07-28T11:21:26)
* Document retry
* :pushpin: Automatic update of dependency numpy from 1.19.0 to 1.19.1
* :pushpin: Automatic update of dependency matplotlib from 3.2.2 to 3.3.0
* Retry the proper way
* Updated the pipfile and the requirement.txt file
* :pushpin: Automatic update of dependency matplotlib from 3.2.1 to 3.2.2
* :pushpin: Automatic update of dependency pandas from 1.0.4 to 1.0.5
* :pushpin: Automatic update of dependency requests from 2.23.0 to 2.24.0
* :pushpin: Automatic update of dependency dateparser from 0.7.5 to 0.7.6
* Update README.md
* Update README.md
* Update README.md

## Release 0.4.1 (2020-09-02T12:18:03)
### Features
* Updated the get_metric_aggregations to return global aggregations for both range query and current time query
* :hatching_chick: follow pre-commit compliance for the application
* :truck: include aicoe-ci configuration file with pytest env vars
* add metricrangedf and tests (#137)
### Improvements
* Make tests pass: ensure ordering of fixtures. (#140)
* Deduplicate creation of MetricsList.
### Automatic Updates
* :pushpin: Automatic update of dependency matplotlib from 3.3.0 to 3.3.1 (#148)
* :pushpin: Automatic update of dependency matplotlib from 3.3.0 to 3.3.1 (#147)
* :pushpin: Automatic update of dependency pandas from 1.1.0 to 1.1.1 (#146)
* :pushpin: Automatic update of dependency pandas from 1.0.5 to 1.1.0

## Release 0.4.2 (2020-12-03T16:47:55)
### Features
* Add method to check connection to Prometheus (#181)
*  feat: replaced exit with ValueError (#182)
* Add MetricRangeDataFrame to RTD. Add sphinx to Pipfile. (#177)
* Update example notebook (#166)
* Add description of MetricSnapshotDataFrame,MetricRangeDataFrame to README
* :sparkles: now with an OWNERS file, so that Thoth bots can help you even more
* Updating the readme
### Bug Fixes
* :sparkles: fixes to make pre-commit happy
### Automatic Updates
* :pushpin: Automatic update of dependency httmock from 1.3.0 to 1.4.0 (#172)
* :pushpin: Automatic update of dependency numpy from 1.19.2 to 1.19.4 (#171)
* :pushpin: Automatic update of dependency matplotlib from 3.3.2 to 3.3.3 (#170)
* :pushpin: Automatic update of dependency dateparser from 0.7.6 to 1.0.0 (#168)
* :pushpin: Automatic update of dependency requests from 2.24.0 to 2.25.0 (#167)
* :pushpin: Automatic update of dependency numpy from 1.19.1 to 1.19.2 (#162)
* :pushpin: Automatic update of dependency numpy from 1.19.1 to 1.19.2 (#161)
* :pushpin: Automatic update of dependency matplotlib from 3.3.1 to 3.3.2 (#160)
* :pushpin: Automatic update of dependency numpy from 1.19.1 to 1.19.2 (#155)
* :pushpin: Automatic update of dependency matplotlib from 3.3.1 to 3.3.2 (#158)
* :pushpin: Automatic update of dependency pandas from 1.1.1 to 1.1.2 (#154)
