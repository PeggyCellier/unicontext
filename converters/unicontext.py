
import sys
import os
from pydantic import BaseModel, Field
from typing import List, Dict
import json
import unicontextModels

def parseUniContext(filepath):
    with open(filepath, 'r') as file:
        data = unicontextModels.DataModel.model_validate_json(file.read())
        return data

def printUniContext(model):
        print("Nom:", model.name)
        print("Catégories:")
        for category, items in model.categories.root.items():
            print(f"{category}: {items}")
        print("FormalContexts:")
        for context_name, context in model.formalContexts.root.items():
            print(f"{context_name}:")
            print(f"  Domain: {context.domain}")
            print(f"  Attributes: {context.attributes}")
            print(f"  Incidence: {context.incidence}")
        print("RelationalContexts:")
        for context_name, context in model.relationalContexts.root.items():
            print(f"{context_name}:")
            print(f"  Domain: {context.domain}")
            print(f"  Range: {context.range}")
            print(f"  Incidence: {context.incidence}")

def dump_model(model):
    print(model.model_dump_json(indent=2))


def main():
    m = parseUniContext('data/royal.json')
    dump_model(m)

if __name__ == "__main__":
    main()