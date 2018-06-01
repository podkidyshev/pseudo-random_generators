from generators import *


class GenLFSR(Gen):
    NAME = 'Регистр сдвига с обратной связью (РСЛОС)'
    PARAMS = ['p', 'a', 'w']

    def __init__(self, params):
        # ассерты
        Gen.assert_len(params.i, 1, GenLFSR.NAME)
        # параметры
        self.lfsr = LFSR(params)
        self.w = Gen.get(params, 'w', Gen.default, DEFAULT_W, 'w')
        # ассерты
        assert self.w > 0, 'Длина выходного слова должна быть > 0'

        super().__init__()

    def __next__(self):
        return self.lfsr.gen_word(self.w)

    @staticmethod
    def usage():
        usage = """
w - длина выходного слова > 0
p - длина регистра в битах > 0
a - полином над GF(2) степени p-1
От введенного полинома а будут использованы первые p битов

Инициализационный вектор:
i[0] - начальное состояние регистра (полином над GF(2))
От введенного состояния i[0] будут использованы первые p битов
"""
        print(usage)


class LFSR:
    def __init__(self, params, idx=None):
        idx = idx if idx is not None else ''

        p_name = 'p{}'.format(idx)
        a_name = 'a{}'.format(idx)
        x_name = 'x{}'.format(idx)

        self.p = Gen.get(params, p_name, Gen.gen_param, DEFAULT_P, p_name)
        assert self.p > 0, 'Длина регистра должна быть целым положительным числом'
        self.a = Gen.get(params, a_name, self.choose_poly) & (2 ** self.p - 1)
        self.x = Gen.getv(params, 0, Gen.gen_param, (1, 2 ** self.p - 1), x_name) & (2 ** self.p - 1)

    def __next__(self):
        out_bit = self.x & 1                            # первый бит регистра
        new_bit = bin(self.x & self.a).count('1') & 1   # умножаем полином на регистр, посчитываем число единиц mod 2
        self.x >>= 1                                    # сдвигаем регистр (удаляем первый бит)
        self.x |= new_bit << (self.p - 1)               # в конец регистра записываем новый бит
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

    polynomials = ['полином нулевой степени не определён',
                   3, 7, 13, 25, 41, 97, 193, 369, 545, 1153, 2561, 7185, 14593, 28677, 49153,
                   106513, 147457, 264193, 933889, 1179649, 2621441, 6291457, 8650753, 29491201]

    # Костыль
    class DummyParams:
        def __init__(self, p, a, seed):
            self.g_p = p
            self.a = a
            self.i = [seed]
