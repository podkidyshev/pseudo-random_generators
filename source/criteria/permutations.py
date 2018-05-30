from math import factorial

import criteria.chi2 as chi2

DEFAULT_T = 4


def permutations(prs):
    t = DEFAULT_T
    ft = factorial(t)
    n_possible = len(prs) // t

    n_real = 0
    groups = []
    for group_number in range(n_possible):
        group = [prs[group_number * t + j] for j in range(t)]
        if len(set(group)) == len(group):  # в группе должны быть только разные числа
            n_real += 1
            groups.append(group)
    n = n_real

    counts = {}
    fill_permutations(counts, t, [], set(idx for idx in range(t)))
    for group in groups:
        s_group = [v for v in sorted(group)]
        permutation = tuple(s_group.index(v) for v in group)
        counts[permutation] += 1

    chi2.chi2_conclusion(chi2.chi2_compute(list(counts.values()), n / ft), chi2.chi2_stat(0.95, ft))


def fill_permutations(container, t, buffer, values_buffer):
    for i in values_buffer:
        buffer.append(i)
        values_buffer.remove(i)
        if len(buffer) == t:
            container[tuple(buffer)] = 0
        else:
            fill_permutations(container, t, buffer, values_buffer)
        buffer.pop()
        values_buffer.add(i)
