class diffTimeSeries:

    def __init__(self, timeseries, date):
        self.raw_series = timeseries
        self.diff_series = [self.raw_series[i] - self.raw_series[i-1] for i in range(1, len(self.raw_series))]
        self.basic = self.raw_series[0]
        self.date = date[1:]

    def __len__(self):
        return len(self.diff)

    def inverse_difference(self, last_ob, value):
        return value + last_ob

    def inverse_difference_series(self, diff_series):
        return [self.inverse_difference(self.raw_series[i], diff_series[i]) for i in range(len(diff_series))]
