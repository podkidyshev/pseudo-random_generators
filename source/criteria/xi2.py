from distributions import *
from criteria import *


class Xi2(Criteria):
    def __init__(self, args):
        self.k = 5

        super().__init__()

    def check(self, prs, dist):
        # dist.dist(0)
        # """
        a, b = min(prs), max(prs)
        intervals = []
        for idx in range(self.k):
            ai = a + (idx / self.k) * (b - a)
            bi = a + ((idx + 1) / self.k) * (b - a)
            intervals.append({'ab': (ai, bi), 'nj': 0})
        for value in prs:
            for aibi in intervals:
                if aibi['ab'][0] < value <= aibi['ab'][1]:
                    aibi['nj'] += 1
                    break
            else:
                intervals[0]['nj'] += 1

        for aibi in intervals:
            fbi = dist.cdf(aibi['ab'][1])
            fai = dist.cdf(aibi['ab'][0])
            aibi['pj'] = fbi - fai
            aibi['Ej'] = len(prs) * aibi['pj']

        xi2 = 0
        for aibi in intervals:
            nj, ej = aibi['nj'], aibi['Ej']
            v = ((nj - ej) ** 2) / ej if ej else 0
            xi2 += v

        interval = stats.chi2.interval(alpha=0.05, df=4)
        print("Вычисленное значение - {}".format(xi2))
        print("Доверительный интервал = {}".format(interval))
        if interval[0] <= xi2 <= interval[1]:
            print("Вычисленное значение принадлежит доверительному интервалу. " +
                  "Случайная величина подчиняется теоретическому распределению")
        elif xi2 < interval[0]:
            print("Xi2 входит в левый 'хвост'. Генератор не случае")
        else:
            print("Случайная величина не подчиняется теоретическому распределению")
        # """

