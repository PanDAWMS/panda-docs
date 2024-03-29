cwlVersion: v1.0
class: Workflow

inputs: []

outputs:
  outDS:
    type: string
    outputSource: bottom/outDS


steps:
  top:
    run: prun
    in:
      opt_exec:
        default: "echo %RNDM:10 > seed.txt"
      opt_args:
        default: "--outputs seed.txt --nJobs 3 --avoidVP"
    out: [outDS]

  bottom:
    run: prun
    in:
      opt_inDS: top/outDS
      opt_exec:
        default: "echo %IN > results.root"
      opt_args:
        default: "--outputs results.root --forceStaged --avoidVP"
    out: [outDS]
