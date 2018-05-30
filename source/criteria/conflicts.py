from functools import reduce


def conflicts(prs):
    # длина тестируемой последовательности должна быть 2 ** 14 = 16384
    # числа должны быть размера 2 ** 20 = 1048576
    conflicts_count = {}
    for v in prs:
        conflicts_count[v] = 1 if v in conflicts_count else 0
    res = reduce(int.__add__, conflicts_count.values())

    conflicts_crit = 145  # alpha = 0.946
    comp = compute_probabilities(2 ** 20, 2 ** 14)
    print(comp)
    print(res)


def compute_probabilities(m, n):
    a = [0 for _idx in range(n + 1)]
    a[1] = 1
    j0, j1 = 1, 1
    for _k in range(n - 1):
        j1 += 1
        j = j1
        lel = j0
        while j >= lel:
            a[j] = (j / m) * a[j] + ((1 + 1 / m) - (j / m)) * a[j - 1]
            if a[j] < 0.00001:
                a[j] = 0
                if j == j1:
                    j1 -= 1
                elif j == j0:
                    j0 += 1
            j -= 1

    print(max(a))

    tlist = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1]
    res = []
    p = 0
    j = j0 - 1
    t = 0
    while t != len(tlist) - 1:
        j += 1
        p += a[j]
        if p > tlist[t]:
            res.append((n - j - 1, 1 - p))
        while p <= tlist[t] and t < len(tlist) - 1:
            t += 1

    return res
