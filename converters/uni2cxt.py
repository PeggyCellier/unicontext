import sys
import unicontext as unicontext

def printMatrix(objects, attributes, incidence):
    for object in objects:
        line = ""
        for attribute in attributes:
            if attribute in incidence[object]:
                line += "X"
            else :
                line += "."
        print(line)


def printCxt(model):
    print("B")
    print("")
    objects_index = next(iter(model.categories.root))
    objects = model.categories.root[objects_index]
    print(len(objects))
    fc_index = next(iter(model.formalContexts.root))
    fc = model.formalContexts.root[fc_index]
    print(len(fc.attributes))
    print("")
    for o in objects:
        print(o)
    for a in fc.attributes:
        print(a)
    printMatrix(objects, fc.attributes, fc.incidence)

def validateModel(model):
    if len(model.categories.root) == 1:
        if len(model.formalContexts.root) == 1:
            if len(model.relationalContexts.root) == 0:
                return True
            else :
                print("no relational context allowed")
                return False
        else:
            print("only one formal context allowed")
            return False
    else:
        print("only one category allowed")
        return False



def main(filepath):
    with open(filepath, 'r') as file:
        data = unicontext.DataModel.model_validate_json(file.read())
        if validateModel(data):
            printCxt(data)
        else:
            print("json context not accepted")
        


if __name__ == "__main__":
    # Vérifiez que des arguments ont été passés
    if len(sys.argv) > 1:
        # Le premier argument est à l'index 1 (sys.argv[0] est le nom du script)
        filepath = sys.argv[1]
        main(filepath)
    else:
        print("no file passed as input")