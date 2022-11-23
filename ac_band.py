import numpy as np
import math
import simulated_environment
import compute_parameter
from cse import cse, arm_elimination
import logging

logger = logging.getLogger(__name__)


def update_stats(stat_store, **kwargs):
    for s in stat_store.keys():
        stat_store[s].append(kwargs[s])
    return stat_store

def ac_band(env, conf_space, num_instances, budget, k, alpha,  delta , N = None):

    iteration_stats = {"e": [], "n_e": [], "roh_e": [], "c_e":[], "I_e": [], "R":[], "cpu_rt":[], "wc_rt": [], "instances": [], "configurations": []}
    seen_configurations = []
    seen_instances = []
    acb_cpu_rt = 0
    acb_wall_clock_rt = 0
    incumbent = [np.random.choice(conf_space)]

    if N is None:
        N = compute_parameter.compute_N(alpha, delta)

    n_zero = N + 1
    epochs = math.ceil(math.log2(n_zero/(n_zero - N)))

    logging.info(f"Starting AC-Band with: configurations: {len(conf_space)}, instances: {num_instances}, B: {budget}, k: {k}, "
          f"alpha: {alpha} delta: {delta}, n zero: {n_zero}, N: {N}, epochs: {epochs}")

    for e in range(1, epochs+1):
        logging.info(f"Starting epoch {e}")
        n_e = math.ceil((n_zero/(2**e))) + 1
        roh_e = math.log2(((e+k-1)/e))
        c_e = compute_parameter.compute_c_e(e, k, epochs, n_zero, N)
        I_e = budget / c_e
        R = compute_parameter.compute_r(roh_e, k, n_e)
        new_confs = np.random.choice([c for c in conf_space if c not in seen_configurations], n_e - 1, replace=False).tolist()
        seen_configurations = seen_configurations + new_confs
        confs = new_confs + incumbent

        instances = np.random.choice([i for i in range(0, int(num_instances)) if i not in seen_instances], int(I_e), replace=False).tolist()
        seen_instances = seen_instances + instances
        logger.info(f"AC-Band epoch: {e} with: n_e: {n_e}, roh_e: {roh_e}, c_e: {c_e}, I_e: {I_e}, R: {R}")
        incumbent, cse_cpu_rt, cse_wallclock_rt = cse(env, confs, k, roh_e, instances, R)

        acb_cpu_rt = acb_cpu_rt + cse_cpu_rt
        acb_wall_clock_rt = acb_wall_clock_rt + cse_wallclock_rt
        logger.info(f"New incumbent in e: {e}: {incumbent}, CSE cpu time{compute_parameter.format_runtime(cse_cpu_rt)} , CSE wc time{compute_parameter.format_runtime(cse_wallclock_rt)}")
        iteration_stats = update_stats(iteration_stats, e=e, n_e=n_e, roh_e=roh_e, c_e=c_e, I_e=I_e, R=R, cpu_rt = cse_cpu_rt, wc_rt = cse_wallclock_rt, instances=instances, configurations=confs)

    general_stats = {"incumbent": incumbent, "cpu_rt": acb_cpu_rt, "wallclock_rt": acb_wall_clock_rt ,"n_zero": n_zero, "N ":N }
    return incumbent, seen_configurations, general_stats, iteration_stats


def ac_band_until_budget(env, cpu_budget, configurations, num_instances , k, alpha, delta):
    hall_of_fame = []
    cpu_budget_sofar = 0
    wc_budget_sofar = 0

    N = compute_parameter.compute_N(alpha, delta)
    n_zero = N + 1

    number_conf_per_iter = n_zero + 8
    seen_configurations = []
    logger.info(f"Starting multiple AC-band runs with: Number of conf per iter: {number_conf_per_iter}")

    while cpu_budget_sofar < cpu_budget and (len(configurations) - len(seen_configurations)) >= number_conf_per_iter :

        confs = np.random.choice([c for c in configurations if c not in seen_configurations], number_conf_per_iter, replace=False).tolist()
        seen_configurations = seen_configurations + confs

        best_iteration, seen_confs_iteration, gs, es = ac_band(env, confs , num_instances, num_instances, k, alpha, delta)

        cpu_budget_sofar = cpu_budget_sofar + gs["cpu_rt"]
        wc_budget_sofar = wc_budget_sofar + gs["wallclock_rt"]
        hall_of_fame = hall_of_fame + best_iteration
        logger.info(f"Finished one AC-Band round with: cpu time: {cpu_budget_sofar}, current hall of fame. {hall_of_fame}, seen configuration: {len(seen_configurations)}{seen_configurations}")

    overall_best = arm_elimination(env, hall_of_fame, 1, list(range(num_instances)))

    general_stats = {"incumbent": overall_best, "cpu_rt": cpu_budget_sofar, "wallclock_rt": wc_budget_sofar,"cpu_budget":cpu_budget}

    return overall_best, general_stats



