from distributions import *

DEFAULT_CHI2_DEGREES_OF_FREEDOM = 5


def chi2(prs):
    k = DEFAULT_CHI2_DEGREES_OF_FREEDOM
    print('INFO: КРИТЕРИЙ Хи-квадрат\n')
    print('Число степеней свободы k = {}'.format(k))
    # a, b = 0, 1 - исследуем стандартное равномерное распределение
    ab = [(idx / k, (idx + 1) / k) for idx in range(k)]
    nlist = [0 for _idx in range(k)]        # число значений в интервалах
    plist = [bi - ai for ai, bi in ab]      # теоретические вероятности попадания в интервалы
    for value in prs:
        for idx, (ai, bi) in enumerate(ab):
            if ai < value <= bi:
                nlist[idx] += 1
                break
        else:  # value == 0
            nlist[0] += 1

    conclusion(compute(nlist, plist, len(prs)), stat(k - 1))


def compute(nlist, plist, n):
    """
    Вычисление статистики хи-квадрат
    :param nlist: массив количества значений ПСП в интервалах
    :param plist: массив теоретических вероятностей попадания в интервалы
    :param n: число значений
    :return: выборочная статистика хи-квадрат
    """
    chi = 0
    for idx, nj in enumerate(nlist):
        pj = plist[idx] if type(plist) == list else plist
        ej = n * pj
        chi += ((nj - ej) ** 2) / ej if ej else 0
    return chi


def stat(k):
    """
    :param k: число степеней свободы
    :return: доверительный интервал с уровнем значимости 0.05 и k степенями свободы
    """
    return stats.chi2.interval(alpha=0.95, df=k)


def conclusion(chi, interval):
    print("Вычисленная статистика Хи2 - {}".format(chi))
    print("Доверительный интервал = {}".format(interval))
    if interval[0] <= chi <= interval[1]:
        print("ИТОГ: Вычисленное значение принадлежит доверительному интервалу. ППСЧ случайна")
    elif interval[1] < chi:
        print("ИТОГ: ППСЧ не случайна")
    else:
        print('ИТОГ: ГПСЧ не случаен')
