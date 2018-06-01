import distributions
import criteria.chi2 as chi2


def serial(prs, d=15):
    print('INFO: КРИТЕРИЙ серий\n')

    k = d * d
    prsd = [int(v * d) for v in prs]
    nj = [0 for _idx in range(k)]
    for j in range(len(prsd) // 2):
        u1, u2 = prsd[2 * j], prsd[2 * j + 1]
        nj[u1 * d + u2] += 1

    chi2.conclusion(chi2.compute(nj, 1 / k, len(prsd) // 2), chi2.stat(k))
