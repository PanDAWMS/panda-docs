cwlVersion: v1.2
class: Workflow

requirements:
  InlineJavascriptRequirement: {}

inputs: []

outputs:
  outDS:
    type: string
    outputSource: main_hpo/outDS


steps:
  preproc:
    run: prun.cwl
    in:
      opt_exec:
        default: "echo %RNDM:10 > seed.txt"
      opt_args:
        default: "--outputs seed.txt --nJobs 2 --avoidVP"
    out: [outDS]

  main_hpo:
    run: phpo.cwl
    in:
      opt_trainingDS: preproc/outDS
      opt_args:
        default: "--loadJson config.json"
    out: [outDS]
    when: $(self.opt_trainingDS)
