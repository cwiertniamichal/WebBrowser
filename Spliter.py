from os import walk

def split():
    mypath = "AllBooks"
    f = []
    for(dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        break
    return f

def main():
    size = 10000
    files = split()
    for file in files:
        it = 0
        with open("AllBooks/" + file, "r", errors='ignore') as f:
            while( True ):
                lines = f.readlines(size)
                if not lines:
                    break
                with open("AllBooksShort/" + file + "_short_" + str(it) + ".txt", "w") as fw:
                    for word in lines:
                        fw.write(word)
                    it += 1

main()