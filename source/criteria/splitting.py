from math import floor

import criteria.chi2 as chi2


def splitting(prs_orig):
    # Приводим к дискретному распределению от 0 до (число различных карт - 1)
    prs = [floor(12 * v) for v in prs_orig]

    # будем рассматривать пятерки чисел
    d = 12
    k = 5
    n = len(prs) - k
    counts = [0] * k

    for i in range(n):
        # число различных элементов
        r = len(set(prs[i + j] for j in range(k)))
        counts[r] += 1

    """
    k = 5
    ni = [0] * k
    values = {v: set() for v in range(k)}

    for v in prs:
        res = min(floor(1000 * v) // k, k - 1)
        ni[res] += 1
        values[res].add(floor(1000 * v) % k)

    stirling = [0, 720, 1764, 1624, 735, 175, 21, 1]
    ej = [st * k for st in stirling]

    chi2.chi2_conclusion(chi2.chi2_compute(ni, ej), chi2.chi2_stat(0.95, k))
    """
