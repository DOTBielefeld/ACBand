import math
import compute_parameter
import logging
logger = logging.getLogger(__name__)

def configuration_partition(set, size):
    partition = []
    for i in range(0, len(set), size):
        partition.append(set[i:i + size])
    return partition


def initial_instance_partition(instances, R):
    instances_partition = []
    size = int(math.floor(len(instances) / R))
    previous = 0
    next = size
    for r in range(R):
        instances_partition.append(instances[previous:next])
        previous = next
        next = next + size
    return instances_partition

def instance_partition_for_round(instances_round, b_r, number_partions):
    instances_partition = []
    size = b_r
    previous = 0
    next = size
    for r in range(number_partions):
        instances_partition.append(instances_round[previous:next])
        previous = next
        next = next + size
    return instances_partition

def arm_elimination(env, active_confs, num_winners, instance_set):
    num_winners = max(num_winners, 1)
    feedback_store = {conf: 0 for conf in active_confs}
    cpu_rt = 0
    wall_clock_rt = 0

    for instance in instance_set:
        instance_results = {}
        for configuration in active_confs:
            did_timeout, time_taken, _ = env.run(config_id=configuration, timeout=900, instance_id=instance)
            instance_results[configuration] = time_taken

        winner_on_instance = min(instance_results, key=instance_results.get)
        feedback_store[winner_on_instance] = feedback_store[winner_on_instance] + 1
        cpu_rt = cpu_rt + (instance_results[winner_on_instance] * len(active_confs))
        wall_clock_rt = wall_clock_rt + instance_results[winner_on_instance]

    ordering = sorted(feedback_store, key=feedback_store.get, reverse=True)
    return ordering[:num_winners], cpu_rt, wall_clock_rt


def cse(env, configuration_ids, k, roh, instance_ids, R):

    n = len(configuration_ids)
    B = len(instance_ids)
    logger.info(f"Starting CSE with: configurations: {len(configuration_ids)}, k: {k}, roh: {roh}, instances: {len(instance_ids)}, R: {R}")

    instances_for_rounds = initial_instance_partition(instance_ids, R)
    active_configurations = configuration_ids
    r = 1
    cse_cpu_rt = 0
    cse_wallclock_rt = 0

    while len(active_configurations) >= k:

        next_active_set = []
        round_configuration_partition = configuration_partition(active_configurations, k)

        p = len(round_configuration_partition)
        f = compute_parameter.compute_f_x(k, roh)

        remainder = 0
        if len(round_configuration_partition[-1]) < k:
            p = p - 1
            next_active_set += round_configuration_partition[-1]
            remainder =  round_configuration_partition[-1]
            del round_configuration_partition[-1]

        b = int(math.floor((B / (p * R))))
        round_instance_partition = instance_partition_for_round(instances_for_rounds[r-1], b, p)
        logger.info(f"CSE: round: {r}, p: {p}, b: {b},f: {f} conf: {round_configuration_partition}, remainder: {remainder} instances: {round_instance_partition}")
        for j in range(len(round_configuration_partition)):
            best_confs, cpu_rt_j, wall_clock_rt_j = arm_elimination(env, round_configuration_partition[j], f, round_instance_partition[j])
            next_active_set += best_confs
            cse_cpu_rt = cse_cpu_rt + cpu_rt_j
            cse_wallclock_rt = cse_wallclock_rt + wall_clock_rt_j

        active_configurations = next_active_set
        r += 1

    while len(active_configurations) > 1 :
        p = int(compute_parameter.compute_p_for_r(roh, k, n, r))
        b = int(math.floor((B / (p * R))))
        f = compute_parameter.compute_f_x(len(active_configurations), roh)

        logger.info(f"CSE: round: {r}, p: {p}, b: {b}, f: {f} conf: {active_configurations}, instances: {instances_for_rounds[r-1]}")
        active_configurations, cpu_rt_j, wall_clock_rt_j = arm_elimination(env, active_configurations, f, instances_for_rounds[r-1])
        cse_cpu_rt = cse_cpu_rt + cpu_rt_j
        cse_wallclock_rt = cse_wallclock_rt + wall_clock_rt_j
        r += 1

    return active_configurations, cse_cpu_rt, cse_wallclock_rt
