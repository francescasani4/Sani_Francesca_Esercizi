from itertools import combinations
import random
import timeit
import matplotlib.pyplot as plt
import string
import numpy as np

nrIterazioniTest = 100

maxLength = 13 # Dimensione massima delle sequenze generate

# Array per salvare i tempi e le dimensioni delle sequenze generate
BruteForce = []
Recursive = []
Memoization = []
BottomUp = []
length = []

# Algoritmo Forza-Bruta
def lcs_bruteForce(s1, s2):
    substrings = allSubsequences(s1)
    lenght = 0

    for i in range(len(substrings)):
        sub = substrings[i]
        index = -1
        maxL = 0

        for j in range(len(sub)):
            found = False

            for k in range(len(s2)):
                if sub[j] == s2[k] and index < k and found == False:
                    maxL += 1
                    index = k
                    found = True

        if maxL > lenght:
            lenght = maxL

    return lenght

def allSubsequences(s):
    out = set()

    for r in range(1, len(s) + 1):
        for c in combinations(s, r):
            out.add(''.join(c))

    return sorted(out)

# Algoritmo Ricorsivo
def lcs_recursive(s1, s2):
    m = len(s1) - 1
    n = len(s2) - 1

    lenght = recursive(s1, s2, m, n)

    return lenght

def recursive(s1, s2, m, n):
    if m < 0 or n < 0:
        return 0
    elif s1[m] == s2[n]:
        return 1 + recursive(s1, s2, m - 1, n - 1)
    else:
        return max(recursive(s1, s2, m, n - 1), recursive(s1, s2, m - 1, n))

# Algoritmo Ricorsivo con Memoization
def lcs_memoization(s1, s2):
    m = len(s1)
    n = len(s2)

    c = [[0 for x in range(m + 1)] for y in range(n + 1)]
    lenght = memoization(s1, s2, c, m, n)

    return lenght

def memoization(s1, s2, c, m, n):
    if c[m][n] != 0:
        return c[m][n]
    elif m <= 0 or n <= 0:
        return 0
    elif s1[m - 1] == s2[n - 1]:
        c[m][n] = 1 + memoization(s1, s2, c, m - 1, n - 1)
        return c[m][n]
    else:
        c[m][n] = max(memoization(s1, s2, c, m, n - 1), memoization(s1, s2, c, m - 1, n))
        return c[m][n]

# Algoritmo Bottom-Up

def lcs_bottomUp(s1, s2):
    m = len(s1)
    n = len(s2)

    c = [[0 for x in range(m + 1)] for y in range(n + 1)]

    for i in range(1, m + 1):
        c[i][0] = 0
    for j in range(1, n + 1):
        c[0][j] = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
            else:
                c[i][j] = c[i][j - 1]

    lenght = c[m][n]

    return lenght

# Funzione per generare sequenze
def stringGenerator(length):
    sequence = ""
    for x in range(length):
        sequence = ("".join(random.choice(string.ascii_uppercase)for _ in range(length)))
    return sequence

# Funzione per calcolare i tempi medi
def measureTime(function, s1, s2):
    """ Ritorna il tempo di esecuzione medio (in millisecondi) della funzione data"""
    return timeit.timeit(stmt=lambda : function(s1, s2), number=nrIterazioniTest) / nrIterazioniTest * 1000

# Funzione per generare il grafico
def drawPlots():
    plt.plot(length, BruteForce, label="Forza-Bruta", color="blue")
    plt.plot(length, Recursive, label="Ricorsiva", color="green")
    plt.plot(length, Memoization, label="Memoization", color="red")
    plt.plot(length, BottomUp, label="Bottom-Up", color="orange")

    plt.xlabel("Dimensioni dell'array")
    plt.ylabel("Tempo di esecuzione (ms)")

    plt.title("Confronto tra gli algoritmi per calcolare la LCS")
    plt.legend()

    plt.savefig("./plot/GraficoLCS.png")
    plt.show()

# Funzione per generare la tabella
def drawTable(columns: list, headers: tuple, title: str):
    fig, ax = plt.subplots(figsize=(10, 6))

    data = np.stack(tuple(columns), axis=1)

    ax.axis('off')
    table = ax.table(cellText=data, colLabels=headers, loc='center', cellLoc='center')
    table.auto_set_column_width(col=list(range(len(columns))))
    table.scale(1, 1.5)

    for cell in table._cells:
        if table[cell].get_text().get_text() in headers:
            table[cell].set_facecolor("#e0ebd4")
            table[cell].set_text_props(weight='bold')
        elif cell[0] % 2 == 0:
            table[cell].set_facecolor("#e0ebd4")

    fig.savefig("./table/TabellaLCS.png", bbox_inches='tight')

# Funzione di test
def test():
    # Misurazione dei tempi di esecuzione
    for i in range(1, maxLength):
        s1 = stringGenerator(i)
        s2 = stringGenerator(i)
        print("Sequenze generate: ", s1, "  ", s2)
        print("\n")

        length.append(i)

        BruteForce.append(measureTime(lcs_bruteForce, s1, s2))

        Recursive.append(measureTime(lcs_recursive, s1, s2))

        Memoization.append(measureTime(lcs_memoization, s1, s2))

        BottomUp.append(measureTime(lcs_bottomUp, s1, s2))

    print(BruteForce)
    print(Recursive)
    print(Memoization)
    print(BottomUp)

    #Generazione dei singoli grafici

    # Forza-Bruta
    plt.plot(length, BruteForce, color="blue")
    plt.xlabel("Dimensioni dell'array")
    plt.ylabel("Tempo di esecuzione (ms)")
    plt.title("Versione Forza-Bruta")
    plt.savefig("./plot/Forza-Bruta.png")
    plt.show()

    # Ricorsivo
    plt.plot(length, Recursive, color="green")
    plt.xlabel("Dimensioni dell'array")
    plt.ylabel("Tempo di esecuzione (ms)")
    plt.title("Versione Ricorsiva")
    plt.savefig("./plot/Ricorsiva.png")
    plt.show()

    # Ricorsivo con Memoization
    plt.plot(length, Memoization, color="red")
    plt.xlabel("Dimensioni dell'array")
    plt.ylabel("Tempo di esecuzione (ms)")
    plt.title("Versione Ricorsiva con Memoization")
    plt.savefig("./plot/Memoization.png")
    plt.show()

    # Bottom-Up
    plt.plot(length, BottomUp, color="orange")
    plt.xlabel("Dimensioni dell'array")
    plt.ylabel("Tempo di esecuzione (ms)")
    plt.title("Versione Bottom-Up")
    plt.savefig("./plot/Bottom-Up.png")
    plt.show()

    drawPlots()

    # Generazione della tabella con i tempi
    drawTable([[i for i in range(1, maxLength)],
               ["{:.3e}".format(val) for val in BruteForce],
               ["{:.3e}".format(val) for val in Recursive],
               ["{:.3e}".format(val) for val in Memoization],
               ["{:.3e}".format(val) for val in BottomUp]],
              ("Dimensioni sequenza", "Forza-Bruta", "Ricorsivo", "Memoization", "Bottom-Up"),
                    "Tempi di esecuzione per calcolo di LCS")

if __name__ == '__main__':
    test()
    print("\n")
    print("-------------------------------------------------------------")
    print("Eseguito!")