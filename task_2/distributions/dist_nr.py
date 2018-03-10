from math import sqrt, log, cos, pi
from task_2.distributions import *

DEFAULT_μ = (0.2, 0.8)
DEFAULT_σ = (0, 20)


class DistNR(Dist):
    NAME = 'Общий случай равномерного распределения'

    def __init__(self, params):
        # параметры
        self.μ = Dist.extract_param(params, 'p1', Dist.gen_param, DEFAULT_μ, 'μ')
        self.σ = Dist.extract_param(params, 'p2', Dist.gen_param, DEFAULT_σ, 'σ')
        # ассерты
        assert 0 < self.μ < 1, 'μ - математическое ожидание - должно быть в интервале (0, 1)'
        assert 0 <= self.σ, 'σ - среднеквадратичное отклонение - должно быть положительным числом'

        super().__init__()

    def transform(self, values):
        values_standard = Dist.transform_standard(values)
        values_in_1, values_in_2 = Dist.separate_values(values_standard)

        values_out = []
        for u1, u2 in zip(values_in_1, values_in_2):
            z1 = self.μ + self.σ * sqrt(-2 * log(1 - u1)) * cos(2 * pi * u2)
            z2 = self.μ + self.σ * sqrt(-2 * log(1 - u2)) * cos(2 * pi * u1)

            values_out.append(z1)
            values_out.append(z2)

        return values_out
