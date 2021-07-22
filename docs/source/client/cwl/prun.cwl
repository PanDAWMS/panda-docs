cwlVersion: v1.0
class: CommandLineTool
baseCommand: python
stdout: cwl.output.json

inputs:
  opt_exec: string
  opt_args: string
  opt_inDS:
    type:
      - "null"
      - string
      - string[]
  opt_inDsType:
    type:
      - "null"
      - string
      - string[]
  opt_secondaryDSs:
    type:
      - "null"
      - string
      - string[]
  opt_secondaryDsTypes:
    type:
      - "null"
      - string[]
  opt_outDS: string
outputs:
  outDS:
    type:
      - "null"
      - string

arguments:
  - prefix: '-c'
    valueFrom: |
      import json, sys, shlex
      args = r""" $(inputs.opt_args) """
      items = shlex.split(args)
      if '--outputs' in items:
      	 output_str = items[items.index('--outputs') + 1]
      	 opt_outputs = output_str.split(',')
      else:
      	 opt_outputs = []
      opt_outDS = "$(inputs.opt_outDS)"
      x = {"outDS": ','.join([opt_outDS+"."+s for s in opt_outputs])}
      print(json.dumps(x))
