from math import sqrt, log


def series(prs):
    var_series = list(sorted(prs))
    if len(prs) & 1:
        xmed = var_series[len(prs) // 2]
    else:
        xmed = 0.5 * (var_series[len(prs) // 2] + var_series[len(prs) // 2 + 1])

    v = 1
    tau = 0
    cur_sign = prs[0] < xmed
    cur_count = 1
    for idx, value in enumerate(prs):
        if idx == 0 or value == xmed:
            continue
        next_sign = value < xmed
        if cur_sign == next_sign:
            cur_count += 1
        else:
            v += 1
            cur_sign = next_sign
            tau = max(tau, cur_count)
            cur_count = 0

    n = len(prs)
    print("Число серий = {}".format(v))
    print("Длина максимальной серии - {}".format(tau))
    v1 = 0.5 * (n + 1 - 1.96 * sqrt(n - 1))
    v2 = 3.3 * log(n + 1, 10)
    correct = v > v1 and tau < v2
    print("для v {}, для tau {}".format(v1, v2))
    if correct:
        print("Гипотеза принята, последовательность случайна")
    else:
        print("Гипотеза отвергается. Последовательность не случайна")
