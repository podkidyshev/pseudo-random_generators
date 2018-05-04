from generators import *
from generators.gen_lfsr import LFSR


class Gen5p(Gen):
    NAME = 'Пятипараметрический метод'
    PARAMS = ['p', 'q1', 'q2', 'q3']

    def __init__(self, params):
        # ассерты
        Gen.assert_i_len(params.i, 1, Gen5p.NAME)
        # основные параметры
        self.p = Gen.extract_param(params, 'p', Gen.gen_param, DEFAULT_P, 'p')
        bounds = (0, self.p - 1)
        self.q1 = Gen.extract_param(params, 'q1', Gen.gen_param, bounds, 'q1')
        self.q2 = Gen.extract_param(params, 'q2', Gen.gen_param, bounds, 'q2')
        self.q3 = Gen.extract_param(params, 'q3', Gen.gen_param, bounds, 'q3')

        assert 0 <= self.q1 < self.p, 'параметры q(i) должны удовлетворять 0 <= q(i) < p'
        assert 0 <= self.q2 < self.p, 'параметры q(i) должны удовлетворять 0 <= q(i) < p'
        assert 0 <= self.q3 < self.p, 'параметры q(i) должны удовлетворять 0 <= q(i) < p'
        # инициализационный вектор
        mask = 2 ** self.p - 1
        self.seed = Gen.extract_param_vec(params, 0, Gen.gen_param, (0, mask), 'seed') & mask

        self.a = (1 << self.q1) | (1 << self.q2) | (1 << self.q3)
        self.lfsr = LFSR(LFSR.DummyParams(self.p, self.a, self.seed))

        super().__init__()

    def __next__(self):
        return self.lfsr.gen_word(self.lfsr.p)

    @staticmethod
    def usage():
        usage = """
p - длина регистра в битах
0 <= q1, q2, q3 < p - единичные биты для полинома a в РСЛОС

Инициализационный вектор:

seed - начальное состояние
От введенного состояния seed будут использованы первые p-1 битов
"""
        print(usage)
