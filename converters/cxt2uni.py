import unicontext as unicontext

def parse_input(input_data):
    lines = input_data.strip().split('\n')

    # Vérifier que la première ligne est 'B'
    if lines[0] != 'B':
        raise ValueError("L'entrée doit commencer par la lettre 'B'.")

    # Lire le nombre d'objets et le nombre d'attributs
    num_objects = int(lines[1])
    num_attributes = int(lines[2])

    # Lire la liste des objets
    objects = lines[3:3 + num_objects]

    # Lire la liste des attributs
    attributes = lines[3 + num_objects:3 + num_objects + num_attributes]

    # Lire le tableau des relations entre objets et attributs
    relations = lines[3 + num_objects + num_attributes:]

    # Convertir les relations en une matrice binaire
    relation_matrix = [list(line.replace('.', '0').replace('X', '1')) for line in relations]

    return {
        'objects': objects,
        'attributes': attributes,
        'relation_matrix': relation_matrix
    }

# Exemple d'utilisation
input_data = """
B
8
9
fish leech
bream
frog
dog
water weeds
reed
bean
corn
needs water to live
lives in water
lives on land
needs chlorophyll
dicotyledon
monocotyledon
can move
has limbs
breast feeds
XX....X..
XX....XX.
XXX...XX.
X.X...XXX
XX.X.X...
XXXX.X...
X.XXX....
X.XX.X...
"""

parsed_data = parse_input(input_data)

result = unicontext.DataModel()
unicontext.printUniContext(result)




print("Objets:", parsed_data['objects'])
print("Attributs:", parsed_data['attributes'])
print("Matrice des relations:")
for row in parsed_data['relation_matrix']:
    print(row)