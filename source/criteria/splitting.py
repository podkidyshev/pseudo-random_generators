from math import floor
from sympy.functions.combinatorial.numbers import stirling
import criteria.chi2 as chi2


def splitting(prs_orig):
    # Данный критерий называется также покер-критерий
    # Приводим к дискретному распределению от 0 до <число различных карт - 1=12>
    d = 13  # число различных карт
    prs = [floor(d * v) for v in prs_orig]

    k = 5              # пятерки чисел/карт
    n = len(prs) // k  # число групп элементов
    counts = [0] * k   # массив: в r-ой ячейке число групп с r+1-различными картами (нуль-нумерация)

    for i in range(n):
        # число различных элементов/карт в руке
        r = len(set(prs[i * k + j] for j in range(k)))
        counts[r - 1] += 1

    plist = []
    for r in range(1, k + 1):
        pr = 1 / (d ** k)
        st = stirling(k, r, kind=2)
        pr *= st
        for i in range(r):
            pr *= d - i
        plist.append(pr * n)

    chi2.chi2_conclusion(chi2.chi2_compute(counts, plist), chi2.chi2_stat(0.95, k))
