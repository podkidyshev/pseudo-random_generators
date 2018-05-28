import launch
import argparse

DEFAULT_SAMPLE_SIZE = 10000
DEFAULT_DISTRIBUTION = 'gm'
DEFAULT_GENERATOR = 'nfsr'
MT_KEY_BACKUP = 1334820826
MT_KEY = 133482082634567


def parse_args():
    # Костыль 1
    args = launch.get_args()

    parser = argparse.ArgumentParser()
    # распределение
    parser.add_argument('--d', default=DEFAULT_DISTRIBUTION)
    parser.add_argument('--p1', type=float)
    parser.add_argument('--p2', type=float)
    parser.add_argument('--p3', type=float)
    parser.add_argument('--n', type=int, default=DEFAULT_SAMPLE_SIZE)
    # генерация
    parser.add_argument('--i', nargs='*', default=None)
    launch.init_gen_parser(parser, DEFAULT_GENERATOR)

    return parser.parse_args(args)


def generate_prs(args):
    # args.i = [MT_KEY_BACKUP]
    generator = launch.GENS_DICT[DEFAULT_GENERATOR](args)
    prs = [next(generator) for _idx in range(args.n)]
    distribution = launch.DISTS_DICT[args.d](args)
    prs_dist, prs_ideal = distribution.transform(prs)
    return prs_dist, distribution


def main():
    # Аргументы
    args = parse_args()
    prs, distribution = generate_prs(args)

    import criteria.xi2
    import criteria.series
    # cr = criteria.xi2.Xi2(args)
    cr = criteria.series.Series(args)
    cr.check(prs, distribution)


if __name__ == '__main__':
    main()
