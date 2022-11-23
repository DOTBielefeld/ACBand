# ACBand
This is an implementation of AC-Band, an algorithm configurator described in the paper AC-Band: A Combinatorial Bandit-Based Approach to Algorithm Configuration.

#### Abstract 
We study the algorithm configuration (AC) problem, in which one seeks to find an optimal parameter configuration of a given target algorithm in an automated way. Recently, there has been significant progress in designing AC approaches that satisfy strong theoretical guarantees. However, a significant gap still remains between the practical performance of these approaches and state-of-the-art heuristic methods. To this end, we introduce AC-Band, a general approach for the AC problem based on multi-armed bandits that provides theoretical guarantees while exhibiting strong practical performance. We show that AC-Band requires significantly less computation time than other AC approaches providing theoretical guarantees while still yielding high-quality configurations.
#### Requirements
Python 3, numpy, matplotlib

#### Experimental Setup
The saved runtimes of the CPLEX integer progarm solver on two datsets (Regions, RCW) can be downloaded [here](https://www.cs.ubc.ca/~drgraham/datasets.html) and the saved runtimes of Minisat sat solver on the CNFuzzdd data can be downloaded from this [repo](https://github.com/deepmind/leaps-and-bounds).
The runtime environments are obtained from [here]( https://github.com/deepmind/leaps-and-bounds) and [here](https://github.com/empennage98/icar)
#### Running the Code

```
# Main experiments
python run_ac_band_[rcw|region|sat].py
``` 
