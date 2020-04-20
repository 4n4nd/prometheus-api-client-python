import math
import statistics


class Metric_aggregation():
    def __init__(self, values, operations):
        self.values = values
        self.output = {}

        for operation in operations:
            if operation == "sum":
                self.get_sum()
            elif operation == "max":
                self.get_sum()
            elif operation == "min":
                self.get_min()
            elif operation == "average":
                self.get_average()
            elif operation.startswith("percentile"):
                percentile = operation.split('_')[1]
                self.get_percentile(percentile)
            elif operation == "deviation":
                self.get_deviation()
            elif operation == "variance":
                self.get_variance()

            return self.output


    def get_max(self):
        self.output['max'] = max(self.values)

    def get_min(self, values):
        self.output['min'] = min(self.values)

    def get_sum(self):
        self.output['sum'] = sum(self.values)

    def get_average(self):
        avg = sum(self.values) / len(self.values)
        self.output['average'] = avg

    def get_percentile(self, percentile):
        size = len(self.values)
        self.output['percentile_' + str(percentile)] = sorted(self.values)[
            int(math.ceil((size * percentile) / 100)) - 1]

    def get_deviation(self):
        self.output['deviation'] = statistics.stdev(self.values)

    def get_variance(self):
        self.output['variance'] = statistics.variance(self.values)
