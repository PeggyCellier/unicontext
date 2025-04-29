from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

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

# Exemple d'utilisation avec le fichier de la famille royale britannique
file_content_family = """
% British royal family
:-
Charles & William & Harry & Georges : [ male ],
Diana & Kate & Charlotte : [ female ],
William & Harry : [ parent Charles & Diana ],
Georges & Charlotte : [ parent William & Kate ].
"""

# Exemple d'utilisation avec le fichier des plats et céréales
file_content_food = """
:-
arancini : [ arancini, dish, hasMainCereal arborioRice ],
gardiane : [ gardiane, dish, hasMainCereal arborioRice & redRice ],
khaoManKai : [ khaoManKai, dish, hasMainCereal thaiRice ],
biryani : [ biryani, dish, hasMainCereal basmatiRice ],
redRice : [ redRice, cereal, rice, isProducedIn France ],
arborioRice : [ arborioRice, cereal, rice, isProducedIn Italy ],
basmatiRice : [ basmatiRice, cereal, rice, isProducedIn Pakistan ],
thaiRice : [ thaiRice, cereal, rice, isProducedIn Thailand ],
Italy : [ Italy, Europe, country ],
France : [ France, Europe, country ],
Thailand : [ Thailand, Asia, country, eatLotOf khaoManKai ],
Pakistan : [ Pakistan, Asia, country, eatLotOf biryani ]
"""

# Parser le fichier de la famille royale britannique
family_entities = parse_file(file_content_family)
print("Family Entities:")
for key, value in family_entities.root.items():
    print(key, value)

# Parser le fichier des plats et céréales
food_entities = parse_file(file_content_food)
print("\nFood Entities:")
for key, value in food_entities.root.items():
    print(key, value)
