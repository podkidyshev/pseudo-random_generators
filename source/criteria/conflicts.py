from functools import reduce


def conflicts(prs):
    # Взято из Кнута. Глава 3.3.2
    # Длина тестируемой последовательности должна быть 2 ** 14 = 16384
    # Числа должны быть размера 2 ** 20 = 1048576
    print('INFO: КРИТЕРИЙ конфликтов\n')
    conflicts_count = {}
    for v in prs:
        conflicts_count[v] = 1 if v in conflicts_count else 0
    res = reduce(int.__add__, conflicts_count.values())

    alpha = 0.946
    conflicts_crit = 145

    print('При уровне значимости {} критическое число конфликтов равно {}. Число конфликтов в выборке: {}'
          .format(alpha, conflicts_crit, res))
    if res <= conflicts_crit:
        print('{0} <= критического {1}. ППСЧ случайна'.format(res, conflicts_crit))
    else:
        print('Критическое {1} < {0}. ППСЧ не случайна'.format(res, conflicts_crit))
