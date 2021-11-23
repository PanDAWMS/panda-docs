cwlVersion: v1.0
class: Workflow

inputs:
  dataset:
    type: string
  param_xxx:
    type: int
    default: 123
  param_yyy:
    type: float
    default: 0.456

outputs:
  outDS:
    type: string
    outputSource: inner_work_bottom/outDS


steps:
  inner_work_top:
    run: prun
    in:
      opt_inDS: dataset
      opt_exec:
        default: "echo %IN %{xxx} %{i} > seed.txt"
      opt_args:
        default: "--outputs seed.txt --avoidVP"
    out: [outDS]

  inner_work_bottom:
    run: prun
    in:
      opt_inDS: inner_work_top/outDS
      opt_exec:
        default: "echo %IN %{yyy} > results.root"
      opt_args:
        default: "--outputs results.root --forceStaged"
    out: [outDS]


  checkpoint:
    run: junction
    in:
      opt_inDS:
        - inner_work_top/outDS
        - inner_work_bottom/outDS
      opt_exec:
        default: "echo %{DS0} %{DS1} aaaa; echo '{\"x\": 456, \"to_terminate\": true}' > results.json"
    out: []
