cwlVersion: v1.0
class: Workflow

requirements:
  ScatterFeatureRequirement: {}
  SubworkflowFeatureRequirement: {}

inputs:
  signal: string

outputs:
  outDS:
    type: string
    outputSource: seq_loop/outDS


steps:
  seq_loop:
    run: scatter_body.cwl
    in:
      dataset: signal
    out: [outDS]
    hints:
      - loop
