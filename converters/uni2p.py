import sys
import unicontext as unicontext



def printCtx(data):
    unicontext.printUniContext(data)


def main(filepath):
    with open(filepath, 'r') as file:
        data = unicontext.DataModel.model_validate_json(file.read())
        printCtx(data)


if __name__ == "__main__":
    # Vérifiez que des arguments ont été passés
    if len(sys.argv) > 1:
        # Le premier argument est à l'index 1 (sys.argv[0] est le nom du script)
        filepath = sys.argv[1]
        main(filepath)
    else:
        print("no file passed as input")