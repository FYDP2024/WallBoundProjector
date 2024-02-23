class SimpleMovingAverage:
    def __init__(self, period):
        self.period = period
        self.data_points = []

    def add_data_point(self, data_point):
        if data_point is not None:
            self.data_points.append(data_point)
            if len(self.data_points) > self.period:
                self.data_points.pop(0)  # Remove the oldest data point

    def calculate_sma(self):
        if len(self.data_points) == 0:
            return 0  # Handle case with no data
        return sum(self.data_points) / len(self.data_points)