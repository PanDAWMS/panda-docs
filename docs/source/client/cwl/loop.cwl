cwlVersion: v1.0
class: Workflow

requirements:
  SubworkflowFeatureRequirement: {}

inputs: []

outputs:
  outDS:
    type: string
    outputSource: work_end/outDS


steps:
  work_start:
    run: prun
    in:
      opt_exec:
        default: "echo %RNDM:10 > seed.txt"
      opt_args:
        default: "--outputs seed.txt --nJobs 2 --avoidVP"
    out: [outDS]

  work_loop:
    run: loop_body.cwl
    in:
      dataset: work_start/outDS
    out: [outDS]
    hints:
      - loop

  work_end:
    run: prun
    in:
      opt_inDS: work_loop/outDS
      opt_exec:
        default: "echo %IN > results.root"
      opt_args:
        default: "--outputs results.root --forceStaged"
    out: [outDS]
