cwlVersion: v1.0
class: Workflow

requirements:
  ScatterFeatureRequirement: {}
  SubworkflowFeatureRequirement: {}

inputs:
  signals: string[]

outputs:
  outDS:
    type: string
    outputSource: work_end/outDS


steps:
  work_loop:
    run: loop_body.cwl
    scatter: [dataset]
    scatterMethod: dotproduct
    in:
      dataset: signals
    out: [outDS]
    hints:
      - loop

  merge:
    run: prun
    in:
      opt_inDS: work_loop/outDS
      opt_exec:
        default: "echo %IN > results.root"
      opt_args:
        default: "--outputs results.root --forceStaged"
    out: [outDS]
