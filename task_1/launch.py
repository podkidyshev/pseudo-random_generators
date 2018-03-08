import random
import argparse

import generators
from generators.lc import GenLC
from generators.add import GenAdd
from generators.p5 import Gen5p
from generators.lfsr import GenLFSR
from generators.nfsr import GenNFSR
from generators.mt import GenMT
from generators.rc4 import GenRC4
from generators.rsa import GenRSA
from generators.bbs import GenBBS

GENS_DICT = {'lc': GenLC, 'add': GenAdd, '5p': Gen5p, 'lfsr': GenLFSR, 'nfsr': GenNFSR,
             'mt': GenMT, 'rc4': GenRC4, 'rsa': GenRSA, 'bbs': GenBBS
             }


def rand_gen():
    gen_name = random.choice(list(GENS_DICT.keys()))
    print('Случайно выбран генератор {}'.format(gen_name) + generators.SEPARATOR)
    return gen_name


def init_parser(parser: argparse.ArgumentParser, gen_name: str):
    params = GENS_DICT[gen_name].PARAMS

    for param_name in params:
        parser.add_argument('--{}'.format(param_name), type=int)
