from functools import reduce


def conflicts(prs):
    # Взято из Кнута. Глава 3.3.2
    # Длина тестируемой последовательности должна быть 2 ** 14 = 16384
    # Числа должны быть размера 2 ** 20 = 1048576
    print('INFO: КРИТЕРИЙ конфликтов\n')
    conflicts_count = {}
    for v in prs:
        v_new = int(v * 1000000)
        conflicts_count[v_new] = conflicts_count[v_new] + 1 if v in conflicts_count else 0
    res = reduce(int.__add__, conflicts_count.values())

    conflicts_crit = 60
    print('Критическое число конфликтов равно {}. Число конфликтов в выборке: {}'
          .format(conflicts_crit, res))
    if res <= conflicts_crit:
        print('{0} <= критического {1}. ППСЧ случайна'.format(res, conflicts_crit))
    else:
        print('Критическое {1} < {0}. ППСЧ не случайна'.format(res, conflicts_crit))
