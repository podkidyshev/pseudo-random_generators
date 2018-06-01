from functools import reduce
from itertools import combinations_with_replacement
from sympy.ntheory import factorint
from math import gcd

from generators import *


class GenBBS(Gen):
    NAME = 'Алгоритм Блюма-Блюма-Шуба'
    PARAMS = ['p', 'q', 'bbs_n', 'w']

    def __init__(self, params):
        # ассерты
        Gen.assert_len(params.i, 1, GenBBS.NAME)
        # основные параметры
        self.p = Gen.get(params, 'p', GenBBS.gen_blum_factor, 'p', GenBBS.primes)
        self.q = Gen.get(params, 'q', GenBBS.gen_blum_factor, 'q', GenBBS.primes)
        self.n = Gen.get(params, 'bbs_n', lambda: self.p * self.q)
        self.w = Gen.get(params, 'w', Gen.default, DEFAULT_W, 'w')
        # ассерты
        assert 1 <= self.w, 'Длина выходного слова должна быть > 0'
        assert self.p % 4 == 3, 'p % 3 == 4'
        assert self.q % 4 == 3, 'q % 3 == 4'
        GenBBS.check(self.n)
        # инициализационный вектор
        self.x = Gen.getv(params, 0, GenBBS.gen_relatively_prime, self.n, 'x')
        assert gcd(self.n, self.x) == 1, 'bbs_n = {} и i[0] = {} должны быть взаимно простыми'.format(self.n, self.x)
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
    def check(blum):
        factors = list(factorint(blum).keys())
        assert len(factors) == 2, 'Число bbs_n должно быть произведением двух простых чисел % 4 == 3'
        assert factors[0] % 4 == 3, 'Число bbs_n должно быть произведением двух простых чисел % 4 == 3'
        assert factors[1] % 4 == 3, 'Число bbs_n должно быть произведением двух простых чисел % 4 == 3'

    @staticmethod
    def gen_relatively_prime(f, name):
        factors = set(factorint(f).keys())
        possible_factors = [factor for factor in GenBBS.primes if factor not in factors]

        x = 1
        for idx in range(2):
            x *= random.choice(possible_factors)

        Gen.print_genned_param(name, x)
        return x

    # простые числа, сравнимые с 3 по модулю 4
    primes = [859, 863, 883, 887, 907, 911, 919, 947, 967, 971, 983, 991, 15486671,
              94244707, 238471, 103591, 389171, 152879, 11240783, 9833647, 11241023, 939823]

    @staticmethod
    def usage():
        usage = """
w - длина выходного слова > 0
p и q - целые числа % 4 == 3
bbs_n - число Блюма - будет использовано, даже если переданы p и q

Инициализационный вектор:
i[0] - число, взаимно-простое с bbs_n=p*q
"""
        print(usage)
