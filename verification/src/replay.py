"""Exact rational checks for model predictions, the finite grid and atomic witnesses."""

from fractions import Fraction as F
from itertools import product
from random import Random


def means(order, weights, action):
    x = [F(1)] + [F(0)] * len(order)
    for v in order:
        x[v] = F(action[v]) if v in action else sum(a * b for a, b in zip(weights[v], x))
    return x


def random_model(d, rng):
    order = list(range(1, d))
    rng.shuffle(order)
    order.append(d)
    weights = {}
    for i, v in enumerate(order):
        available = {0, *order[:i]}
        entries = [rng.randrange(5) if j in available else 0 for j in range(d + 1)]
        weights[v] = [F(value, 1 + sum(entries)) for value in entries]
    return order, weights


def residual_cases():
    rng = Random(441)
    for _ in range(1200):
        d = rng.randrange(2, 10)
        T = rng.randrange(1, 25)
        step = F(1, (d + 1) ** 3 * T ** 2)
        true_order, true = random_model(d, rng)
        other_order, other = random_model(d, rng)
        action = {v: rng.randrange(2) for v in range(1, d) if rng.random() < .35}
        x = means(true_order, true, action)
        y = means(other_order, other, action)
        diff = [b - a for a, b in zip(x, y)]
        residuals = []
        for v in other_order:
            if v in action:
                assert diff[v] == 0
                continue
            rv = sum((b - a) * z for a, b, z in zip(true[v], other[v], x))
            assert rv == diff[v] - sum(w * e for w, e in zip(other[v], diff))
            assert rv ** 2 <= 4 * sum(z ** 2 for z in diff)
            residuals.append(rv)
        assert max(map(abs, diff)) <= sum(map(abs, residuals))
        rounded = {v: [(entry // step) * step for entry in row] for v, row in true.items()}
        xr = means(true_order, rounded, action)
        assert max(abs(a - b) for a, b in zip(x, xr)) <= d * (d + 1) * step <= F(1, d * T)
    print('Mean residual and rounding checks: 1,200 exact rational model/action pairs.')


def first_round_grid():
    # d=2, T=1, target sink Y. All 11,368 rows on the actual h=1/27 grid.
    d, T = 2, 1
    n = (d + 1) ** 3 * T ** 2
    c = d * (((n + 1) ** (d * (d + 1))) * (T + 1) ** 2).bit_length()
    assert c == 62
    count = 0
    grid_max = F(-1)
    for root in range(n + 1):
        for intercept in range(n + 1):
            for edge in range(n - intercept + 1):
                weights = {1: (F(root, n), 0, 0), 2: (F(intercept, n), F(edge, n), 0)}
                for action in ({}, {1: 0}, {1: 1}):
                    result = means((1, 2), weights, action)
                    assert all(0 <= v <= 1 for v in result)
                    grid_max = max(grid_max, result[-1])
                count += 1
    assert count == 11368 and grid_max == 1
    print('Actual first-round model grid: all 11,368 models and 34,104 action predictions checked.')


def atomic_cases():
    count = 0
    for m in range(2, 8):
        r, a = F(1, m), F(1, 8 * m)
        roots = list(product((0, 1), repeat=m))
        actions = [None] + [(i, b) for i in range(m) for b in (0, 1)]
        for j in range(m):
            for delta in (F(1, 8), F(1, 16), F(1, 24)):
                scores = {}
                for action in actions:
                    total = baseline_mean = alternative_mean = chi_square_bound = F(0)
                    for x in roots:
                        if action is not None and x[action[0]] != action[1]:
                            continue
                        weight = F(1)
                        for i, bit in enumerate(x):
                            if action is None or action[0] != i:
                                weight *= r if bit else 1 - r
                        p = F(1, 2) + a * sum(x)
                        q = p + delta * x[j]
                        assert F(1, 2) <= p <= q <= F(3, 4)
                        chi_square_bound += weight * (p - q) ** 2 / (q * (1 - q))
                        total += weight
                        baseline_mean += weight * p
                        alternative_mean += weight * q
                    assert total == 1
                    assert chi_square_bound <= 6 * delta ** 2 * (1 if action == (j, 1) else r)
                    scores[action] = (baseline_mean, alternative_mean)
                    count += 1
                assert scores[j, 1][0] == max(pair[0] for pair in scores.values())
                for action, pair in scores.items():
                    if action != (j, 1):
                        assert scores[j, 1][1] - pair[1] >= delta * (1 - r)
    assert F(1, 16) * (F(1, 2) - F(5, 16)) > F(1, 100)
    print(f'Atomic family: {count} exact distribution, gap and chi-square-bound checks.')


def illustration():
    reference = {1: (F(1, 5), 0, 0, 0), 2: (F(1, 10), F(1, 2), 0, 0),
                 3: (F(1, 10), F(1, 5), F(1, 2), 0)}
    candidate = {1: (F(1, 10), 0, F(1, 2), 0), 2: (F(1, 5), 0, 0, 0),
                 3: (F(1, 10), F(3, 5), F(1, 5), 0)}
    expected = (
        ((20, 20, 24), (20, 20, 26)),
        ((100, 60, 60), (100, 20, 74)),
        ((20, 100, 64), (60, 100, 66)),
    )
    for action, pair in zip(({}, {1: 1}, {2: 1}), expected):
        x, y = means((1, 2, 3), reference, action), means((2, 1, 3), candidate, action)
        assert (tuple(100 * a for a in x[1:]), tuple(100 * b for b in y[1:])) == pair
        if action == {1: 1}:
            e = [b - a for a, b in zip(x, y)]
            residual = sum((a - b) * c for a, b, c in zip(candidate[3], reference[3], x))
            assert residual == F(22, 100)
            assert e[3] == residual + F(1, 5) * e[2] == F(14, 100)
    print('Worked illustration: all three intervention pairs and the exact reward residual passed.')


if __name__ == '__main__':
    residual_cases()
    first_round_grid()
    atomic_cases()
    illustration()
