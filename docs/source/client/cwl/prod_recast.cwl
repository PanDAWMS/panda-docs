cwlVersion: v1.0
class: Workflow

requirements:
  ScatterFeatureRequirement: {}
  SubworkflowFeatureRequirement: {}


inputs:
  seeds: int[]

outputs:
  outDS:
    type: string
    outputSource: recast/outDS


steps:
  prod:
    run: evnt_to_deriv_ntup.cwl
    scatter: [seed]
    scatterMethod: dotproduct
    in:
      seed: seeds
    out: [outDS]

  recast:
    run: reana
    in:
      opt_inDS: prod/outDS
      opt_exec:
        default: "echo %{DS*} > cl.root"
      opt_args:
        default: "--outputs cl.root"
    out: [outDS]