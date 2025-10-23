import os
import sys
import unicontext as unicontext


output = ""
def printInOutput(*text):
    global output
    for t in text :
        output += t + " "
    output += "\n"

def printMatrix(objects, attributes, incidence):
    for object in objects:
        line = ""
        for attribute in attributes:
            if attribute in incidence[object]:
                line += "X"
            else :
                line += "."
        printInOutput(line)


def printCxt(model):
    printInOutput("B")
    printInOutput("")
    objects_index = next(iter(model.categories.root))
    objects = model.categories.root[objects_index]
    printInOutput(str(len(objects)))
    fc_index = next(iter(model.formalContexts.root))
    fc = model.formalContexts.root[fc_index]
    printInOutput(str(len(fc.attributes)))
    printInOutput("")
    for o in objects:
        printInOutput(o)
    for a in fc.attributes:
        printInOutput(a)
    printMatrix(objects, fc.attributes, fc.incidence)

# this function aims to ensure that the model is convertible to a .cxt file
def validateModel(model):
    if len(model.categories.root) == 1:
        if len(model.formalContexts.root) == 1:
            if len(model.relationalContexts.root) == 0:
                return True
            else :
                print("uni2cxt : no relational context allowed")
                return False
        else:
            print("uni2cxt : only one formal context allowed")
            return False
    else:
        print("uni2cxt : only one category allowed")
        return False

# this function aims to build a model acceptable by uni2cxt from any model
def lintModel(model):
    #first remove all relational contexts
    model.relationalContexts.root.clear()
    
    # remove all the categories but the first one
    dictionary = model.categories.root
    first_key = next(iter(dictionary))
    keys_to_remove = [key for key in dictionary if key != first_key]
    for key in keys_to_remove:
        del dictionary[key]

    # remove all formal context except a formal context which domain is the first category
    dictionary2 = model.formalContexts.root
    first_key_reach = False
    keys_to_remove = [key for key in dictionary2]
    cat = dictionary[first_key]
    for key in keys_to_remove:
        if dictionary2[key].domain == first_key and not first_key_reach:
            first_key_reach = True
        else :
            del dictionary2[key]

    # if all formal contexts have been removed, build a blank formal context
    if len(dictionary2) == 0:
        dictionary2["objects"] = unicontext.FormalContext(
            domain="objects", 
            attributes=["object"],
            incidence={key:["object"] for key in cat})
    
    # unicontext.printUniContext(model)


def main(filepath):
    with open(filepath, 'r') as file:
        data = unicontext.DataModel.model_validate_json(file.read())
        lintModel(data)
        if validateModel(data):
            printCxt(data)
            basefilepath, file_extension = os.path.splitext(filepath)
            if file_extension != ".json":
                print("uni2cxt : input file should be encoded as JSON")
                return
            outputfilepath = basefilepath + ".cxt"
            with open(outputfilepath, "w") as f:
                f.write(output)
        else:
            print("uni2cxt : json context not accepted")
        


if __name__ == "__main__":
    # Vérifiez que des arguments ont été passés
    if len(sys.argv) > 1:
        # Le premier argument est à l'index 1 (sys.argv[0] est le nom du script)
        filepath = sys.argv[1]
        main(filepath)
    else:
        print("uni2cxt : no file passed as input")