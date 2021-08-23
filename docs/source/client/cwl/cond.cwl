cwlVersion: v1.2
class: Workflow

requirements:
  InlineJavascriptRequirement: {}

inputs: []

outputs:
  outDS_OK:
    type: string
    outputSource: bottom_OK/outDS
  outDS_NG:
    type: string
    outputSource: bottom_NG/outDS


steps:
  top:
    run: prun.cwl
    in:
      opt_exec:
        default: "echo %RNDM:10 > seed.txt"
      opt_args:
        default: "--outputs seed.txt --nJobs 2"
    out: [outDS]

  bottom_OK:
    run: prun.cwl
    in:
      opt_inDS: top/outDS
      opt_exec:
        default: "echo %IN > results.txt"
      opt_args:
        default: "--outputs results.txt --forceStaged"
    out: [outDS]
    when: $(self.opt_inDS)

  bottom_NG:
    run: prun.cwl
    in:
      opt_inDS: top/outDS
      opt_exec:
        default: "echo hard luck > bad.txt"
      opt_args:
        default: "--outputs bad.txt"
    out: [outDS]
    when: $(!self.opt_inDS)
 
