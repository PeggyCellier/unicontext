
import sys
import os
from pydantic import BaseModel, Field
from typing import List, Dict
import json
import unicontextModels



def printUniContext(filepath):
    with open(filepath, 'r') as file:
        data_1 = unicontextModels.DataModel.model_validate_json(file.read())
        
        print("Nom:", data_1.name)
        print("Catégories:")
        for category, items in data_1.categories.root.items():
            print(f"{category}: {items}")
        print("FormalContexts:")
        for context_name, context in data_1.formalContexts.root.items():
            print(f"{context_name}:")
            print(f"  Domain: {context.domain}")
            print(f"  Attributes: {context.attributes}")
            print(f"  Incidence: {context.incidence}")
        print("RelationalContexts:")
        for context_name, context in data_1.relationalContexts.root.items():
            print(f"{context_name}:")
            print(f"  Domain: {context.domain}")
            print(f"  Range: {context.range}")
            print(f"  Incidence: {context.incidence}")

def main():
    printUniContext('data/royal.json')

if __name__ == "__main__":
    main()