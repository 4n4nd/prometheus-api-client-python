"""plot code for metric class."""

# This only gets called if there's a plot() call
# This speeds up load time for all the non plot() users
#
# Only loads matplotlib etc during __init__
#

class MetricPlot:
    r"""
    A Class for `MetricPlot` object.

    Internal use only at present

    """

    def __init__(self, *args, **kwargs):
        """Functions as a Constructor for the Metric object."""
        try:
            import matplotlib.pyplot as plt
            from pandas.plotting import register_matplotlib_converters

            register_matplotlib_converters()
        except ImportError as exce:  # noqa F841
            raise ImportError("matplotlib was not found")

        # One graph with potentially N lines - if plot() is called twice
        self._plt = plt
        self._fig, self._axis = self._plt.subplots(*args, **kwargs)

    def plot_date(self, metric):
        """Plot a very simple line graph for the metric time-series."""

        # If we made it here, then we know matplotlib is installed and available
        self._axis.plot_date(metric.metric_values.ds, metric.metric_values.y,
            linestyle="solid",
            label=str(metric.metric_name),
        )
        self._fig.autofmt_xdate()
        # These are provided for documentation reasons only - it's presumptuous for this code to call them
        # self._axis.set_xlabel('Date/Time')
        # self._axis.set_ylabel('Metric')
        # self._axis.set_title('Prometheus')
        if len(self._axis.lines) > 1:
            # We show a legend (or update the legend) if there's more than line on the plot
            self._axis.legend()

    def show(self, block=None):
        """convience show() call."""
        self._plt.show(block=block)

    @property
    def plt(self):
        """ pyplot value for present plotting """
        return self._plt

    @property
    def axis(self):
        """ Axis value for present plotting """
        return self._axis

    @property
    def fig(self):
        """ Figure value for present plotting """
        return self._fig
