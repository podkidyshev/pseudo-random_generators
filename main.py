import launch
import argparse

SAMPLE_SIZE_DEFAULT = 10000
GENERATOR_DEFAULT = 'rc4'
RC4_KEY = 923213721


def parse_args():
    # Костыль 1
    args = launch.get_args()

    parser = argparse.ArgumentParser()
    parser.add_argument('--d', default='nr')
    parser.add_argument('--p1', type=float)
    parser.add_argument('--p2', type=float)
    parser.add_argument('--p3', type=float)
    parser.add_argument('--n', type=int, default=SAMPLE_SIZE_DEFAULT)

    return parser.parse_args(args)


def generate_prs(args):
    args.i = [RC4_KEY]
    generator = launch.GENS_DICT[GENERATOR_DEFAULT](args)
    prs = [next(generator) for _idx in range(args.n)]
    distribution = launch.DISTS_DICT[args.d](args)
    prs_dist, prs_ideal = distribution.transform(prs)
    return prs_dist, distribution


def main():
    # Аргументы
    args = parse_args()
    prs, distribution = generate_prs(args)

    import criteria.xi2
    cr = criteria.xi2.Xi2(args)
    cr.check(prs, distribution)


if __name__ == '__main__':
    main()
