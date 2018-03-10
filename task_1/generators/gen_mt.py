from task_1.generators import *


class GenMT(Gen):
    NAME = 'Вихрь Мерсенна'
    PARAMS = []

    p = 624
    w = 32
    r = 31
    q = 397
    a = 2567483615
    u = 11
    s = 7
    t = 15
    l = 18
    b = 2636928640
    c = 4022730752
    f = 1812433253

    def __init__(self, params):
        self.mask_all = (2 ** GenMT.w) - 1
        self.mask_last = 2 ** GenMT.r
        self.mask_first = (2 ** GenMT.r) - 1
        # ассерты
        Gen.assert_i_len(params.i, 1, GenMT.NAME)
        # инициализационный вектор
        self.seed = Gen.extract_param_vec(params, 0, Gen.gen_param, (0, (2 ** GenMT.w) - 1), 'seed') & self.mask_all

        self.a = [0] * GenMT.p
        self.a[0] = self.seed
        for i in range(1, GenMT.p):
            self.a[i] = ((GenMT.f * self.a[i - 1]) ^ ((self.a[i - 1] >> (GenMT.w - 2)) + i)) & self.mask_all
        # индекс периода
        self.n = 0

        super().__init__()

    def gen_new_a(self):
        for i in range(GenMT.p):
            y = (self.a[i] & self.mask_last) + (self.a[(i + 1) % GenMT.p] & self.mask_first)
            self.a[i] = self.a[(i + GenMT.q) % GenMT.p] ^ (y >> 1)
            if y % 2:
                self.a[i] ^= GenMT.b

    def __next__(self):
        if self.n == 0:
            self.gen_new_a()

        y = self.a[self.n]
        y ^= y >> GenMT.u
        y ^= (y << GenMT.s) & GenMT.b
        y ^= (y << GenMT.t) & GenMT.c
        y ^= y >> GenMT.l

        self.n = (self.n + 1) % GenMT.p
        return y

    @staticmethod
    def usage():
        usage = """
Инициализационный вектор:

seed - начальное состояние генератора (полином над GF2)
От введенного состояния seed будут использованы первые 32 бита
"""
        print(usage)
