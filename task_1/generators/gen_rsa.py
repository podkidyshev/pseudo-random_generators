from sympy.ntheory import factorint, isprime
from math import gcd

from task_1.generators import *


class GenRSA(Gen):
    """/rsa_n:61849 /rsa_e:929"""
    NAME = 'RSA'
    PARAMS = ['p', 'q', 'rsa_e', 'rsa_n', 'w']

    def __init__(self, params):
        # ассерты
        Gen.assert_i_len(params.i, 1, GenRSA.NAME)
        # основные параметры
        self.p = Gen.extract_param(params, 'p', GenRSA.gen_prime, 'p', GenRSA.big)
        self.q = Gen.extract_param(params, 'q', GenRSA.gen_prime, 'q', GenRSA.small)
        self.n = Gen.extract_param(params, 'rsa_n', self.gen_n)
        self.e = Gen.extract_param(params, 'rsa_e', self.gen_e)
        self.w = Gen.extract_param(params, 'w', Gen.gen_param, DEFAULT_W, 'w')
        # ассерты
        assert 1 <= self.w, 'ограничение 1 <= w'
        assert isprime(self.p), 'p должно быть простым положительным числом'
        assert isprime(self.q), 'q должно быть простым положительным числом'
        self.p, self.q = GenRSA.assert_n(self.n)
        GenRSA.assert_e(self.p, self.q, self.e)
        # инициализационный вектор
        self.x0 = Gen.extract_param_vec(params, 0, Gen.gen_param, (1, self.n - 1), 'x0') % self.n

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
        assert isprime(factors[0]) and isprime(factors[1]), 'множители n должны быть простыми: {} и {}'.format(*factors)
        return factors[0], factors[1]

    @staticmethod
    def assert_e(p, q, e):
        assert e < (p - 1) * (q - 1), 'e должно быть строго меньше (p - 1)(q - 1)'
        assert gcd(e, (p - 1) * (q - 1)) == 1, 'e и (p - 1)(q - 1) должны быть взаимно простыми'

    @staticmethod
    def gen_prime(name, primes):
        prime = random.choice(primes)
        Gen.print_genned_param(name, prime)
        return prime

    @staticmethod
    def gen_relatively_prime(f, name):
        res = GenRSA._gen_relatively_prime(f)
        Gen.print_genned_param(name, res)
        return res

    @staticmethod
    def _gen_relatively_prime(f):
        factors = set(factorint(f).keys())
        possible_factors = [factor for factor in GenRSA.big + GenRSA.small if factor < f and f not in factors]
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

    big = [104933, 15486671, 15490781, 15495749, 179426549, 552301, 94244707, 11303401, 238471, 80713, 53993,
           103591, 15401, 389171, 152879, 225949, 6528793, 1377653, 11240783, 9833647, 11241023, 939823]

    @staticmethod
    def usage():
        usage = """
p и q - простые числа
w - длина генерируемых бинарных слов - целое положительное число
rsa_n - произведение двух простых чисел
rsa_e - взаимно простое число с (p - 1)(q - 1), где rsa_n = p * q

Инициализационный вектор:

x0 - начальное состояние
x0 будет автоматически взят по модулю rsa_n
"""
        print(usage)
