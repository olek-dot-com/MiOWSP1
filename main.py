import matplotlib.pyplot as plt


a_min = float(input("minimalny ruch - "))
a_max = float(input("maksymalny ruch - "))
a_step = float(input("krok obliczen - "))
C = int(input("Pojemnosc systemu - ")) #pojemnosc systemu
m = int(input("liczba klas strumieni oferowanych systemowi - ")) #liczba klas strumieni oferowanych systemowi

# a_min = 0.2
# a_max = 1.3
# a_step = 0.1
# C = 20
# m = 2
t=[] #t_i dla każdej klasy strumieni oferowanych systemowi

#uzupełnienie jednostek alokacji dla poszczególnych klas strumieni
for i in range(m):
    t_i = input(f"zadania strumienia klasy {i+1} - ")
    t.append(float(t_i))

strumien_a = [] #strumien a 0.2 0.3 0.4 0.5 0.6 itd..

#uzupelnienie listy strumien_a
w_iterator = a_min
while round(w_iterator, 2) <= a_max:
    strumien_a.append(float(w_iterator))
    w_iterator+=a_step

a_i = [] #a_i dla każdego strumienia i liczby jednostek alokacji. Wielowymiarowa tablica aby

#uzupełnienie tablicy a_i dla każdego strumienia i każdej jednostki alokacji ze wzoru 7 z treści zadania
for i in range(len(strumien_a)):
    row = []
    for j in range(m):
        row.append(float(strumien_a[i] * C) / (m * t[j]))
    a_i.append(row)


wiersze_po_kaufmanie = [] #lista prawdopodobieństw dla poszczególnych wierszy po zrealizowaniu schematu Kaufmana-Robertsa
tablica_zrealizowanych_kaufman = {} #tablica zrealizowanych prawdopodobieństw dla poszczególnych wierszy aby usprawnić obliczenia

#funkcja realizująca pierwsze zadanie korzystająca ze schematu rekurencyjnego Kaufmana-Robertsa (4) z treści zadania
def kaufman_roberts(n, row_strumienia_a): #s[n]
    if (n, row_strumienia_a) in tablica_zrealizowanych_kaufman:
        return tablica_zrealizowanych_kaufman[(n, row_strumienia_a)]
    if n == 0:
        return 1
    if n > 0:
        suma = 0.0
        for i in range(m):
            if n - t[i] >= 0:
                suma += a_i[row_strumienia_a][i] * t[i] * kaufman_roberts(n - t[i], row_strumienia_a)
        rozklad_zajetosci = suma / n
        tablica_zrealizowanych_kaufman[(n, row_strumienia_a)] = rozklad_zajetosci
        return rozklad_zajetosci
    return 0

sumy_dla_poszczegolnych_strumieni_a = [] #SUM
for i in range(len(strumien_a)):
    suma_dla_poszczegolnego_strumienia = 0.0
    for j in range(C+1):
        suma_dla_poszczegolnego_strumienia += kaufman_roberts(j,i)
    sumy_dla_poszczegolnych_strumieni_a.append(suma_dla_poszczegolnego_strumienia)

def prawdopodobienstwo_zajetosci(n,row_strumienia_a): #p[n]
    result = kaufman_roberts(n,row_strumienia_a)/sumy_dla_poszczegolnych_strumieni_a[row_strumienia_a]
    return result

def blokada_strumienia(t_i,row_strumienia_a): #E_i prawdopodobienstwo blokady dla strumienia
    prawd_blokady = 0.0
    for i in range(C-int(t[t_i])+1,C+1):
        prawd_blokady += prawdopodobienstwo_zajetosci(i,row_strumienia_a)
    return prawd_blokady

#zapisanie wyników pierwszego zadania do pliku sol.txt
def zapisz_do_pliku_sol1():
    with open('sol.txt', 'w') as f:
        f.write("# C = %d \n#\n" % C)
        for i in range(m):
            f.write(f"# t{i+1} = {t[i]}\n")
        f.write("#\n")
        f.write("{:<25}".format("a"))
        for i in range(m):
            f.write(f"t{i+1:<25}")
        f.write("\n")
        for i in range(len(strumien_a)):
            f.write("{:<25} ".format(round(strumien_a[i], 2)))
            for j in range(m):
                f.write("{:<25}".format(blokada_strumienia(j,i)))
            f.write('\n')
#funkcja realizująca drugie zadanie korzystająca ze wzoru 6 z treści zadania
def zadanie_2(row, col, n):
    if 0 <= n-t[col] <= C:
        return (a_i[row][col]*t[col]*prawdopodobienstwo_zajetosci(n-t[col],row))/prawdopodobienstwo_zajetosci(n,row)
    return 0

#zapisanie wyników drugiego zadania do pliku sol2.txt
def zapisz_do_pliku_sol2():
    with open('sol2.txt', 'w') as f:
        f.write("# C = %d \n#\n" % C)
        for i in range(m):
            f.write(f"# t{i+1} = {t[i]}\n")
        f.write("#\n")
        for ai in range(len(strumien_a)):
            f.write("{:<25}".format(round(strumien_a[ai], 2)))
            for i in range(m):
                f.write(f"t{i+1:<25}")
            f.write("{:<12}".format(":"))
            f.write("sum\n")
            for row in range(C+1):
                f.write(f"{row:<25}")
                sum = 0
                for col in range(m):
                    value = round(zadanie_2(ai,col,row),5)
                    f.write(f"{value:<25}")
                    sum += value
                f.write("{:<12}".format(":"))
                f.write(f"{str(sum):>12}")
                f.write("\n")
            f.write("\n")

def wykresy_dla_sol1(): #tworzenie wykresu dla t1,t2,t3 itd. w skali logarytmicznej dla pierwszego zadania skalą x jest a
    for i in range(m):
        y = []
        for j in range(len(strumien_a)):
            y.append(blokada_strumienia(i,j))
        plt.plot(strumien_a, y, label=f"t{i+1}")
    plt.yscale('log')
    plt.xlabel('a')
    plt.grid(True)
    plt.ylabel('Prawdopodobieństwo blokady')
    plt.legend()
    plt.title('Prawdopodobieństwo blokady w zależności od a')
    plt.savefig('wykres1.png')
    plt.show()

def wykresy_dla_sol2():
    for i in range(m):
        y = []
        for j in range(len(strumien_a)):
            y.append(blokada_strumienia(i,j))
        plt.plot(strumien_a, y, label=f"t{i+1}")
    plt.yscale('log')
    plt.xlabel('a')
    plt.grid(True)
    plt.ylabel('Prawdopodobieństwo blokady')
    plt.legend()
    plt.title('Prawdopodobieństwo blokady w zależności od a')
    plt.savefig('wykres2.png')
    plt.show()



task = input("które zadanie chcesz wykonać? (1/2) - ")
if task == '1':
    wykresy_dla_sol1()
    zapisz_do_pliku_sol1()
elif task == '2':
    wykresy_dla_sol2()
    zapisz_do_pliku_sol2()
elif task == '3':
    wykresy_dla_sol1()
    wykresy_dla_sol2()
    zapisz_do_pliku_sol1()
    zapisz_do_pliku_sol2()