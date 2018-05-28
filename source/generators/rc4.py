from generators import *


class GenRC4(Gen):
    NAME = 'RC4'
    PARAMS = []

    def __init__(self, params):
        # ассерты
        Gen.assert_i_len(params.i, 1, GenRC4.NAME)
        # основные параметры
        # инициализационный вектор
        mask = (2 ** 256) - 1
        self.key = Gen.extract_param_vec(params, 0, Gen.gen_param, (0, mask), 'key') & mask

        self.S = [idx for idx in range(256)]

        j = 0
        for i in range(256):
            j = (j + self.S[i] + GenRC4.get_byte(self.key, i)) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]

        self.i = 0
        self.j = 0

        super().__init__()

    def __next__(self):
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.S[self.i]) % 256
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
        return (self.S[self.i] + self.S[self.j]) % 256

    @staticmethod
    def get_byte(a, i):
        return (a >> (i * 8)) & (2 ** 8 - 1)

    @staticmethod
    def usage():
        usage = """
Инициализационный вектор:
key - ключ шифрования, будут использованы первые 256 битов
"""
        print(usage)
