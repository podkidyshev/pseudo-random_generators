from sympy.ntheory import factorint, isprime
from fractions import gcd

from generators import *


class GenBBS(Gen):
    NAME = 'Алгоритм Блюма-Блюма-Шуба'
    PARAMS = ['p', 'q', 'bbs_n', 'bbs_x', 'w']

    def __init__(self, params):
        # ассерты
        Gen.assert_i_len(params.i, 0, GenBBS.NAME)
        # основные параметры
        self.p = Gen.extract_param(params, 'p', GenBBS.gen_blum_factor, 'p', GenBBS.big)
        self.q = Gen.extract_param(params, 'q', GenBBS.gen_blum_factor, 'q', GenBBS.small)
        self.n = Gen.extract_param(params, 'bbs_n', lambda: self.p * self.q)
        self.x = Gen.extract_param(params, 'bbs_x', GenBBS.gen_relatively_prime, self.n, 'x')
        self.w = Gen.extract_param(params, 'w', Gen.gen_param, DEFAULT_W, 'w')
        # ассерты
        assert 1 <= self.w, 'ограничение 1 <= w'
        assert isprime(self.p) and self.p % 4 == 3, 'p не простое или % 3 != 4'
        assert isprime(self.q) and self.q % 4 == 3, 'q не простое или % 3 != 4'
        if params.bbs_n or params.bbs_x: assert GenBBS.check_n(self.n) and gcd(self.n, self.x) == 1, \
            'bbs_n и bbs_x должны быть взаимно простыми'
        # инициализационный вектор
        self.x0 = pow(self.x, 2, self.n)

        super().__init__()

    def __next__(self):
        res = 0
        for _idx in range(self.w):
            self.x0 = pow(self.x0, 2, self.n)
            res <<= 1
            res += self.x0 & 1
        return res

    @staticmethod
    def gen_blum_factor(name, blums):
        res = random.choice(blums)
        Gen.print_genned_param(name, res)
        return res

    @staticmethod
    def check_n(n):
        factors = tuple(factorint(n).keys())
        assert len(factors) == 2, 'rsa_n должно быть произведением двух простых чисел'
        assert isprime(factors[0]) and isprime(factors[1]), 'множители n должны быть простыми: {} и {}'.format(*factors)
        assert factors[0] % 4 == 3 and factors[1] % 4 == 3, 'один из сомножителей bbs_n - не число Блюма'
        return factors[0], factors[1]

    @staticmethod
    def gen_relatively_prime(f, name):
        res = GenBBS._gen_relatively_prime(f)
        Gen.print_genned_param(name, res)
        return res

    @staticmethod
    def _gen_relatively_prime(f):
        factors = set(factorint(f).keys())
        possible_factors = [factor for factor in GenBBS.big + GenBBS.small if factor < f and f not in factors]
        if not possible_factors:
            return f - 1

        e = 1

        while e < f:
            next_prime = random.choice(possible_factors)
            if next_prime * e > f:
                break
            e *= next_prime
        return e

    small = [3, 7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83, 103, 107, 127, 131, 139, 151, 163, 167, 179, 191, 199,
             211, 223, 227, 239, 251, 263, 271, 283, 307, 311, 331, 347, 359, 367, 379, 383, 419, 431, 439, 443, 463,
             467, 479, 487, 491, 499, 503, 523, 547, 563, 571, 587, 599, 607, 619, 631, 643, 647, 659, 683, 691, 719,
             727, 739, 743, 751, 787, 811, 823, 827, 839, 859, 863, 883, 887, 907, 911, 919, 947, 967, 971, 983, 991]

    big = [15486671, 94244707, 238471, 103591, 389171, 152879, 11240783, 9833647, 11241023, 939823]

    @staticmethod
    def usage():
        usage = """
w - длина выходного слова - > 0
p и q - простые числа % 3 == 4
bbs_n - число Блюма
bbs_x - число, взаимно-простое с bbs_n
"""
        print(usage)
