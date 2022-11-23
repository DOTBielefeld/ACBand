import collections
import numpy as np
import os
import pickle

import json

# Env as suggested in https://github.com/empennage98/icar

class RuntimeMatrixEnvironment():
    def __init__(self, fn, seed=520):

        # fn is the filename of the runtime matrix
        self.rt = np.load(fn)
        self.run_so_far = collections.defaultdict(dict)
        self.total_runtime = 0


    def _run(self, config_id, instance_id, timeout):

        return min(self.rt[config_id,instance_id], timeout)

    def run(self, config_id, instance_id, timeout):

        runtime = self._run(config_id, instance_id, timeout)
        if instance_id in self.run_so_far[config_id]:
            if runtime > self.run_so_far[config_id][instance_id]:
                self.total_runtime += runtime - self.run_so_far[config_id][instance_id]
                self.run_so_far[config_id][instance_id] = runtime
        else:
            self.total_runtime += runtime
            self.run_so_far[config_id][instance_id] = runtime

        return runtime < timeout, min(runtime, timeout), ""