from math import log
from task_2.distributions import *


class DistLS(Dist):
    NAME = 'Логистическое распределение'

    def __init__(self, params):
        # параметры
        self.a = Dist.extract_param(params, 'p1', Dist.gen_param, DEFAULT_OFFSET_A, 'a')
        self.b = Dist.extract_param(params, 'p2', Dist.gen_param, DEFAULT_SCALE_B, 'b')
        # ассерты
        assert 0 < self.b, 'Масштаб распределения = {} должен быть положительным числом'.format(self.b)

        super().__init__()

    def transform(self, values):
        values_standard = Dist.transform_standard(values)
        return [self.a + self.b * log(u / (1 - u)) for u in values_standard]
