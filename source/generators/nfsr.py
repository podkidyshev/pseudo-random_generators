from generators import *
from generators.lfsr import LFSR


class GenNFSR(Gen):
    NAME = 'Нелинейная комбинация РСЛОС'
    PARAMS = ['p1', 'a1', 'p2', 'a2', 'p3', 'a3', 'w']

    def __init__(self, params):
        # ассерты
        Gen.assert_len(params.i, 3, GenNFSR.NAME)
        # основные параметры
        self.lfsr = []
        for _idx in range(3):
            self.lfsr.append(LFSR(params, _idx + 1))
        self.w = Gen.get(params, 'w', Gen.default, DEFAULT_W, 'w')
        # ассерты
        assert self.w > 0, 'Длина выходного слова должна быть > 0'

        super().__init__()

    def __next__(self):
        res = ''
        for _idx in range(self.w):
            x1, x2, x3 = (next(lfsr) for lfsr in self.lfsr)
            new_bit = (x1 * x2) ^ (x2 * x3) ^ x3
            res += str(new_bit)
        return int(res, 2)

    @staticmethod
    def usage():
        usage = """
Используются 3 параллельных генератора РСЛОС (generators.lfsr.LFSR)
w - длина выходного слова > 0    
p[1-3] - длина регистра в битах - >0
a[1-3] - полином над GF(2) степени p[1-3]-1
От введенного полинома а[1-3] будут использованы первые p[1-3] битов

Инициализационный вектор:
i[1-3] - начальное состояние регистра 1-3 (полином над GF(2))
От введенного состояния i[1-3] будут использованы первые p[1-3] битов
"""
        print(usage)
