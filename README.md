# on-the-emerging-potential-of-quantum-annealing-hardware 

The software and data in this repository comprise a snapshot of artifacts used in the production of the article [_On the Emerging Potential of Quantum Annealing Hardware for Combinatorial Optimization_](https://arxiv.org/pdf/2210.04291.pdf) by B. Tasseff, T. Albash, Z. Morrell, M. Vuffray, A. Y. Lokhov, S. Misra, and C. Coffrin.
This snapshot is based on the specific Ising model instances found in the `data` directory.
Snapshots of unprocessed experimental output are provided in the subdirectories of `results`.
Finally, various postprocessing utilities are provided in the `scripts` directory.

## Instances

First, to uncompress all Ising model instance data, execute
```bash
find data/instances/ -name "*.zip" -exec sh -c 'unzip -o "{}" -d "$(dirname "{}")"' \;
```

Each instance is stored in a directory corresponding to its lattice size and suffixed with an index ranging from 1 to 50.
For example, `data/instances/Pegasus-Lattice_Size-2/Pegasus-Lattice_Size-2_00036.json` corresponds to the 36th generated Ising model instance with a lattice size of two.
Each Ising model instance is stored in a JSON-based encoding of a binary quadratic program.
This format is named `bqpjson`.
A detailed description of the `bqpjson` format is available [here](http://bqpjson.readthedocs.io/en/latest/bqpjson_format.html).


## Results

To uncompress all solver benchmarking results, execute
```bash
find data/results/ -name "*.zip" -exec sh -c 'unzip -o "{}" -d "$(dirname "{}")"' \;
```

### Subdirectory Naming

Within each `Pegasus-Lattice_Size-*` directory, results are partitioned into subdirectories based on (i) the solution method employed (the prefix) and (ii) the time or iteration limit (the suffix).
For example, the file `Pegasus-Lattice_Size-16/iqp_gurobi_0000064/Pegasus-Lattice_Size-16/Pegasus-Lattice_Size-16_00001.stdout` corresponds to the output from the `iqp_gurobi` solver for the first `Pegasus-Lattice_Size-16` instance when using a time limit of 64 seconds.
Another example is `Pegasus-Lattice_Size-2/pt_par_0016384/Pegasus-Lattice_Size-2/Pegasus-Lattice_Size-2_00010.stdout`, which corresponds to the output from the `pt_par` (parallel tempering) solver for the tenth `Pegasus-Lattice_Size-2` instance when using 16,384 parallel tempering updates per run.
More information on each solver and their possible parameterizations are described in the appendix of the article.
Below, we briefly describe the solver prefixes and suffixes that appear in each subdirectory.
Only a subset of these solvers is employed for instances with lattice sizes less than 16.

- `grd_dwave_*`: [D-Wave's steepest descent greedy heuristic](https://github.com/dwavesystems/dwave-greedy), where the suffix corresponds to the number of times the steepest descent is executed (`num_reads` in the documentation's parlance). Note that neither this solver nor its results are discussed in our article, as we used the `grd_scd` solver as our comparative greedy heuristic.
- `grd_scd_*`: A steepest coordinate descent heuristic implemented in Julia. The suffix corresponds to the time limit in seconds.
- `ilp_gurobi_*`: An integer linear programming model solved using Gurobi. The suffix corresponds to the time limit in seconds.
- `iqp_cplex_*`: An integer quadratic programming model solved using CPLEX. The suffix corresponds to the time limit in seconds.
- `iqp_gurobi_*`: An integer quadratic programming model solved using Gurobi. The suffix corresponds to the time limit in seconds.
- `iqp_gurobipar_*`: An integer quadratic programming model solved using Gurobi with tuned parameters and parallelism. The suffix corresponds to the time limit in seconds.
- `mcmc_gd_*`: A Markov chain Monte Carlo heuristic based on Glauber dynamics. The suffix corresponds to the time limit in seconds.
- `mp_ms_*`: A message passing (message-based min-sum) heuristic. The suffix corresponds to the time limit in seconds.
- `pt_par_*`: A parallel tempering algorithm. The suffix corresponds to the number of parallel tempering updates per independent run.
- `pt_par_betamax_8_*`: A parallel tempering algorithm with a non-default inverse temperature distribution. The suffix corresponds to the number of parallel tempering updates per independent run.
- `qa*_dwave_*`: Quantum annealing using D-Wave's Advantage system. The suffix immediately following `qa*` corresponds to the annealing time in tenths of a microsecond, and the suffix following `dwave_` corresponds to the number of anneal-read cycles. For example, `qa3125_dwave_0001280` corresponds to a quantum annealing run with an annealing time of 312.5 microseconds and 1280 anneal-read cycles.
- `sa_dwave_*`: [D-Wave's simulated annealing heuristic](https://github.com/dwavesystems/dwave-neal). The suffix corresponds to the number of simulated annealing sweeps (random perturbations per discrete temperature value).
- `svmc_par_*`: A parallelized spin-vector Monte Carlo (SVMC) algorithm. The suffix corresponds to the number of sweeps per independent SVMC run in a parallel set.
- `tabu_dwave_*`: [D-Wave's tabu search heuristic](https://github.com/dwavesystems/dwave-tabu). The suffix corresponds to the number of "reads" (`num_reads` in the documentation's parlance), where each read is generated by one run of the tabu algorithm.

## Scripts

A small number of helpful Python scripts are provided in the `scripts` directory for readers interested in (i) parsing our `bqpjson` instances for their own research or (ii) postprocessing our experimental results.
These utilities assume that the user has Python 3.7 or later installed on their system.
First, to install the necessary Python dependencies, execute
```bash
pip install -r scripts/requirements.txt
```

### Parsing Instances

### Postprocessing Results

## Citing

If you have found this repository useful in your work, please cite [the corresponding article](https://arxiv.org/pdf/2210.04291.pdf):
Below is a BibTeX entry that may be used:
```
@misc{tasseff+:arxiv22,
  title         = {On the Emerging Potential of Quantum Annealing Hardware for Combinatorial Optimization},
  author        = {Byron Tasseff and Tameem Albash and Zachary Morrell and Marc Vuffray and Andrey Y. Lokhov and Sidhant Misra and Carleton Coffrin},
  year          = {2022},
  eprint        = {2210.04291},
  archivePrefix = {arXiv},
  primaryClass  = {math.OC}
}
```

## License

This software is provided under a BSD-ish license with a "modifications must be indicated" clause.
See the `LICENSE.md` file for the full text.
This package is part of the Hybrid Quantum-Classical Computing suite, known internally as LA-CC-16-032.
