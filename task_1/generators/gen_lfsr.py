from task_1.generators import *


class GenLFSR(Gen):
    NAME = 'Регистр сдвига с обратной связью (РСЛОС)'
    PARAMS = ['p', 'a', 'w']

    def __init__(self, params):
        # ассерты
        Gen.assert_i_len(params.i, 1, GenLFSR.NAME)
        # параметры
        self.lfsr = LFSR(params)
        self.w = Gen.extract_param(params, 'w', Gen.gen_param, DEFAULT_W, 'w')
        assert self.w > 0, 'длина выходного слова должна быть целым положительным числом'

        super().__init__()

    def __next__(self):
        return self.lfsr.gen_word(self.w)

    @staticmethod
    def usage():
        usage = """
w - длина выходного слова - > 0
p - длина регистра в битах - > 0
a - полином над GF(2) степени p-1
От введенного полинома а будут использованы первые p-1 битов

Инициализационный вектор:

x - начальное состояние регистра (полином над GF(2))
От введенного состояния х будут использованы первые p-1 битов
"""
        print(usage)


class LFSR:
    def __init__(self, params, idx=None):
        idx = idx if idx is not None else ''

        p_name = 'p{}'.format(idx)
        a_name = 'a{}'.format(idx)
        x_name = 'x{}'.format(idx)

        self.p = Gen.extract_param(params, p_name, Gen.gen_param, DEFAULT_P, p_name)
        assert self.p > 0, 'длина регистра должна быть целым положительным числом'
        self.a = Gen.extract_param(params, a_name, self.choose_poly) & (2 ** self.p) - 1
        self.x = Gen.extract_param_vec(params, 0, Gen.gen_param, (1, 2 ** self.p - 1), x_name) & (2 ** self.p) - 1

    def __next__(self):
        out_bit = self.x & 1
        new_bit = bin(self.x & self.a).count('1') & 1
        self.x >>= 1
        self.x |= new_bit << (self.p - 1)
        return out_bit

    def choose_poly(self):
        if self.p <= len(LFSR.polynomials):
            a = LFSR.polynomials[self.p - 1]
            print('Выбран полином a = {}'.format(a))
        else:
            a = Gen.gen_param((0, (2 ** self.p) - 1), 'a')
        return a

    def gen_word(self, w):
        res = 0
        for _idx in range(w):
            res <<= 1
            res += next(self)
        return res

    polynomials = [0, 3, 7, 13, 25, 41, 97, 193, 369, 545, 1153, 2561, 7185, 14593, 28677, 49153,
                   106513, 147457, 264193, 933889, 1179649, 2621441, 6291457, 8650753, 29491201]

    # Костыль 3
    class DummyParams:
        def __init__(self, p, a, seed):
            self.p = p
            self.a = a
            self.i = [seed]
