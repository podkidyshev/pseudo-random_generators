import criteria.chi2 as chi2


def intervals(prs):
    print('INFO: Критерий интервалов. Проверка на "отклонение выше среднего" (a = 0, b = 0.5)')
    a, b = 0, 0.5

    t = 5
    n = len(prs) // 4
    s = 0
    cr = [0 for _idx in range(t + 1)]

    r = 0
    last = True
    for j in range(len(prs)):
        if a <= prs[j] <= b and not last:
            cr[min(r, t)] += 1
            s += 1
            last = True
        elif not a <= prs[j] <= b and last:
            r = 1
            last = False
        elif not a <= prs[j] <= b and not last:
            r += 1
        elif a <= prs[j] <= b and last:
            cr[0] += 1
            s += 1
        if s > n:
            break

    p = b - a
    pr = [(1 - p) ** t if r == t else p * (1 - p) ** r for r in range(t + 1)]
    chi2.conclusion(chi2.compute(cr, pr, n), chi2.stat(t + 1))
