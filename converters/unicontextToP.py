import unicontext as unicontext



def main():
    filepath = 'data/royal.json'
    with open(filepath, 'r') as file:
        data = unicontext.DataModel.model_validate_json(file.read())
        unicontext.printUniContext(data)



if __name__ == "__main__":
    main()