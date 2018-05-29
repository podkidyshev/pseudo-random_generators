import argparse

import utils
import gen
import dist

DEFAULT_SAMPLE_SIZE = 10000
DEFAULT_DISTRIBUTION = 'gm'
DEFAULT_GENERATOR = 'nfsr'
MT_KEY_BACKUP = 1334820826
MT_KEY = 133482082634567


def parse_args():
    args = utils.get_args()
    # Добавление аргументов
    parser = argparse.ArgumentParser()
    gen.DEFAULT_LEN = DEFAULT_SAMPLE_SIZE
    gen.init_args(parser, args)
    # Парсинг
    args_parsed = parser.parse_args(args)
    utils.handle_bins(args_parsed)
    # Стандартное равномерное распределение
    args_parsed.d = 'st'
    args_parsed.p1 = 0
    args_parsed.p2 = 1
    return args_parsed


def main():
    # Аргументы
    args = parse_args()
    # Генерация ПРС и приведение к стандартному равномерному распределению
    prs = gen.generate(args)
    prs_st, prs_ideal = dist.transform(args, prs)

    import criteria.chi2 as chi2
    import criteria.series as series
    import criteria.intervals as intervals
    import criteria.splitting as splitting
    # chi2.chi2(prs_st)
    #series.series(prs_st)
    #intervals.intervals(prs_st)
    splitting.splitting(prs_st)


if __name__ == '__main__':
    main()
