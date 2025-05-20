import sys
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import unicontext as unicontext

class Entity(BaseModel):
    attributes: List[List[str]] = Field(default_factory=list)

class Entities(BaseModel):
    root: Dict[str, Entity] = Field(default_factory=dict)

def parse_file(file_content):
    lines = file_content.strip().split('\n')
    ent = Entities()

    for line in lines:
        line = line.strip()
        if line.startswith('%') or line == ':-':
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

def computeUni(entities):
    category = []
    attributes = []
    incidenceAttr = {}
    for obj, entity in entities.root.items():
        category.append(obj)
        incidenceAttr[obj] = []
        for item in entity.attributes:
            if len(item) == 1:
                if not item[0] in attributes:
                    attributes.append(item[0])
                if not item[0] in incidenceAttr[obj] :
                    incidenceAttr[obj].append(item[0])
    categories = unicontext.Categories(root={"objects":category})
    fc = unicontext.FormalContext(domain="objects", attributes=attributes, incidence=incidenceAttr)
    fcs = unicontext.FormalContexts(root={"formalContext":fc})
    model = unicontext.DataModel(name="context", categories=categories, formalContexts=fcs)
    unicontext.printUniContext(model)

def printEntities(entities):
    for obj, relations in entities.root.items():
        print(obj, relations)

def main(filepath):
    with open(filepath, 'r') as file:
        entities = parse_file(file.read())
        #printEntities(entities)
        computeUni(entities)


if __name__ == "__main__":
    # Vérifiez que des arguments ont été passés
    if len(sys.argv) > 1:
        # Le premier argument est à l'index 1 (sys.argv[0] est le nom du script)
        filepath = sys.argv[1]
        main(filepath)
    else:
        print("no file passed as input")