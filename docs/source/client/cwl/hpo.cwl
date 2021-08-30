cwlVersion: v1.0
class: Workflow

inputs: []

outputs:
  outDS:
    type: string
    outputSource: post_proc/outDS


steps:
  pre_proc:
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
      opt_trainingDS: pre_proc/outDS
      opt_args:
        default: "--loadJson conf.json"
    out: [outDS]
    when: $(self.opt_trainingDS)

  post_proc:
    run: prun.cwl
    in:
      opt_inDS: main_hpo/outDS
      opt_exec:
        default: "echo %IN > anal.txt"
      opt_args:
        default: "--outputs anal.txt --nFilesPerJob 100 --avoidVP"
    out: [outDS]
    when: $(self.opt_inDS)
