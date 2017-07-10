import math
from numpy import *
from os import walk
from scipy.sparse.linalg import svds


def split():
    mypath = "AllBooksShort"
    f = []
    for(dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        break
    return f


def IDF(A, n):
    for j in range(len(A[0])):
        nw = 0
        for i in range(len(A)):
            if A[i][j] != 0:
                nw += 1
        for i in range(len(A)):
            if nw != 0:
                A[i][j] = A[i][j] * math.log(n/nw, 10)
            else:
                A[i][j] = A[i][j]
    return A


def multiply(v, m):
    RES = []
    for j in range(len(m)):
        RES.append(0)
        for i in range(len(v)):
            RES[j] += v[i] * m[j][i]
        RES[j] = abs(RES[j])
    return RES


def normalization(v):
    sum = 0
    for i in range(len(v)):
        sum += v[i] * v[i]
    for i in range(len(v)):
        v[i] = (v[i] * v[i] / sum)**(1/2)
    return v


def find(A, number_of_docs, files, q):
    A_normalized = []
    q_normalized = normalization(q)
    for i in range(len(A)):
       A_normalized.append(normalization(A[i]))

    res = multiply(q_normalized, A_normalized)
    s = sorted(range(len(res)), key=lambda k: res[k], reverse=True)
    for i in range(number_of_docs):
        print(files[s[i]])


def find_SVD(A, number_of_docs, files, q):
    k = 500

    U, S, Vt = svds(A, k, which='LM')  # rozklad SVD
    S = S[::-1]
    S = diag(S)
    Ak = dot(U, dot(S, Vt))


    Ak_normalized = []
    q_normalized = normalization(q)
    for i in range(len(Ak)):
        Ak_normalized.append(normalization(Ak[i]))

    res = multiply(q_normalized, Ak_normalized)
    s = sorted(range(len(res)), key=lambda k: res[k], reverse=True)
    for i in range(number_of_docs):
        print(files[s[i]])


def main():
    words = {};
    A = []
    it = 0
    n = 1000
    number_of_docs = 5

    files = split()
    files = files[:n]

    for file in files:
        with open("AllBooksShort/" + file, "r") as f:
            text = f.readlines()
            parsed = []
            for line in text:
                parsed.append(line.replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").replace(";", " ").replace(":", " ").split())
            parsed = [item.lower() for sublist in parsed for item in sublist]
            for word in parsed:
                if word not in words.keys():
                    words[word] = [it, 1]
                    it += 1
                else:
                    words[word][1] += 1


    for file in files:
        bag_of_words = []
        for j in range(len(words)):
            bag_of_words.append(0)
        with open("AllBooksShort/" + file, "r") as f:
            text = f.readlines()
            parsed = []
            for line in text:
                parsed.append(line.replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").replace(";", " ").replace(":"," ").split())
            parsed = [item.lower() for sublist in parsed for item in sublist]
            for word in parsed:
                bag_of_words[words[word][0]] += 1
        A.append(bag_of_words)



    words_to_search = input("Enter the words to search: ")
    q = []
    words_to_search = words_to_search.split()
    for word in words:
        q.append(0)
    for word in words_to_search:
        if(word in words.keys()):
            q[words[word][0]] += 1

    A = IDF(A, n)

    #find(A, number_of_docs, files, q)
    print()
    find_SVD(A, number_of_docs, files, q)

main()