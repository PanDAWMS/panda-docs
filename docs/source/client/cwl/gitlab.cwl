cwlVersion: v1.0
class: Workflow

inputs: []

outputs:
  outDS:
    type: string
    outputSource: deux/outDS


steps:
  un:
    run: prun
    in:
      opt_exec:
        default: "echo 1 > out.txt"
      opt_args:
        default: "--outputs out.txt"
    out: [outDS]

  deux:
    run: gitlab
    in:
      opt_inDS:
        - un/outDS
      opt_site:
        default: "CERN"
      opt_ref:
        default: "master"
      opt_api:
        default: "https://gitlab.cern.ch/api/v4/projects"
      opt_projectID:
        default: "165337"
      opt_triggerToken:
        default: "MY_T_TOKEN"
      opt_accessToken:
        default: "MY_A_TOKEN"
    out: [outDS]
