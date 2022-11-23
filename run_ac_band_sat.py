import sys
import os
sys.path.append(os.getcwd())
import numpy as np
import pickle
import logging

import compute_parameter
import math
from cse import initial_instance_partition, instance_partition_for_round, arm_elimination, cse
#from ac_band import ACBand
import simulated_environment
from ac_band import ac_band
from compute_parameter import compute_p_for_r, compute_g_x

import logging
import sys


logger = logging.getLogger()
logger.setLevel(logging.INFO)

for ips in [20118]:
    for alpha in [ 0.05, 0.02, 0.01]:
        for kk in [2,4,8,16]:
            for s in range(5):
                seed = 520 + s
                num_confs = 972
                num_instances = ips
                k = kk
                alpha = alpha
                delta = 0.01
                timeout = 900
                N = compute_parameter.compute_N(alpha, delta)

                np.random.seed(seed)

                logger_path = f"./logs/acband/sat/AC-Band_GS_SAT_{num_confs}_{num_instances}_{k}_{alpha}_{delta}_{N}_{seed}.log"

                fileh = logging.FileHandler(logger_path)
                formatter = logging.Formatter('%(asctime)s %(message)s')
                fileh.setFormatter(formatter)

                log = logging.getLogger()
                for hdlr in log.handlers[:]:
                    log.removeHandler(hdlr)
                log.addHandler(fileh)
                log.addHandler(logging.StreamHandler())


                results_file = "./data/measurements.dump"
                env = simulated_environment.Environment(results_file, timeout)

                best,_ , gs, es = ac_band(env, list(range(num_confs)), num_instances, num_instances, k, alpha,  delta)

                with open(f'./results/acband/sat/AC-Band_GS_SAT_{num_confs}_{num_instances}_{k}_{alpha}_{delta}_{N}_{seed}.p', 'wb') as f:
                     pickle.dump(gs, f)

                with open(f'./results/acband/sat/AC-Band_ES_SAT_{num_confs}_{num_instances}_{k}_{alpha}_{delta}_{N}_{seed}.p','wb') as f:
                 pickle.dump(es, f)
