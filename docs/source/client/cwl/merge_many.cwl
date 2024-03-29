cwlVersion: v1.0
class: Workflow

requirements:
  ScatterFeatureRequirement: {}
  SubworkflowFeatureRequirement: {}

inputs:
  signals: string[]
  backgrounds: string[]

outputs:
  outDS:
    type: string
    outputSource: merge/outDS


steps:
  many_sig_bg_comb:
    run: sig_bg_comb.cwl
    scatter: [signal, background]
    scatterMethod: dotproduct
    in:
      signal: signals
      background: backgrounds
    out: [outDS]

  merge:
    run: prun
    in:
      opt_inDS: many_sig_bg_comb/outDS
      opt_exec:
        default: "python merge.py --type aaa --level 3 %IN"
      opt_args:
        default: "--outputs merged.root"
    out: [outDS]
