
import sys
import uni2p
import uni2cxt
import uni2rcft

if __name__ == "__main__":
    # Vérifiez que des arguments ont été passés
    if len(sys.argv) > 1:
        # Le premier argument est à l'index 1 (sys.argv[0] est le nom du script)
        filepath = sys.argv[1]
        uni2p.main(filepath)
        uni2rcft.main(filepath)
        uni2cxt.main(filepath)
    else:
        print("no file passed as input")