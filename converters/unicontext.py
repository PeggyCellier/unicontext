
from pydantic import BaseModel, Field, RootModel
from typing import List, Dict, Union, Any

# Définir les modèles Pydantic
class Categories(RootModel):
    root:Dict[str,List[str]] = Field(default_factory=dict)

class FormalContext(BaseModel):
    domain: str = Field(default="domain")
    attributes: List[str] = Field(default_factory=list)
    incidence: Dict[str, List[str]] = Field(default_factory=dict)

class RelationalContext(BaseModel):
    domain: str = Field(default="domain")
    range: Union[str, List[str]] = Field(default_factory=list)
    incidence: Dict[str, Union[List[str], List[List[str]]]] = Field(default_factory=dict)

class FormalContexts(RootModel):
    root: Dict[str, FormalContext] = Field(default_factory=dict)

class RelationalContexts(RootModel):
    root: Dict[str, RelationalContext] = Field(default_factory=dict)

class DataModel(BaseModel):
    name: str = Field(default="name")
    categories: Categories = Field(default_factory=Categories)
    formalContexts: FormalContexts = Field(default_factory=FormalContexts)
    relationalContexts: RelationalContexts = Field(default_factory=RelationalContexts)



def printUniContext(rootcontext):     
    print("Nom:", rootcontext.name)
    print("Catégories:")
    for category, items in rootcontext.categories.root.items():
        print(f"{category}: {items}")
    print("FormalContexts:")
    for context_name, context in rootcontext.formalContexts.root.items():
        print(f"{context_name}:")
        print(f"  Domain: {context.domain}")
        print(f"  Attributes: {context.attributes}")
        print(f"  Incidence: {context.incidence}")
    print("RelationalContexts:")
    for context_name, context in rootcontext.relationalContexts.root.items():
        print(f"{context_name}:")
        print(f"  Domain: {context.domain}")
        print(f"  Range: {context.range}")
        print(f"  Incidence: {context.incidence}")

def printJson(model):
    print(model.model_dump_json(indent=2))
