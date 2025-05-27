import sys
import re
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import unicontext as unicontext

class Entity(BaseModel):
    attributes: List[List[str]] = Field(default_factory=list)

class Entities(BaseModel):
    root: Dict[str, Entity] = Field(default_factory=dict)

def validate_oneRule(file_content):
    def rule_search(string, substring):
        occurrences = []
        index = 0
        while True:
            index = string.find(substring, index)
            if index == -1:
                break
            occurrences.append(index)
            index += 1 
        return occurrences
    occurences = rule_search(file_content, ":-")
    if len(occurences) != 1 :
        print("file should contain one rule exactly")
        raise "file should contain one rule exactly"
    
def validate_noHead(file_content):
    head, body = file_content.split(":-")
    lines = head.strip().split('\n')
    for line in lines :
        if line.startswith('%') or line == "":
            continue
        else:
            print("rule should not have head")
            raise "rule should not have head"

def validate_wellFormated(file_content):
    head, body = file_content.split(":-")
    lines = body.strip().split('\n')
    for line in lines:
        if line == ".":
            return
        line = line.strip()
        name, details = line.split(':')
        pattern = r'\[\s*([\w\s,]+)\s*,?\s*\]'
        match = re.match(pattern, details.strip())
        if not match:
            print("details are not well formatted")
            raise "details are not well formatted"

def parse_file(file_content):
    lines = file_content.strip().split('\n')
    ent = Entities()

    for line in lines:
        line = line.strip()
        if line.startswith('%') or line == ':-' or line.startswith('.'):
            continue

        name, details = line.split(':')
        name = name.strip()
        details = details.strip(' [],.').split(',')
        names = name.split('&')
        def strip(name):
            return name.strip()
        names = map(strip, names)


        def appendDetail(name, entity, detail):
            detail = detail.strip()
            if ' ' in detail:
                pred, value = detail.split(' ', 1)
                value = value.strip()
                if '&' in value:
                    values = value.split('&')
                    for v in values :
                        entity.attributes.append([pred, v.strip()])
                else:
                    if ' ' in value:
                        entity.attributes.append([pred] + value.split(' '))
                    else:
                        entity.attributes.append([pred, value])
            else:
                entity.attributes.append([detail])
            ent.root[name] = entity

        def getEntity(name):
            return ent.root.get(name, Entity())

        for name in names:
            entity = getEntity(name)
            for detail in details:
                appendDetail(name, entity, detail)
    return ent

def incidenceLength(incidence):
    key = next(iter(incidence))
    example_relation = incidence[key]
    rel = example_relation[0]
    if isinstance(rel, str):
        return 1
    else : #rel is a list
        return len(rel)

def computeUni(entities):
    category = []
    attributes = []
    incidenceAttr = {}
    incidenceObj = {}
    for obj, entity in entities.root.items():
        category.append(obj)
        incidenceAttr[obj] = []
        for item in entity.attributes:
            if len(item) == 1:
                if not item[0] in attributes:
                    attributes.append(item[0])
                if not item[0] in incidenceAttr[obj] :
                    incidenceAttr[obj].append(item[0])
            elif len(item) == 2:
                if not item[0] in incidenceObj.keys():
                    incidenceObj[item[0]] = {}
                if not obj in incidenceObj[item[0]].keys():
                    incidenceObj[item[0]][obj] = []
                incidenceObj[item[0]][obj].append(item[1])
            else : #len(item) >= 3
                if not item[0] in incidenceObj.keys():
                    incidenceObj[item[0]] = {}
                if not obj in incidenceObj[item[0]].keys():
                    incidenceObj[item[0]][obj] = []
                incidenceObj[item[0]][obj].append(item[1:])
    categories = unicontext.Categories(root={"objects":category})
    fc = unicontext.FormalContext(domain="objects", attributes=attributes, incidence=incidenceAttr)
    fcs = unicontext.FormalContexts(root={"formalContext":fc})
    rcs_dict = {}
    for key, value in incidenceObj.items():
        length = incidenceLength(value)
        if length == 1:
            rcs_dict[key] = unicontext.RelationalContext(domain="objects", range="objects", incidence=value)
        else : #length >= 2
            range = ["objects"] * length
            rcs_dict[key] = unicontext.RelationalContext(domain="objects", range=range, incidence=value)
    rcs = unicontext.RelationalContexts(root=rcs_dict)
    model = unicontext.DataModel(name="context", categories=categories, formalContexts=fcs, relationalContexts=rcs)
    return model

def printEntities(entities):
    for obj, relations in entities.root.items():
        print(obj, relations)

def main(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
        try:
            validate_oneRule(content)
            validate_noHead(content)
            validate_wellFormated(content)
        except Exception as e:
            print(e.message, e.args)
            print("file has incorrect format")
            return
        entities = parse_file(content)
        #printEntities(entities)
        model = computeUni(entities)
        unicontext.printJson(model)


if __name__ == "__main__":
    # Vérifiez que des arguments ont été passés
    if len(sys.argv) > 1:
        # Le premier argument est à l'index 1 (sys.argv[0] est le nom du script)
        filepath = sys.argv[1]
        main(filepath)
    else:
        print("no file passed as input")