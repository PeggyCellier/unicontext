import sys

def parse_incidence(lines):
    headers = lines[0].split('|')[1:]
    headers = [header.strip() for header in headers]

    relations = {}
    for line in lines[1:]:
        parts = line.strip('|').split('|')
        name = parts[0].strip()
        connections = parts[1:]
        relations[name] = [headers[i+1] for i in range(len(connections)) if connections[i].strip() == 'x']
    return relations


def read_data(data):
    entries = data.strip().split('\n\n')
    for entry in entries:
        lines = entry.strip().split('\n')
        fst = lines[0].strip().split(' ')
        if fst[0] == "FormalContext":
            relations=parse_incidence(lines[2:])
            print(relations)
        elif fst[0] == "RelationalContext":
            relations=parse_incidence(lines[4:])
            print(relations)
        else:
            raise "unknown context"


def main(filepath):
    with open(filepath, 'r') as file:
        data = file.read()
        read_data(data)
        

if __name__ == "__main__":
    # Vérifiez que des arguments ont été passés
    if len(sys.argv) > 1:
        # Le premier argument est à l'index 1 (sys.argv[0] est le nom du script)
        filepath = sys.argv[1]
        main(filepath)
    else:
        print("no file passed as input")