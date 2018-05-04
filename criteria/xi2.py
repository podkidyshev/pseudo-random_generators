from dist import *
from criteria import *


class Xi2(Criteria):
    def __init__(self, args):
        self.k = 5

        super().__init__()

    def check(self, prs, distribution):
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
            fbi = distribution.distribution(aibi['ab'][1])
            fai = distribution.distribution(aibi['ab'][0])
            aibi['pj'] = fbi - fai
            aibi['Ej'] = len(prs) * aibi['pj']

        xi2 = 0
        for aibi in intervals:
            nj, ej = aibi['nj'], aibi['Ej']
            v = ((nj - ej) ** 2) / ej
            xi2 += v

        print(xi2)
