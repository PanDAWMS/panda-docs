cwlVersion: v1.0
class: Workflow

inputs: []

outputs:
  outDS:
    type: string
    outputSource: drai/outDS


steps:
  ain:
    run: prun
    in:
      opt_exec:
        default: "echo %RNDM:10 > seed_ain.txt"
      opt_args:
        default: "--outputs seed_ain.txt --avoidVP --nJobs 2"
    out: [outDS]

  twai:
    run: prun
    in:
      opt_exec:
        default: "echo %RNDM:10 > seed_twai.txt"
      opt_args:
        default: "--outputs seed_twai.txt --avoidVP --nJobs 3"
    out: [outDS]

  drai:
    run: reana
    in:
      opt_inDS:
        - ain/outDS
        - twai/outDS
      opt_exec:
        default: "echo %{DS1} %{DS2} > results.root"
      opt_args:
        default: "--outputs results.root"
      opt_containerImage:
        default: docker://busybox
    out: [outDS]
