import numpy as np
import math

def compute_f_x(x, roh):
    f = math.floor(x/2**roh)
    return f


def compute_g_x(x, k, roh):
    f = max(compute_f_x(k, roh), 1) * math.floor(x / k)
    return f + (x % k)


def compute_r_one(roh, k, n):
    rounds = 1
    g_x = compute_g_x(n, k, roh)
    while g_x > k:
        g_x = compute_g_x(g_x, k, roh)
        rounds += 1
    return rounds, g_x


def compute_r_two(roh, k):
    if k > 1:
        rounds = 1
        f_x = compute_f_x(k, roh)
        while f_x > 1:
            f_x = compute_f_x(f_x, roh)
            rounds += 1
        return rounds
    else:
        return 0


def compute_r(roh, k, n):
    if n >= k:
        r_one, last_g = compute_r_one(roh, k, n)
    else:
        r_one = 0
        last_g = n
    r_two = compute_r_two(roh, last_g)
    return r_one + r_two


def compute_p_for_r(roh, k , n, r):
    if r == 1:
        return max(1, math.floor(n/k))
    else:
        f = (compute_f_x(k,roh)/k)**(r-1)
        return max(1, math.ceil((n/k))*f,)


def compute_N(alpha, delta):
    return math.ceil((math.log2(delta))/(math.log2((1-alpha))))

def compute_n_zero(alpha, delta):
    return math.ceil((math.log2(delta))/(2*(math.log2((1-alpha)))))

def compute_c_1(k, epochs):
    return math.log(2, (1 + ((k-1)/epochs)))

def compute_c_2(k, n_zero, epochs, N):
    base = 1 + ((k-1)/epochs)
    return 1 + math.log(n_zero + (4 * n_zero) / (n_zero - N), base)


def compute_c_3(k, epochs):
    return math.log(k, (1 + ((k-1)/epochs)))

def compute_c_e(e, k, epochs, n_zero, N):
    c_1 = compute_c_1(k, epochs)
    c_2 = compute_c_2(k,n_zero, epochs, N)
    c_3 = compute_c_3(k, epochs)
    numerator = ((c_1 * epochs) - ((2**epochs - 1)*((2 * c_1) - c_2 - c_3)))* 2**e
    denominator = 2**epochs * (-(e*c_1) + c_2 + c_3)
    return numerator/denominator

def format_runtime(runtime):
    """ """
    return '{}s = {}m = {}h = {}d'.format(runtime, runtime / 60, runtime / 3600, runtime / (3600 * 24))

def format_runtime_days(runtime):
    """ """
    return '{}'.format(np.around(runtime / (3600 * 24),2))