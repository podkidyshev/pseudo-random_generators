import distributions
import criteria.chi2 as chi2


def series(prs_orig, d=15):
    prs = prs_orig[:]

    k = d * d
    prsd = [int(v * d) for v in prs]
    nj = [0 for _idx in range(k)]
    for u1, u2 in distributions.Dist.iter_next_pairs(prsd):
        nj[u1 * d + u2] += 1

    ej = len(prsd) / k
    chi = 0
    for j in range(k):
        v = ((nj[j] - ej) ** 2) / ej
        chi += v

    chi2.chi2_conclusion(chi2.chi2_compute(nj, ej), chi2.chi2_stat(0.95, k))
