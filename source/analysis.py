import argparse

import utils
import utils.launch_dist as launch_dist
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
    args = parse_args()
    # Генерация ПСП и приведение к стандартному равномерному распределению
    prs = launch_dist.handle_file_dist_in(args)
    prs_st, prs_ideal = dist.transform(args, prs)

    old_separator = utils.SEPARATOR
    utils.SEPARATOR = old_separator + '\n' + old_separator

    import criteria.chi2 as chi2
    import criteria.serial as serial
    import criteria.intervals as intervals
    import criteria.splitting as splitting
    import criteria.permutations as permutations
    import criteria.run as run
    import criteria.conflicts as conflicts

    criterias = [
        chi2.chi2, serial.serial, intervals.intervals, splitting.splitting,
        permutations.permutations, run.run_1, run.run_2, conflicts.conflicts
    ]

    for crit in criterias:
        crit(prs_st if crit != conflicts.conflicts else prs)  # критерий конфликтов запустим на исходной ПСП
        print(utils.SEPARATOR)

    utils.SEPARATOR = old_separator


if __name__ == '__main__':
    main()
