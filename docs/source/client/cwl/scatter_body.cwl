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
    scatter: [param_xxx, param_yyy]
    scatterMethod: dotproduct
    in:
      dataset: dataset
      param_xxx: param_xxx
      param_yyy: param_yyy
      
    out: [outDS]


  checkpoint:
    run: junction
    in:
      opt_inDS: parallel_work/outDS
      opt_exec:
        default: "echo 1"
    out: []