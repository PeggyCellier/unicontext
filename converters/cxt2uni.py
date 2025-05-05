import sys
import unicontext as unicontext

def parse_input(input_data):
    lines = input_data.strip().split('\n')

    # Vérifier que la première ligne est 'B'
    if lines[0] != 'B':
        raise ValueError("L'entrée doit commencer par la lettre 'B'.")

    # Lire le nombre d'objets et le nombre d'attributs
    num_objects = int(lines[2])
    num_attributes = int(lines[3])

    # Lire la liste des objets
    objects = lines[5:5 + num_objects]

    # Lire la liste des attributs
    attributes = lines[5 + num_objects:5 + num_objects + num_attributes]

    # Lire le tableau des relations entre objets et attributs
    relations = lines[5 + num_objects + num_attributes:]

    # Convertir les relations en une matrice binaire
    relation_matrix = [list(line.replace('.', '0').replace('X', '1')) for line in relations]

    # Créer la liste des attributs par objet
    incidence1 = []
    for i in range(num_objects):
        obj_attributes = [attributes[j] for j in range(num_attributes) if relation_matrix[i][j] == '1']
        incidence1.append(obj_attributes)

    # classe le resultat dans un dictionnaire indexé par objet
    incidence2 = {}
    for i, obj_attributes in enumerate(incidence1):
        incidence2[objects[i]] = obj_attributes

    cat= unicontext.Categories(root={"objects": objects})
    formalContext = unicontext.FormalContext(domain="objects", attributes=attributes, incidence=incidence2)
    result = unicontext.DataModel(name="context", categories=cat, formalContexts={"formalContext":formalContext})

    return result


def main(filepath):
    with open(filepath, 'r') as file:
        parsed_data = parse_input(file.read())
        unicontext.printJson(parsed_data)


if __name__ == "__main__":
    # Vérifiez que des arguments ont été passés
    if len(sys.argv) > 1:
        # Le premier argument est à l'index 1 (sys.argv[0] est le nom du script)
        filepath = sys.argv[1]
        main(filepath)
    else:
        print("no file passed as input")