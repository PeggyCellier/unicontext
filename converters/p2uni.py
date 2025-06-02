import sys
import re
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import unicontext as unicontext

class Entity(BaseModel):
    relations: List[List[str]] = Field(default_factory=list)

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
        raise BaseException("file should contain one rule exactly")
    
def validate_noHead(file_content):
    head, body = file_content.split(":-")
    lines = head.strip().split('\n')
    for line in lines :
        if line.startswith('%') or line == "":
            continue
        else:
            raise BaseException("rule should not have head")

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
            raise BaseException("details are not well formatted")

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
                        entity.relations.append([pred, v.strip()])
                else:
                    if ' ' in value:
                        entity.relations.append([pred] + value.split(' '))
                    else:
                        entity.relations.append([pred, value])
            else:
                entity.relations.append([detail])
            ent.root[name] = entity

        def getEntity(name):
            return ent.root.get(name, Entity())

        for name in names:
            entity = getEntity(name)
            for detail in details:
                appendDetail(name, entity, detail)
    return ent

def computeCategoryMapping(entities):
    catMapping = {}
    for obj, entity in entities.root.items():
        fstRel = entity.relations[0]
        if len(fstRel) != 1:
            raise "first relation of object should be its category"
        else:
            catMapping[obj] = fstRel[0]
    return catMapping

def computeDumbCategoryMapping(entities):
    catMapping = {}
    for obj, entity in entities.root.items():
        catMapping[obj] = "objects"
    return catMapping

def computeCategories(catMapping):
    categories = {}
    for obj, cat in catMapping.items():
        if not cat in categories.keys():
            categories[cat] = []
        categories[cat].append(obj)
    return categories

def isFCempty(fc):
    for obj, attrs in fc.incidence.items():
        if len(attrs) > 0:
            return False
    return True

def computeFCs(entities, catMapping, categories):
    headerAttr = {}
    incidenceAttr = {}
    for cat in categories.keys():
        incidenceAttr[cat] = {}
        headerAttr[cat] = []
    for obj, entity in entities.root.items():
        cat = catMapping[obj]
        for item in entity.relations:
            if len(item) == 1:
                if not item[0] in headerAttr[cat] and item[0] != cat:
                    headerAttr[cat].append(item[0])
                if not obj in incidenceAttr[cat].keys():
                    incidenceAttr[cat][obj] = []
                if not item[0] in incidenceAttr[cat][obj] and item[0] != cat :
                    incidenceAttr[cat][obj].append(item[0])
    fc_dict = {}
    for name, incidence in incidenceAttr.items():
        fc = unicontext.FormalContext(domain=name, attributes=headerAttr[name], incidence=incidence)
        if not isFCempty(fc):
            fc_dict[name] = fc
    fcs = unicontext.FormalContexts(root=fc_dict)
    return fcs

def incidenceLength(incidence):
    key = next(iter(incidence))
    example_relation = incidence[key]
    rel = example_relation[0]
    if isinstance(rel, str):
        return 1
    else : #rel is a list
        return len(rel)

def getIncidenceDomain(incidence, catMapping):
    key = next(iter(incidence))
    return catMapping[key]

def getIncidenceRange(incidence, catMapping):
    def catMap(obj):
        return catMapping[obj]
    key = next(iter(incidence))
    example_relation = incidence[key]
    rel = example_relation[0]
    if isinstance(rel, str):
        return catMapping[rel]
    else : #rel is a list
        return list(map(catMap, rel))

def computeRCs(entities, catMapping, categories):
    incidenceObj = {}
    for obj, entity in entities.root.items():
        for item in entity.relations:
            if len(item) == 2:
                if not item[0] in incidenceObj.keys():
                    incidenceObj[item[0]] = {}
                if not obj in incidenceObj[item[0]].keys():
                    incidenceObj[item[0]][obj] = []
                incidenceObj[item[0]][obj].append(item[1])
            if len(item) >= 3 :
                if not item[0] in incidenceObj.keys():
                    incidenceObj[item[0]] = {}
                if not obj in incidenceObj[item[0]].keys():
                    incidenceObj[item[0]][obj] = []
                incidenceObj[item[0]][obj].append(item[1:])
    rcs_dict = {}
    for key, value in incidenceObj.items():
        domain = getIncidenceDomain(value, catMapping)
        range = getIncidenceRange(value, catMapping)
        rcs_dict[key] = unicontext.RelationalContext(domain=domain, range=range, incidence=value)
    rcs = unicontext.RelationalContexts(root=rcs_dict)
    return rcs

def computeUni(entities, catMapping):
    categories = computeCategories(catMapping)
    fcs = computeFCs(entities, catMapping, categories)
    rcs = computeRCs(entities, catMapping, categories)
    cats = unicontext.Categories(root=categories)
    model = unicontext.DataModel(name="context", categories=cats, formalContexts=fcs, relationalContexts=rcs)
    return model

def printEntities(entities):
    for obj, relations in entities.root.items():
        print(obj, relations)

def main(filepath, computeCategories):
    with open(filepath, 'r') as file:
        content = file.read()
        try:
            validate_oneRule(content)
            validate_noHead(content)
            validate_wellFormated(content)
            entities = parse_file(content)
            #printEntities(entities)
            catMapping = {}
            if computeCategories :
                catMapping = computeCategoryMapping(entities)
            else :
                catMapping = computeDumbCategoryMapping(entities)
            #print(catMapping)
            model = computeUni(entities, catMapping)
            unicontext.printJson(model)
        except BaseException as e:
            print(e)
            print("file has incorrect format")
            return


if __name__ == "__main__":
    # Vérifiez que des arguments ont été passés
    if len(sys.argv) == 2:
        # Le premier argument est à l'index 1 (sys.argv[0] est le nom du script)
        filepath = sys.argv[1]
        main(filepath, False)
    elif len(sys.argv) == 3 and sys.argv[1] == "-categories":
        filepath = sys.argv[2]
        main(filepath, True)
    else:
        print("command line arguments not recognized")