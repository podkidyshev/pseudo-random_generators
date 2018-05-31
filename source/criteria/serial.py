import distributions
import criteria.chi2 as chi2


def serial(prs, d=15):
    print('INFO: Критерий серий. По умолчанию d = 15')

    k = d * d
    prsd = [int(v * d) for v in prs]
    nj = [0 for _idx in range(k)]
    for u1, u2 in distributions.Dist.iter_next_pairs(prsd):
        nj[u1 * d + u2] += 1

    chi2.conclusion(chi2.compute(nj, 1 / k, len(prsd)), chi2.stat(k))
