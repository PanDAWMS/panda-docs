===========================
Run on GPU
===========================

GPUs (Graphics Processing Unit) have numerous advantages in data-intensive tasks, 
physics analysis, machine learning, and other fields, making them powerful tools for 
high-performance and efficient calculations and processing.

GPU resources are avaialbe exclusively at designated sites, necessitating explicit job assignment. 
Users need to specify the GPU architecture in the ``--architecture`` option when executing ``prun``. 
For example, to utilize NVIDIA GPUs, you can set the argument like: ``--architecture '&nvidia'``.　e.g.,

|br|

.. prompt:: bash
            
 prun --containerImage docker://gitlab-registry.cern.ch/hepimages/public/gpu-basic-test --exec "python /test-gpu.py" --outDS user.[USER].`uuidgen` --noBuild --nJobs=1 --architecture '&nvidia'
