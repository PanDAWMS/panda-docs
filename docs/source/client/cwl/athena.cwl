cwlVersion: v1.0
class: Workflow

inputs: []

outputs:
  outDS:
    type: string
    outputSource: second/outDS


steps:
  first:
    run: prun.cwl
    in:
      opt_exec:
        default: "Gen_tf.py --maxEvents=1000 --skipEvents=0 --ecmEnergy=5020 --firstEvent=1 --jobConfig=860059 --outputEVNTFile=evnt.pool.root --randomSeed=4 --runNumber=860059 --AMITag=e8201"
      opt_args:
        default: "--outputs evnt.pool.root --nJobs 3"
      opt_useAthenaPackages:
        default: true
    out: [outDS]

  second:
    run: prun.cwl
    in:
      opt_inDS: top/outDS
      opt_exec:
        default: "echo %IN > results.txt"
      opt_args:
        default: "--outputs results.txt"
    out: [outDS]

    