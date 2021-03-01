==========================================================
Dynamic Optimization of Task Parameters
==========================================================

JEDI automatically optimizes task parameters for compute/storage resource requirements
and strategies to partition workload while running those tasks. In the early stage of
the task execution, JEDI generates several jobs for each task using only a small portion of input data,
collects various metrics such as data processing rate and memory footprints, and adjusts the following task parameters.