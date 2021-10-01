cwlVersion: v1.0
class: Workflow

inputs:
  dataset:
    type: string
  param_xxx:
    type: int
  param_yyy:
    type: float

outputs:
  outDS:
    type: string
    outputSource: core/outDS


steps:
  core:
    run: prun.cwl
    in:
      opt_inDS: dataset
      opt_exec:
        default: "echo %IN %%xxx%% %%yyy%% > seed.txt"
      opt_args:
        default: "--outputs seed.txt --avoidVP"
    out: [outDS]
