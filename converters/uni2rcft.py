import sys
import unicontext as unicontext


def printFormalContext(name, ctx):
    print("FormalContext", name)
    print("algo fca")
    header= "||"
    for a in ctx.attributes:
        header+=a
        header+="|"
    print(header)
    for obj, rel in ctx.incidence.items():
        line = "|" + obj + "|"
        for a in ctx.attributes:
            if a in rel:
                line+= "x|"
            else:
                line+= "|"
        print(line)

def printRelContext(name, ctx, source, target):
    print("RelationalContext", name)
    print("source", ctx.domain)
    print("target", ctx.range)
    print("scaling exist")
    header= "||"
    for o in target:
        header+=o
        header+="|"
    print(header)
    for obj in source:
        rel = ctx.incidence[obj]
        line = "|" + obj + "|"
        for t in target:
            if t in rel:
                line+= "x|"
            else:
                line+= "|"
        print(line)


def printCtx(model):
    for name, ctx in model.formalContexts.root.items():
        printFormalContext(name, ctx)
        print("")
    for name, ctx in model.relationalContexts.root.items():
        printRelContext(name, ctx, model.categories.root[ctx.domain], model.categories.root[ctx.range])
        print("")

def validateModel(model):
    for name, ctx in model.relationalContexts.root.items():
        if isinstance(ctx.range, list):
            print("n-ary relational context with n>=3 not allowed")
            return False
    return True


def main(filepath):
    with open(filepath, 'r') as file:
        data = unicontext.DataModel.model_validate_json(file.read())
        if validateModel(data):
            printCtx(data)
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