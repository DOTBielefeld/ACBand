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
from matrix_enviroment import RuntimeMatrixEnvironment
from ac_band import ac_band
from compute_parameter import compute_p_for_r, compute_g_x

import logging
import sys


logger = logging.getLogger()
logger.setLevel(logging.INFO)


for ips in [35640]:
    for alpha in [0.05, 0.02, 0.01]:
        for kk in [2,4,8,16]:
            for s in range(5):

                seed = 520 + s
                num_confs = 2000
                num_instances = ips
                k = kk
                alpha = alpha
                delta = 0.05
                timeout = 900
                N = compute_parameter.compute_N(alpha, delta)

                np.random.seed(seed)

                logger_path = f"./logs/acband/rcw/AC-Band_GS_rcw_{num_confs}_{num_instances}_{k}_{alpha}_{delta}_{N}_{seed}.log"

                fileh = logging.FileHandler(logger_path)
                formatter = logging.Formatter('%(asctime)s %(message)s')
                fileh.setFormatter(formatter)

                log = logging.getLogger()
                for hdlr in log.handlers[:]:
                    log.removeHandler(hdlr)
                log.addHandler(fileh)
                log.addHandler(logging.StreamHandler())


                results_file = f"./data/dataset_icar/cplex_rcw/cplex_rcw_rt_seed52{s}.npy"
                env = RuntimeMatrixEnvironment(results_file, timeout)

                best, _, gs, es = ac_band(env, list(range(num_confs)), num_instances, num_instances, k, alpha,  delta)
                print(gs)


                with open(f'./results/acband/rcw/AC-Band GS_rcw_{num_confs}_{num_instances}_{k}_{alpha}_{delta}_{N}_{seed}.p', 'wb') as f:
                     pickle.dump(gs, f)

                with open(f'./results/acband/rcw/AC-Band_ES_rcw_{num_confs}_{num_instances}_{k}_{alpha}_{delta}_{N}_{seed}.p','wb') as f:
                 pickle.dump(es, f)
