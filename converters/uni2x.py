
import sys
import uni2p
import uni2cxt
import uni2rcft

if __name__ == "__main__":
    # verify that command has one argument
    if len(sys.argv) > 1:
        #  (sys.argv[0] is the name of the script) filepath is sys.argv[1]
        filepath = sys.argv[1]
        uni2p.main(filepath)
        uni2rcft.main(filepath)
        # warning : only unicontext object without relational data are accepted by uni2cxt
        # therefore uni2cxt will rebuild a context without relational data and with only one category
        # and one formal context from your context
        uni2cxt.main(filepath)
    else:
        print("no file passed as input")