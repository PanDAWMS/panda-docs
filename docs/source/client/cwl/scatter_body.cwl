cwlVersion: v1.0
class: Workflow

requirements:
  ScatterFeatureRequirement: {}
  SubworkflowFeatureRequirement: {}

inputs:
  dataset: string
  param_xxx:
    type: int[]
    default: [123, 456]
  param_yyy:
    type: float[]
    default: [0.456, 0.866]


outputs:
  outDS:
    type: string
    outputSource: /outDS


steps:
  parallel_work:
    run: loop_main.cwl
    scatter: [param_sliced_x, param_sliced_y]
    scatterMethod: dotproduct
    in:
      dataset: dataset
      param_sliced_x: param_xxx
      param_sliced_y: param_yyy
    out: [outDS]


  checkpoint:
    run: junction
    in:
      opt_inDS: parallel_work/outDS
      opt_exec:
        default: " echo '{\"xxx\": [345, 678], \"yyy\": [0.321, 0.567], \"to_continue\": false}' > results.json"
    out: []