import sys

with open(sys.argv[1]) as f:
    is_spec = False
    is_yaml = False
    endpoint = None
    for line in f:
        if line.startswith('@rest_api'):
            is_spec = True
            continue
        if is_spec:
            if line.startswith('def '):
                endpoint = line.split()[1]
                endpoint = endpoint.split('(')[0]
                print(f'  /{endpoint}:')
                continue
            if is_spec and '"""' in line:
                is_yaml = not is_yaml
                if not is_yaml:
                    is_spec = False
                continue
            if is_yaml:
                sys.stdout.write(line)
