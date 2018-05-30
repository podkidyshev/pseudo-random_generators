import argparse

import utils
import utils.launch_dist as launch_dist
import gen
import dist


def parse_args():
    args = utils.get_args()
    # Добавление аргументов
    parser = argparse.ArgumentParser()
    parser.add_argument('--f', help='Файл с входной ПСП')
    # Парсинг
    args_parsed = parser.parse_args(args)
    # Стандартное равномерное распределение
    args_parsed.d = 'st'
    args_parsed.p1 = 0
    args_parsed.p2 = 1
    return args_parsed


def main():
    # Аргументы
    args = parse_args()
    # Генерация ПРС и приведение к стандартному равномерному распределению
    prs = launch_dist.handle_file_dist_in(args)
    prs_st, prs_ideal = dist.transform(args, prs)

    import criteria.chi2 as chi2
    import criteria.series as series
    import criteria.intervals as intervals
    import criteria.splitting as splitting
    #import criteria.permutations as permutations
    import criteria.run as run
    import criteria.conflicts as conflicts
    # chi2.chi2(prs_st)
    #series.series(prs_st)
    #intervals.intervals(prs_st)
    #splitting.splitting(prs_st)
    #permutations.permutations(prs_st)
    #run.run_2(prs_st)
    conflicts.conflicts(prs)


if __name__ == '__main__':
    main()
