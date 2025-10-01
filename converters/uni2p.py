import os
import sys
import unicontext as unicontext

output = ""
def printInOutput(*text):
    global output
    for t in text :
        output += t + " "
    output += "\n"

def stringify(l):
    if isinstance(l, str):
        return l
    elif isinstance(l, list):
        s=""
        if len(l) == 0:
            return s
        elif len(l) == 1:
            return l[0]
        else:
            s += l[0]
            for item in l[1:]:
                s+= (" " + item)
            return s
    else:
        print("unrecognized incidence")

def computePformat(model):
    categories = {}
    for name, c in model.categories.root.items():
        categories[name] = {element: [] for element in c}
    for name, fc in model.formalContexts.root.items():
        for obj, attr in fc.incidence.items():
            categories[fc.domain][obj] += attr
    for name, rc in model.relationalContexts.root.items():
        def prefixAndStringify(l):
            return name + " " + stringify(l)
        for obj, rel in rc.incidence.items():
            categories[rc.domain][obj] += list(map(prefixAndStringify, rel))
    return categories

def printPformat(name, categories):
    printInOutput("%", name)
    printInOutput(":-")
    for name, cat in categories.items():
        for obj, rel in cat.items():
            incidence = "[ " + name 
            for item in rel:
                incidence += ", " + item
            incidence += " ]"
            if name == list(categories)[-1] and obj == list(cat)[-1]:
                printInOutput(obj, ":", incidence)
            else:
                printInOutput(obj, ":", incidence, ",")
    printInOutput(".")


def main(filepath):
    with open(filepath, 'r') as file:
        data = unicontext.DataModel.model_validate_json(file.read())
        categories = computePformat(data)
        printPformat(data.name, categories)
        basefilepath, file_extension = os.path.splitext(filepath)
        if file_extension != ".json":
            print("input file should be encoded as JSON")
            return
        outputfilepath = basefilepath + ".p"
        with open(outputfilepath, "w") as f:
            f.write(output)

if __name__ == "__main__":
    # Vérifiez que des arguments ont été passés
    if len(sys.argv) > 1:
        # Le premier argument est à l'index 1 (sys.argv[0] est le nom du script)
        filepath = sys.argv[1]
        main(filepath)
    else:
        print("no file passed as input")