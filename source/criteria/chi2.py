from distributions import *


def chi2(prs, k=5, alpha=0.95):
    # a, b = 0, 1 - исследуем стандартное равномерное распределение
    ab = [((idx + 1) / k, idx / k) for idx in range(k)]
    nj = [0 for _idx in range(k)]
    ej = [len(prs) * (bi - ai) for ai, bi in ab]
    for value in prs:
        for idx, ai, bi in enumerate(ab):
            if ai < value <= bi:
                nj[idx] += 1
                break
        else:  # value == 0
            nj[0] += 1

    chi2_conclusion(chi2_compute(nj, ej), chi2_stat(alpha, k - 1))


def chi2_compute(nj: list, ej):
    chi = 0
    for idx, n in enumerate(nj):
        e = ej[idx] if type(ej) == list else ej
        chi += ((n - e) ** 2) / e if e else 0
    return chi


def chi2_stat(alpha, k):
    return stats.chi2.interval(alpha=alpha, df=k)


def chi2_conclusion(chi, interval):
    print("Вычисленное значение - {}".format(chi))
    print("Доверительный интервал = {}".format(interval))
    if chi <= interval[1]:
        print("ИТОГ: Вычисленное значение принадлежит доверительному интервалу. ПРС случайна")
    else:
        print("ИТОГ: ПРС не случайна")
