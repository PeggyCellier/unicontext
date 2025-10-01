
import os
import sys
import p2uni
import cxt2uni
import rcft2uni

if __name__ == "__main__":
    # Vérifiez que des arguments ont été passés
    filepath = ""
    categories = False
    if len(sys.argv) == 2:
        # Le premier argument est à l'index 1 (sys.argv[0] est le nom du script)
        filepath = sys.argv[1]
    elif len(sys.argv) == 3 and sys.argv[1] == "-categories":
        filepath = sys.argv[2]
        categories = True
    else:
        raise Exception("command line arguments not recognized")
    basefilepath, file_extension = os.path.splitext(filepath)
    if file_extension == ".cxt" :
        cxt2uni.main(filepath)
    elif file_extension == ".rcft":
        rcft2uni.main(filepath)
    elif file_extension == ".p":
        p2uni.main(filepath, categories)
    else :
        print("file extension not recognized")

    