import sys
import unicontext as unicontext

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

def parse_objects(lines):
    objects = []
    for line in lines[1:]:
        parts = line.strip('|').split('|')
        name = parts[0].strip()
        objects.append(name)
    return objects

def parse_attributes(lines):
    headers = lines[0].strip('| ').split('|')
    headers = [header.strip() for header in headers]
    return headers


        
def read_formal_contexts(data):
    entries = data.strip().split('\n\n')
    fcs = {}
    for entry in entries:
        lines = entry.strip().split('\n')
        fst = lines[0].strip().split(' ')
        if fst[0] == "FormalContext":
            name = fst[1]
            attributes = parse_attributes(lines[2:])
            relations=parse_incidence(lines[2:])
            fc = unicontext.FormalContext(domain=name, attributes=attributes, incidence=relations)
            fcs[name] = fc
        elif fst[0] == "RelationalContext":
            continue
        else:
            raise "unknown context"
    formalContexts = unicontext.FormalContexts(fcs)
    return formalContexts
        

def read_categories(data):
    categories = {}
    entries = data.strip().split('\n\n')
    for entry in entries:
        lines = entry.strip().split('\n')
        fst = lines[0].strip().split(' ')
        if fst[0] == "FormalContext":
            name = fst[1]
            objects=parse_objects(lines[2:])
            categories[name] = objects
        elif fst[0] == "RelationalContext":
            continue
        else:
            raise "unknown context"
    return unicontext.Categories(categories)

def read_relational_contexts(data):
    entries = data.strip().split('\n\n')
    rcs = {}
    for entry in entries:
        lines = entry.strip().split('\n')
        fst = lines[0].strip().split(' ')
        if fst[0] == "FormalContext":
            continue
        elif fst[0] == "RelationalContext":
            snd = lines[1].strip().split(' ')
            thd = lines[2].strip().split(' ')
            name = fst[1]
            domain = snd[1]
            range = thd[1]
            relations=parse_incidence(lines[4:])
            rc = unicontext.RelationalContext(domain=domain, range=range, incidence=relations)
            rcs[name] = rc
        else:
            raise "unknown context"
    return unicontext.RelationalContexts(rcs)


def main(filepath):
    with open(filepath, 'r') as file:
        data = file.read()
        cat = read_categories(data)
        fcs = read_formal_contexts(data)
        rcs = read_relational_contexts(data)
        context = unicontext.DataModel(name="context", categories=cat, formalContexts=fcs, relationalContexts=rcs)
        unicontext.printJson(context)

if __name__ == "__main__":
    # Vérifiez que des arguments ont été passés
    if len(sys.argv) > 1:
        # Le premier argument est à l'index 1 (sys.argv[0] est le nom du script)
        filepath = sys.argv[1]
        main(filepath)
    else:
        print("no file passed as input")