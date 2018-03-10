from task_2.distributions import *


class DistBI(Dist):
    NAME = 'Биномиальное распределение'

    def __init__(self, params):
        # параметры

        # ассерты

        super().__init__()

    def transform(self, values):
        values_standard = Dist.transform_standard(values)
        return []