from math import log
from task_2.distributions import *


class DistEX(Dist):
    NAME = 'Общее экспоненциальное распределение'

    def __init__(self, params):
        self.a = Dist.extract_param(params, 'p1', Dist.default_param, DEFAULT_INTERVAL_A, 'a')
        self.b = Dist.extract_param(params, 'p2', Dist.default_param, DEFAULT_INTERVAL_B, 'b')
        assert self.a < self.b, 'Числа а и b должны составлять непустой интервал (a, b)'

        super().__init__()

    def transform(self, values):
        values_standard = Dist.transform_standard(values)
        values_out = [-self.b * log(value) + self.a for value in values_standard]
        return values_out
