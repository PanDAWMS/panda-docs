cwlVersion: v1.0
class: Workflow

inputs: []

outputs:
  outDS:
    type: string
    outputSource: third/outDS


steps:
  first:
    run: prun
    in:
      opt_exec:
        default: "Gen_tf.py --maxEvents=1000 --skipEvents=0 --ecmEnergy=5020 --firstEvent=1 --jobConfig=860059 --outputEVNTFile=evnt.pool.root --randomSeed=4 --runNumber=860059 --AMITag=e8201"
      opt_args:
        default: "--outputs evnt.pool.root --nJobs 3"
      opt_useAthenaPackages:
        default: true
    out: [outDS]

  second:
    run: prun
    in:
      opt_inDS: top/outDS
      opt_exec:
        default: "echo %IN > results.txt"
      opt_args:
        default: "--outputs results.txt"
    out: [outDS]

  third:
    run: prun
    in:
      opt_inDS: second/outDS
      opt_exec:
        default: "echo %IN > poststep.txt"
      opt_args:
        default: "--outputs poststep.txt --athenaTag AnalysisBase,21.2.167"
      opt_useAthenaPackages:
        default: true
    out: [outDS]
