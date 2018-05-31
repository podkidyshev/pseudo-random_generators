import criteria.chi2 as chi2
import distributions as dist

A = [
    [4529.4, 9044.9, 13568, 22615,  22615,  27892],
    [9044.9, 18097,  27139, 36187,  45234,  55789],
    [13568,  27139,  40721, 54281,  67582,  83685],
    [18091,  36187,  54281, 72414,  90470,  111580],
    [22615,  45234,  67852, 90470,  113262, 139476],
    [27892,  55789,  83685, 111580, 139476, 172860]
]

B = [1/6, 5/24, 11/120, 19/720, 29/5040, 1/840]


def run_1(prs):
    print('INFO: Основной критерий монотонности')
    c = [0, 0, 0, 0, 0, 0]

    series = 1
    for v_last, v_cur in dist.Dist.iter_next_pairs(prs):
        if v_last <= v_cur:
            series += 1
        else:
            c[min(5, series - 1)] += 1
            series = 1
    c[min(5, series - 1)] += 1

    m = 0
    n = len(prs)
    for i in range(6):
        for j in range(6):
            m += (c[i] - n * B[i]) * (c[j] - n * B[j]) * A[i][j]
    m /= n - 6

    print('Вычисленная статистика M = {}'.format(m))
    chi2.conclusion(m, chi2.stat(6))


def run_2(prs):
    print('INFO: Упрощенный критерий монотонности')
    c = [0, 0, 0, 0, 0, 0]

    series = 1
    n = len(prs)
    skip = False
    for v_last, v_cur in dist.Dist.iter_next_pairs(prs):
        if skip:
            n -= 1
            continue
        if v_last <= v_cur:
            series += 1
            skip = False
        else:
            c[min(5, series - 1)] += 1
            if series > 1:
                skip = True
            series = 1
    c[min(5, series - 1)] += 1

    p = [0.5, 0.25, 0.125, 0.0625, 0.03125, 0.0150625]

    chi2.conclusion(chi2.compute(c, p, n), chi2.stat(6))
