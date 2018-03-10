from distributions import *


class DistGM(Dist):
    NAME = 'Гамма-распределение'

    def __init__(self, params):
        super().__init__()

    def transform(self, values):
        values_standard = Dist.transform_standard(values)
        return []
