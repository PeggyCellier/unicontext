def parse_context(lines):
    headers = lines[0].split('|')[1:]
    headers = [header.strip() for header in headers]

    relations = {}
    for line in lines[1:]:
        parts = line.strip('|').split('|')
        name = parts[0].strip()
        connections = parts[1:]
        relations[name] = [headers[i+1] for i in range(len(connections)) if connections[i].strip() == 'x']
    return relations


data = """
FormalContext person
algo fca
|  |male|female|
|Jean|x     |  |
|Julie|      |x     |
|Julien|x     |      |
|Jeanne|      |x     |
|Bob|x     |      |
|Anne|      |x     |

RelationalContext love
source person
target person
scaling exist 
|  |Jean|Julie|Julien|Jeanne|Bob|Anne|
|Jean|  |x |  |  |  |  |
|Julie|  |  |x |  |  |  |
|Julien|  |  |  |x |  |  |
|Jeanne|x |  |  |  |  |  |
|Bob|  |  |  |  |  |x |
|Anne|  |  |  |  |x |  |
"""

def read_data(data):
    entries = data.strip().split('\n\n')
    for entry in entries:
        lines = entry.strip().split('\n')
        fst = lines[0].strip().split(' ')
        if fst[0] == "FormalContext":
            relations=parse_context(lines[2:])
            print(relations)
        elif fst[0] == "RelationalContext":
            relations=parse_context(lines[4:])
            print(relations)
        else:
            raise "unknown context"

read_data(data)
