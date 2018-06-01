from generators import *
from generators.lfsr import LFSR


class Gen5p(Gen):
    NAME = 'Пятипараметрический метод'
    PARAMS = ['p', 'q1', 'q2', 'q3', 'w']

    def __init__(self, params):
        # ассерты
        Gen.assert_len(params.i, 1, Gen5p.NAME)
        # основные параметры
        self.p = Gen.get(params, 'p', Gen.gen_param, DEFAULT_P, 'p')
        bounds = (0, self.p - 1)
        self.q1 = Gen.get(params, 'q1', Gen.gen_param, bounds, 'q1')
        self.q2 = Gen.get(params, 'q2', Gen.gen_param, bounds, 'q2')
        self.q3 = Gen.get(params, 'q3', Gen.gen_param, bounds, 'q3')
        self.w = Gen.get(params, 'w', Gen.default, DEFAULT_W, 'w')
        # ассерты
        assert 0 <= self.q1 < self.p, 'Параметр q[1] не удовлетворяет 0 <= q[1-3] < p'
        assert 0 <= self.q2 < self.p, 'Параметр q[2] не удовлетворяет 0 <= q[1-3] < p'
        assert 0 <= self.q3 < self.p, 'Параметр q[3] не удовлетворяет 0 <= q[1-3] < p'
        assert self.w > 0, 'Длина выходного слова должна быть > 0'
        # инициализационный вектор
        mask = 2 ** self.p - 1
        self.seed = Gen.getv(params, 0, Gen.gen_param, (0, mask), 'seed') & mask

        self.a = (1 << self.q1) | (1 << self.q2) | (1 << self.q3)
        self.lfsr = LFSR(LFSR.DummyParams(self.p, self.a, self.seed))

        super().__init__()

    def __next__(self):
        return self.lfsr.gen_word(self.w)

    @staticmethod
    def usage():
        usage = """
w - длина выходного слова > 0  
p - длина регистра в битах
0 <= q1, q2, q3 < p - единичные биты для полинома a в РСЛОС

Инициализационный вектор:
i[0] - начальное состояние
От введенного состояния i[0] будут использованы первые p битов
"""
        print(usage)
