"""A Class for performing aggregation operations on a query values."""
import logging
import math
import statistics

_LOGGER = logging.getLogger(__name__)


class MetricAggregation:
    """
    A Class to perform aggregation operations on the metric values.

    :param operations: (list) A list of operations to perform on the values.
    Operations are specified in string type.
    Available operations - sum, max, min, variance, nth percentile, deviation
    and average.
    :param values: (list) A list of values to perform operation on.
    These are the metric values(int|float).

    """

    def __init__(self, values, operations):
        """Class MetricAggregation constructor."""
        if not isinstance(operations, list):
            raise TypeError("Operations can be only of type list")

        if not isinstance(values, list):
            raise TypeError("Values can be only of type list")

        if len(values) == 0:
            _LOGGER.debug("No values found for given query.")
            return None

        if len(operations) == 0:
            _LOGGER.debug("No operations found to perform")
            return None

        self.values = values
        self.operations = operations
        self.output = {}

    def get_max(self):
        """Find the maximum value."""
        self.output['max'] = max(self.values)

    def get_min(self):
        """Find the minimum value."""
        self.output['min'] = min(self.values)

    def get_sum(self):
        """Find the sum of the values."""
        self.output['sum'] = sum(self.values)

    def get_average(self):
        """Find the average of the values."""
        avg = sum(self.values) / len(self.values)
        self.output['average'] = avg

    def get_percentile(self, percentile):
        """Find the nth percentile of the values."""
        size = len(self.values)
        self.output['percentile_' + str(percentile)] = sorted(self.values)[
            int(math.ceil((size * percentile) / 100)) - 1]

    def get_deviation(self):
        """Find the standard deviation of the values."""
        self.output['deviation'] = statistics.stdev(self.values)

    def get_variance(self):
        """Find the variance of the values."""
        self.output['variance'] = statistics.variance(self.values)

    def process_values(self):
        """Iterate over each operation and call the respective function and finally return the output."""
        for operation in self.operations:
            if operation == "sum":
                self.get_sum()
            elif operation == "max":
                self.get_max()
            elif operation == "min":
                self.get_min()
            elif operation == "average":
                self.get_average()
            elif operation.startswith("percentile"):
                percentile = float(operation.split('_')[1])
                self.get_percentile(percentile)
            elif operation == "deviation":
                self.get_deviation()
            elif operation == "variance":
                self.get_variance()
            else:
                raise TypeError("Invalid operation!")
        return self.output
