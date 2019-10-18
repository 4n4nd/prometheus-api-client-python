
## Release 0.2.1 (2019-10-18T12:38:12)
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
