cwlVersion: v1.0
class: Workflow

inputs:
  dataset:
    type: string
  param_sliced_x:
    type: int
  param_sliced_y:
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
        default: "echo %IN %{sliced_x} %{sliced_y} > seed.txt"
      opt_args:
        default: "--outputs seed.txt --avoidVP"
    out: [outDS]
