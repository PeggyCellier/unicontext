import os
import sys
import unicontext as unicontext

output = ""
def printInOutput(*text):
    global output
    for t in text :
        output += t + " "
    output += "\n"


class WrappedFC:
    def __init__(self, name, fc):
        self.name = name
        self.fc = fc

def printFormalContext(name, ctx):
    printInOutput("FormalContext", name)
    printInOutput("algo fca")
    header= "||"
    for a in ctx.attributes:
        header+=a
        header+="|"
    printInOutput(header)
    for obj, rel in ctx.incidence.items():
        line = "|" + obj + "|"
        for a in ctx.attributes:
            if a in rel:
                line+= "x|"
            else:
                line+= "|"
        printInOutput(line)

def printRelContext(name, ctx, source, target):
    printInOutput("RelationalContext", name)
    printInOutput("source", ctx.domain)
    printInOutput("target", ctx.range)
    printInOutput("scaling exist")
    header= "||"
    for o in target:
        header+=o
        header+="|"
    printInOutput(header)
    for obj in source:
        if obj in ctx.incidence.keys():
            rel = ctx.incidence[obj]
            line = "|" + obj + "|"
            for t in target:
                if t in rel:
                    line+= "x|"
                else:
                    line+= "|"
            printInOutput(line)
        else:
            line = "|" + obj + "|"
            for t in target:
                line+= "|"
            printInOutput(line)



def FormalContextsPerCategory(model):
    categoryNames = model.categories.root.keys()
    fcpc = {}
    for name, fc in model.formalContexts.root.items():
        domain = fc.domain
        wfc = WrappedFC(name, fc)
        if domain in fcpc :
            fcpc[domain].append(wfc)
        else:
            fcpc[domain] = [wfc]
    for name in categoryNames:
        if name in fcpc.keys():
            continue
        else:
            fcpc[name] = []
    return fcpc

def printCtx(model):
    wfcpc = FormalContextsPerCategory(model)
    for name, wfclist in wfcpc.items():
        if len(wfclist) == 0:
            attr = [name]
            incidence = {}
            for obj in model.categories.root[name]:
                incidence[obj] = [name]
            ctx = unicontext.FormalContext(domain=name, attributes=attr, incidence=incidence)
            printFormalContext(name, ctx)
        elif len(wfclist) == 1:
            printFormalContext(name, wfclist[0].fc)
        else:
            attr=[]
            incidence = {}
            for obj in model.categories.root[name]:
                incidence[obj] = []
            for wctx in wfclist:
                def prefix(name):
                    return wctx.name + "_" + name
                attr = attr + list(map(prefix, wctx.fc.attributes))
                for obj in model.categories.root[name]:
                    for a in wctx.fc.attributes:
                        if a in wctx.fc.incidence[obj]:
                            incidence[obj].append(prefix(a))
            ctx = unicontext.FormalContext(domain=name, attributes=attr, incidence=incidence)
            printFormalContext(name, ctx)
        printInOutput("")
    for name, ctx in model.relationalContexts.root.items():
        printRelContext(name, ctx, model.categories.root[ctx.domain], model.categories.root[ctx.range])
        printInOutput("")

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
            basefilepath, file_extension = os.path.splitext(filepath)
            if file_extension != ".json":
                print("input file should be encoded as JSON")
                return
            outputfilepath = basefilepath + ".rcft"
            with open(outputfilepath, "w") as f:
                f.write(output)
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