from sympy.ntheory import factorint, isprime
from math import gcd

from generators import *


class GenRSA(Gen):
    NAME = 'RSA'
    PARAMS = ['p', 'q', 'rsa_e', 'rsa_n', 'w']

    def __init__(self, params):
        # ассерты
        Gen.assert_len(params.i, 1, GenRSA.NAME)
        # основные параметры
        self.p = Gen.get(params, 'p', GenRSA.gen_prime, 'p')
        self.q = Gen.get(params, 'q', GenRSA.gen_prime, 'q')
        self.n = Gen.get(params, 'rsa_n', self.gen_n)
        self.e = Gen.get(params, 'rsa_e', self.gen_e)
        self.w = Gen.get(params, 'w', Gen.default, DEFAULT_W, 'w')
        # ассерты
        assert 1 <= self.w, 'Длина выходного слова должна быть 0 < w'
        assert self.p > 0 and isprime(self.p), 'p должно быть простым положительным числом'
        assert self.q > 0 and isprime(self.q), 'q должно быть простым положительным числом'
        self.p, self.q = GenRSA.assert_n(self.n)
        GenRSA.assert_e(self.p, self.q, self.e)
        # инициализационный вектор
        self.x0 = Gen.getv(params, 0, Gen.gen_param, (1, self.n - 1), 'x0') % self.n

        super().__init__()

    def __next__(self):
        res = 0
        for _idx in range(self.w):
            self.x0 = pow(self.x0, self.e, self.n)
            res <<= 1
            res += self.x0 & 1
        return res

    def gen_n(self):
        Gen.print_genned_param('rsa_n', self.p * self.q)
        return self.p * self.q

    def gen_e(self):
        e = GenRSA._gen_relatively_prime((self.p - 1) * (self.q - 1))
        Gen.print_genned_param('rsa_e', e)
        return e

    @staticmethod
    def assert_n(n):
        factors = tuple(factorint(n).keys())
        assert len(factors) == 2, 'rsa_n должно быть произведением двух простых чисел'
        return factors

    @staticmethod
    def assert_e(p, q, e):
        assert e < (p - 1) * (q - 1), 'rsa_e должно быть строго меньше (p - 1)(q - 1)'
        assert gcd(e, (p - 1) * (q - 1)) == 1, 'rsa_e и (p - 1)(q - 1) должны быть взаимно простыми'

    @staticmethod
    def gen_prime(name):
        value = random.choice(GenRSA.primes)
        Gen.print_genned_param(name, value)
        return value

    @staticmethod
    def gen_relatively_prime(f, name):
        res = GenRSA._gen_relatively_prime(f)
        Gen.print_genned_param(name, res)
        return res

    @staticmethod
    def _gen_relatively_prime(f):
        factors = set(factorint(f).keys())
        possible_factors = [factor for factor in GenRSA.primes if factor < f and factor not in factors]
        if not possible_factors:
            return f - 1

        e = 1
        while e < f:
            next_prime = random.choice(possible_factors)
            if next_prime * e > f:
                break
            e *= next_prime
        return e

    primes = [104933, 15486671, 15490781, 15495749, 179426549, 552301, 94244707, 11303401, 238471, 80713, 53993,
              103591, 15401, 389171, 152879, 225949, 6528793, 1377653, 11240783, 9833647, 11241023, 939823]

    @staticmethod
    def usage():
        usage = """
p и q - простые положительные числа
w - длина генерируемых двоичных слов > 0
rsa_n - произведение двух простых чисел
rsa_e - взаимно простое с и меньше (p - 1)(q - 1), где rsa_n = p * q

Инициализационный вектор:
i[0] - начальное состояние, будет автоматически взят по модулю rsa_n
"""
        print(usage)
