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

    print(compute_probabilities(2**9, 2**6))

    print('При уровне значимости {} критическое число конфликтов равно {}. Число конфликтов в выборке: {}'
          .format(alpha, conflicts_crit, res))
    if res <= conflicts_crit:
        print('{0} <= критического {1}. ППСЧ случайна'.format(res, conflicts_crit))
    else:
        print('Критическое {1} < {0}. ППСЧ не случайна'.format(res, conflicts_crit))


def compute_probabilities(m, n):
    a = [0 for _idx in range(n + 1)]
    a[1] = 1
    j0, j1 = 1, 1
    for _k in range(n - 1):
        j1 += 1
        j = j1
        lel = j0
        while j >= lel:
            a[j] = (j / m) * a[j] + ((1 + 1 / m) - (j / m)) * a[j - 1]
            if a[j] < 0.00001:
                a[j] = 0
                if j == j1:
                    j1 -= 1
                elif j == j0:
                    j0 += 1
            j -= 1

    tlist = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1]
    res = []
    p = 0
    j = j0 - 1
    t = 0
    while t != len(tlist) - 1:
        j += 1
        p += a[j]
        if p > tlist[t]:
            res.append((n - j - 1, 1 - p))
        while p <= tlist[t] and t < len(tlist) - 1:
            t += 1

    return res
