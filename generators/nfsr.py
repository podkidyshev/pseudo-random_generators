from generators import *
from generators.lfsr import LFSR


class GenNFSR(Gen):
    NAME = 'Нелинейная комбинация РСЛОС'
    PARAMS = ['g_p1', 'a1', 'g_p2', 'a2', 'g_p3', 'a3', 'w']

    def __init__(self, params):
        # ассерты
        Gen.assert_i_len(params.i, 3, GenNFSR.NAME)
        self.lfsr = []
        for _idx in range(3):
            self.lfsr.append(LFSR(params, _idx + 1))
        self.w = Gen.extract(params, 'w', Gen.gen_param, DEFAULT_W, 'w')
        assert self.w > 0, 'длина выходного слова должна быть целым положительным числом'

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
Используются 3 параллельных генератора РСЛОС (lfsr)

w - размер в битах генерируемых слов    
    
pi - длина регистра в битах - >0
ai - полином над GF(2) степени pi-1
От введенного полинома аi будут использованы первые pi-1 битов

Инициализационный вектор:

xi - начальное состояние регистра i (полином над GF(2))
От введенного состояния хi будут использованы первые pi-1 битов
"""
        print(usage)
