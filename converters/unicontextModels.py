
from pydantic import BaseModel, Field, RootModel
from typing import List, Dict, Union, Any

# Définir les modèles Pydantic
class Category(RootModel):
    root:Dict[str,List[str]] = Field(default_factory=dict)

class FormalContext(BaseModel):
    domain: str
    attributes: List[str]
    incidence: Dict[str, List[str]]

class RelationalContext(BaseModel):
    domain: str
    range: Union[str, List[str]]
    incidence: Dict[str, Union[List[str], List[List[str]]]]

class FormalContexts(RootModel):
    root: Dict[str, FormalContext] = Field(default_factory=dict)

class RelationalContexts(RootModel):
    root: Dict[str, RelationalContext] = Field(default_factory=dict)

class DataModel(BaseModel):
    name: str
    categories: Category
    formalContexts: FormalContexts = Field(default_factory=FormalContexts)
    relationalContexts: RelationalContexts = Field(default_factory=RelationalContext)