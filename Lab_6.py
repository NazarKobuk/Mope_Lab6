import random
from scipy.stats import f, t
from prettytable import PrettyTable
from numpy.linalg import solve
import numpy as np


def sum_kf(x1, x2, x3=None):
    xn = []
    for i in range(len(x1)):
        if x3:
            xn.append(round(x1[i] * x2[i] * x3[i], 3))
        else:
            xn.append(round(x1[i] * x2[i], 3))
    return xn


#Варіант №113


x1_min = -15
x1_max = 30
x2_min = 5
x2_max = 40
x3_min = 5
x3_max = 25
m = 3

print("З урахуванням ефекту взаємодії")
x_av_max = (x1_max + x2_max + x3_max) / 3
x_av_min = (x1_min + x2_min + x3_min) / 3
y_max = int(200 + x_av_max)
y_min = int(200 + x_av_min)

X11 = [-1, -1, -1, -1, 1, 1, 1, 1]
X22 = [-1, -1, 1, 1, -1, -1, 1, 1]
X33 = [-1, 1, -1, 1, -1, 1, -1, 1]

X12 = sum_kf(X11, X22)
X13 = sum_kf(X11, X33)
X23 = sum_kf(X22, X33)
X123 = sum_kf(X11, X22, X33)

print("y=b0+b1*x1+b2*x2+b3*x3+b12*x1*x2+b13*x1*x3+b23*x2*x3+b123*x1*x2*x3+b11*x1^2+b22*x2^2+b33*x3^2\n")
print("Кодовані значення X")
table1 = PrettyTable()
table1.add_column("№", (1, 2, 3, 4, 5, 6, 7, 8))
table1.add_column("X1", X11)
table1.add_column("X2", X22)
table1.add_column("X3", X33)
table1.add_column("X12", X12)
table1.add_column("X13", X13)
table1.add_column("X23", X23)
table1.add_column("X123", X123)
print(table1, "\n")

X1 = [x1_min, x1_min, x1_min, x1_min, x1_max, x1_max, x1_max, x1_max]
X2 = [x2_min, x2_min, x2_max, x2_max, x2_min, x2_min, x2_max, x2_max]
X3 = [x3_min, x3_max, x3_min, x3_max, x3_min, x3_max, x3_min, x3_max]

X12 = sum_kf(X1, X2)
X13 = sum_kf(X1, X3)
X23 = sum_kf(X2, X3)
X123 = sum_kf(X1, X2, X3)
X0 = [1] * 8
s1, s2, s3, s4, s5, s6, s7, s8 = 0, 0, 0, 0, 0, 0, 0, 0

while True:

    for i in range(1, m + 1):
        globals()['Y%s' % i] = [random.randrange(y_min, y_max, 1) for k in range(8)]

    for i in range(1, m + 1):
        s1 += globals()['Y%s' % i][0]
        s2 += globals()['Y%s' % i][1]
        s3 += globals()['Y%s' % i][2]
        s4 += globals()['Y%s' % i][3]
        s5 += globals()['Y%s' % i][4]
        s6 += globals()['Y%s' % i][5]
        s7 += globals()['Y%s' % i][6]
        s8 += globals()['Y%s' % i][7]

    y1_av1 = s1 / m
    y2_av2 = s2 / m
    y3_av3 = s3 / m
    y4_av4 = s4 / m
    y5_av5 = s5 / m
    y6_av6 = s6 / m
    y7_av7 = s7 / m
    y8_av8 = s8 / m

    y_av = [round(y1_av1, 3), round(y2_av2, 3), round(y3_av3, 3), round(y4_av4, 3), round(y5_av5, 3), round(y6_av6, 3),
            round(y7_av7, 3), round(y8_av8, 3)]

    sd1, sd2, sd3, sd4, sd5, sd6, sd7, sd8 = 0, 0, 0, 0, 0, 0, 0, 0
    for i in range(1, m + 1):
        sd1 += ((globals()['Y%s' % i][0]) - y1_av1) ** 2
        sd2 += ((globals()['Y%s' % i][1]) - y2_av2) ** 2
        sd3 += ((globals()['Y%s' % i][2]) - y3_av3) ** 2
        sd4 += ((globals()['Y%s' % i][3]) - y4_av4) ** 2
        sd5 += ((globals()['Y%s' % i][4]) - y5_av5) ** 2
        sd6 += ((globals()['Y%s' % i][5]) - y6_av6) ** 2
        sd7 += ((globals()['Y%s' % i][6]) - y7_av7) ** 2
        sd8 += ((globals()['Y%s' % i][7]) - y8_av8) ** 2

    d1 = sd1 / m
    d2 = sd2 / m
    d3 = sd3 / m
    d4 = sd4 / m
    d5 = sd5 / m
    d6 = sd6 / m
    d7 = sd7 / m
    d8 = sd8 / m
    disper = [round(d1, 3), round(d2, 3), round(d3, 3), round(d4, 3), round(d5, 3), round(d6, 3), round(d7, 3),
              round(d8, 3)]

    print("Матриця планування")
    table2 = PrettyTable()
    table2.add_column("№", (1, 2, 3, 4, 5, 6, 7, 8))
    table2.add_column("X1", X1)
    table2.add_column("X2", X2)
    table2.add_column("X3", X3)
    table2.add_column("X12", X12)
    table2.add_column("X13", X13)
    table2.add_column("X23", X23)
    table2.add_column("X123", X123)
    for i in range(1, m + 1):
        table2.add_column("Y" + str(i), globals()['Y%s' % i])
    table2.add_column("Y", y_av)
    table2.add_column("S^2", disper)
    print(table2, "\n")

    b = [i for i in solve(list(zip(X0, X1, X2, X3, X12, X13, X23, X123)), y_av)]
    b0, b1, b2, b3, b4, b5, b6, b7 = round(b[0], 3), round(b[1], 3), round(b[2], 3), round(b[3], 3), round(b[4],
                                                                                                           3), round(
        b[5], 3), round(b[6], 3), round(b[7], 3)

    print("y=" + str(b0) + "+" + str(b1) + "*x1+" + str(b2) + "*x2+" + str(b3) + "*x3+" + str(b4) + "*x1*x2+" + str(
        b5) + "*x1*x3+" + str(b6) + "*x2*x3+" + str(b7) + "*x1*x2*x3", "\n")

    dcouple = [d1, d2, d3, d4, d5, d6, d7, d8]
    print("Критерій Кохрена")

    Gp = max(dcouple) / sum(dcouple)
    q = 0.05
    f1 = m - 1
    f2 = N = 8
    fisher = f.isf(*[q / f2, f1, (f2 - 1) * f1])
    Gt = round(fisher / (fisher + (f2 - 1)), 4)
    print("Gp = " + str(Gp) + ", Gt = " + str(Gt))

    if Gp > Gt:
        print("Дисперсія  неоднорідна , збільшуємо m")
        m += 1
        continue

    print("Gp < Gt -> Дисперсія однорідна\n")
    print("Критерій Стьюдента")
    sb = sum(dcouple) / N
    ssbs = sb / N * m
    sbs = ssbs ** 0.5

    beta0 = (y1_av1 * 1 + y2_av2 * 1 + y3_av3 * 1 + y4_av4 * 1 + y5_av5 * 1 + y6_av6 * 1 + y7_av7 * 1 + y8_av8 * 1) / 8
    beta1 = (y1_av1 * (-1) + y2_av2 * (-1) + y3_av3 * (-1) + y4_av4 * (
        -1) + y5_av5 * 1 + y6_av6 * 1 + y7_av7 * 1 + y8_av8 * 1) / 8
    beta2 = (y1_av1 * (-1) + y2_av2 * (-1) + y3_av3 * 1 + y4_av4 * 1 + y5_av5 * (-1) + y6_av6 * (
        -1) + y7_av7 * 1 + y8_av8 * 1) / 8
    beta3 = (y1_av1 * (-1) + y2_av2 * 1 + y3_av3 * (-1) + y4_av4 * 1 + y5_av5 * (-1) + y6_av6 * 1 + y7_av7 * (
        -1) + y8_av8 * 1) / 8
    beta4 = (y1_av1 * 1 + y2_av2 * 1 + y3_av3 * (-1) + y4_av4 * (-1) + y5_av5 * (-1) + y6_av6 * (
        -1) + y7_av7 * 1 + y8_av8 * 1) / 8
    beta5 = (y1_av1 * 1 + y2_av2 * (-1) + y3_av3 * 1 + y4_av4 * (-1) + y5_av5 * (-1) + y6_av6 * 1 + y7_av7 * (
        -1) + y8_av8 * 1) / 8
    beta6 = (y1_av1 * 1 + y2_av2 * (-1) + y3_av3 * (-1) + y4_av4 * 1 + y5_av5 * 1 + y6_av6 * (-1) + y7_av7 * (
        -1) + y8_av8 * 1) / 8
    beta7 = (y1_av1 * (-1) + y2_av2 * 1 + y3_av3 * 1 + y4_av4 * (-1) + y5_av5 * 1 + y6_av6 * (-1) + y7_av7 * (
        -1) + y8_av8 * 1) / 8

    t0 = abs(beta0) / sbs
    t1 = abs(beta1) / sbs
    t2 = abs(beta2) / sbs
    t3 = abs(beta3) / sbs
    t4 = abs(beta4) / sbs
    t5 = abs(beta5) / sbs
    t6 = abs(beta6) / sbs
    t7 = abs(beta7) / sbs

    f3 = f1 * f2
    ttabl = round(abs(t.ppf(q / 2, f3)), 4)

    quantity_of_koef = 0
    sum_koef = 0
    d = 8
    if (t0 < ttabl):
        print("t0 < ttabl, b0 не значимий")
        b0 = 0
        d = d - 1
    else:
        sum_koef += b0
        quantity_of_koef += 1
    if (t1 < ttabl):
        print("t1 < ttabl, b1 не значимий")
        b1 = 0
        d = d - 1
    else:
        sum_koef += b1
        quantity_of_koef += 1
    if (t2 < ttabl):
        print("t2 < ttabl, b2 не значимий")
        b2 = 0
        d = d - 1
    else:
        sum_koef += b2
        quantity_of_koef += 1
    if (t3 < ttabl):
        print("t3 < ttabl, b3 не значимий")
        b3 = 0
        d = d - 1
    else:
        sum_koef += b3
        quantity_of_koef += 1
    if (t4 < ttabl):
        print("t4 < ttabl, b4 не значимий")
        b4 = 0
        d = d - 1
    else:
        sum_koef += b4
        quantity_of_koef += 1
    if (t5 < ttabl):
        print("t5 < ttabl, b5 не значимий")
        b5 = 0
        d = d - 1
    else:
        sum_koef += b5
        quantity_of_koef += 1
    if (t6 < ttabl):
        print("t6 < ttabl, b6 не значимий")
        b6 = 0
        d = d - 1
    else:
        sum_koef += b6
        quantity_of_koef += 1
    if (t7 < ttabl):
        print("t7 < ttabl, b7 не значимий\n")
        b7 = 0
        d = d - 1
    else:
        sum_koef += b7
        quantity_of_koef += 1

    print("Середнє значення значимих коефіцієнтів =", sum_koef / quantity_of_koef)

    yy1 = b0 + b1 * x1_min + b2 * x2_min + b3 * x3_min + b4 * x1_min * x2_min + b5 * x1_min * x3_min + b6 * x2_min * \
          x3_min + b7 * x1_min * x2_min * x3_min
    yy2 = b0 + b1 * x1_min + b2 * x2_min + b3 * x3_max + b4 * x1_min * x2_min + b5 * x1_min * x3_max + b6 * x2_min * \
          x3_max + b7 * x1_min * x2_min * x3_max
    yy3 = b0 + b1 * x1_min + b2 * x2_max + b3 * x3_min + b4 * x1_min * x2_max + b5 * x1_min * x3_min + b6 * x2_max * \
          x3_min + b7 * x1_min * x2_max * x3_min
    yy4 = b0 + b1 * x1_min + b2 * x2_max + b3 * x3_max + b4 * x1_min * x2_max + b5 * x1_min * x3_max + b6 * x2_max * \
          x3_max + b7 * x1_min * x2_max * x3_max
    yy5 = b0 + b1 * x1_max + b2 * x2_min + b3 * x3_min + b4 * x1_max * x2_min + b5 * x1_max * x3_min + b6 * x2_min * \
          x3_min + b7 * x1_max * x2_min * x3_min
    yy6 = b0 + b1 * x1_max + b2 * x2_min + b3 * x3_max + b4 * x1_max * x2_min + b5 * x1_max * x3_max + b6 * x2_min * \
          x3_max + b7 * x1_max * x2_min * x3_max
    yy7 = b0 + b1 * x1_max + b2 * x2_max + b3 * x3_min + b4 * x1_max * x2_max + b5 * x1_max * x3_min + b6 * x2_max * \
          x3_min + b7 * x1_max * x2_max * x3_min
    yy8 = b0 + b1 * x1_max + b2 * x2_max + b3 * x3_max + b4 * x1_max * x2_max + b5 * x1_max * x3_max + b6 * x2_max * \
          x3_max + b7 * x1_max * x2_max * x3_max

    print("Критерій Фішера")
    print(d, " значимих коефіцієнтів")
    f4 = N - d
    sad = ((yy1 - y1_av1) ** 2 + (yy2 - y2_av2) ** 2 + (yy3 - y3_av3) ** 2 + (yy4 - y4_av4) ** 2 + (
            yy5 - y5_av5) ** 2 + (
                   yy6 - y6_av6) ** 2 + (yy7 - y7_av7) ** 2 + (yy8 - y8_av8) ** 2) * (m / (N - d))
    Fp = sad / sb
    print("Fp=", round(Fp, 2))

    Ft = round(abs(f.isf(q, f4, f3)), 4)

    print("Fp = " + str(round(Fp, 2)) + ", Ft = " + str(Ft))
    if Fp > Ft:
        print("Fp > Ft -> Рівняння неадекватне оригіналу\n\n\nПереходимо до рівняння регресії з квадратичними членами")
    else:
        print("Fp < Ft -> Рівняння адекватне оригіналу")
        break

    # З квадратичними членами========================================================
    while True:

        x01 = (x1_max + x1_min) / 2
        x02 = (x2_max + x2_min) / 2
        x03 = (x3_max + x3_min) / 2
        deltax1 = x1_max - x01
        deltax2 = x2_max - x02
        deltax3 = x3_max - x03

        X11 = [-1, -1, -1, -1, 1, 1, 1, 1, -1.73, 1.73, 0, 0, 0, 0, 0]
        X22 = [-1, -1, 1, 1, -1, -1, 1, 1, 0, 0, -1.73, 1.73, 0, 0, 0]
        X33 = [-1, 1, -1, 1, -1, 1, -1, 1, 0, 0, 0, 0, -1.73, 1.73, 0]


        def kv(x):
            """Повертає список квадратів кожного елемента"""
            xn = []
            for i in range(len(x)):
                xn.append(round(x[i] * x[i], 3))
            return xn


        X12 = sum_kf(X11, X22)
        X13 = sum_kf(X11, X33)
        X23 = sum_kf(X22, X33)
        X123 = sum_kf(X11, X22, X33)
        X1_kv = kv(X11)
        X2_kv = kv(X22)
        X3_kv = kv(X33)

        print("y=b0+b1*x1+b2*x2+b3*x3+b12*x1*x2+b13*x1*x3+b23*x2*x3+b123*x1*x2*x3+b11*x1^2+b22*x2^2+b33*x3^2\n")
        table1 = PrettyTable()
        table1.add_column("№", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))
        table1.add_column("X1", X11)
        table1.add_column("X2", X22)
        table1.add_column("X3", X33)
        table1.add_column("X12", X12)
        table1.add_column("X13", X13)
        table1.add_column("X23", X23)
        table1.add_column("X123", X123)
        table1.add_column("X1^2", X1_kv)
        table1.add_column("X2^2", X2_kv)
        table1.add_column("X3^2", X3_kv)

        print("Матриця планування експерименту для РЦКП при k=3 із нормованими значеннями факторів \n")
        print(table1, "\n")

        X1 = [x1_min, x1_min, x1_min, x1_min, x1_max, x1_max, x1_max, x1_max, round(-1.73 * deltax1 + x01, 3),
              round(1.73 * deltax1 + x01, 3), x01, x01, x01, x01, x01]
        X2 = [x2_min, x2_min, x2_max, x2_max, x2_min, x2_min, x2_max, x2_max, x02, x02, round(-1.73 * deltax2 + x02, 3),
              round(1.73 * deltax2 + x02, 3), x02, x02, x02]
        X3 = [x3_min, x3_max, x3_min, x3_max, x3_min, x3_max, x3_min, x3_max, x03, x03, x03, x03,
              round(-1.73 * deltax3 + x03,
                    3), round(1.73 * deltax3 + x03, 3), x03]
        X12 = sum_kf(X1, X2)
        X13 = sum_kf(X1, X3)
        X23 = sum_kf(X2, X3)
        X123 = sum_kf(X1, X2, X3)
        X1_kv = kv(X1)
        X2_kv = kv(X2)
        X3_kv = kv(X3)

        for j in range(1, m + 1):
            globals()['Y%s' % j] = [round(
                6.7 + 7.1 * X1[i] + 7.8 * X2[i] + 7.4 * X3[i] + 0.1 * X1_kv[i] + 0.7 * X2_kv[i] + 7.1 * X3_kv[i] + 8.2 *
                X12[i]
                + 0.2 * X13[i] + 9.5 * X23[i] + 6.6 * X123[i] + random.randrange(-10, 10) - 5, 3) for i in range(15)]

        y1_av1, y2_av2, y3_av3, y4_av4, y5_av5, y6_av6, y7_av7, y8_av8, y9_av9, y10_av10, y11_av11, y12_av12, y13_av13, y14_av14, y15_av15 = \
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        for i in range(1, m + 1):
            for k in range(15):
                globals()['y%s_av%s' % (k + 1, k + 1)] += globals()['Y%s' % i][k] / m

        y_av = []
        for i in range(15):
            y_av.append(round(globals()['y%s_av%s' % (i + 1, i + 1)], 3))

        table2 = PrettyTable()
        table2.add_column("№", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))
        table2.add_column("X1", X1)
        table2.add_column("X2", X2)
        table2.add_column("X3", X3)
        table2.add_column("X12", X12)
        table2.add_column("X13", X13)
        table2.add_column("X23", X23)
        table2.add_column("X123", X123)
        table2.add_column("X1^2", X1_kv)
        table2.add_column("X2^2", X2_kv)
        table2.add_column("X3^2", X3_kv)

        for i in range(1, m + 1):
            table2.add_column("Y" + str(i), globals()['Y%s' % i])
        table2.add_column("Y", y_av)
        print("Матриця планування експерименту для РЦКП при k=3 із натуралізованими значеннями факторів\n")
        print(table2, "\n")

        for i in range(15):
            globals()['d%s' % (i + 1)] = 0
        for k in range(1, m + 1):
            for i in range(15):
                globals()['d%s' % (i + 1)] += ((globals()['Y%s' % k][i]) - globals()[
                    'y%s_av%s' % (i + 1, i + 1)]) ** 2 / m

        X0 = [1] * 15

        b = np.linalg.lstsq(list(zip(X0, X1, X2, X3, X12, X13, X23, X123, X1_kv, X2_kv, X3_kv)), y_av, rcond=None)[0]
        b = [round(i, 3) for i in b]
        print("\nКоефіцієти b:", b)
        print("Перевірка:")
        for i in range(15):
            print("y" + str(i + 1) + "_av" + str(i + 1) + " = " + str(round(
                b[0] + b[1] * X1[i] + b[2] * X2[i] + b[3] * X3[i] + b[4] * X1[i] * X2[i] + b[5] * X1[i] * X3[i] + b[6] *
                X2[i] *
                X3[i] + b[7] * X1[i] * X2[i] * X3[i] + b[8] * X1_kv[i] + b[9] * X2_kv[i] + b[10] * X3_kv[i],
                3)) + " = " + str(
                round(globals()['y%s_av%s' % (i + 1, i + 1)], 3)))

        dcouple = []
        for i in range(15):
            dcouple.append(round(globals()['d%s' % (i + 1)], 3))

        print("\nКритерій Кохрена")
        Gp = max(dcouple) / sum(dcouple)
        q = 0.05
        f1 = m - 1
        f2 = N = 15
        fisher = f.isf(*[q / f2, f1, (f2 - 1) * f1])
        Gt = round(fisher / (fisher + (f2 - 1)), 4)
        print("Gp = " + str(Gp) + ", Gt = " + str(Gt))
        if Gp >= Gt:
            m += 1
            print("Дисперсія неоднорідна, збільшуємо m\n")
            continue
        print("Gp < Gt -> Дисперсія однорідна\n")

        print("Критерій Стьюдента")
        sb = sum(dcouple) / N
        ssbs = sb / N * m
        sbs = ssbs ** 0.5

        beta0 = (
                        y1_av1 * 1 + y2_av2 * 1 + y3_av3 * 1 + y4_av4 * 1 + y5_av5 * 1 + y6_av6 * 1 + y7_av7 * 1 + y8_av8 * 1 + y9_av9 * (
                    -1.215) + y10_av10 * 1.215 + y11_av11 * 0 + y12_av12 * 0 + y13_av13 * 0 + y14_av14 * 0 + y15_av15 * 0) / 15
        beta1 = (y1_av1 * (-1) + y2_av2 * (-1) + y3_av3 * (-1) + y4_av4 * (
            -1) + y5_av5 * 1 + y6_av6 * 1 + y7_av7 * 1 + y8_av8 * 1 + y9_av9 * 0 + y10_av10 * 0 + y11_av11 * (
                     -1.215) + y12_av12 * 1.215 + y13_av13 * 0 + y14_av14 * 0 + y15_av15 * 0) / 15
        beta2 = (y1_av1 * (-1) + y2_av2 * (-1) + y3_av3 * 1 + y4_av4 * 1 + y5_av5 * (-1) + y6_av6 * (
            -1) + y7_av7 * 1 + y8_av8 * 1 + y9_av9 * 0 + y10_av10 * 0 + y11_av11 * 0 + y12_av12 * 0 + y13_av13 * (
                     -1.215) + y14_av14 * 1.215 + y15_av15 * 0) / 15
        beta3 = (y1_av1 * (-1) + y2_av2 * 1 + y3_av3 * (-1) + y4_av4 * 1 + y5_av5 * (-1) + y6_av6 * 1 + y7_av7 * (
            -1) + y8_av8 * 1) / 15
        beta4 = (y1_av1 * 1 + y2_av2 * 1 + y3_av3 * (-1) + y4_av4 * (-1) + y5_av5 * (-1) + y6_av6 * (
            -1) + y7_av7 * 1 + y8_av8 * 1) / 15
        beta5 = (y1_av1 * 1 + y2_av2 * (-1) + y3_av3 * 1 + y4_av4 * (-1) + y5_av5 * (-1) + y6_av6 * 1 + y7_av7 * (
            -1) + y8_av8 * 1) / 15
        beta6 = (y1_av1 * 1 + y2_av2 * (-1) + y3_av3 * (-1) + y4_av4 * 1 + y5_av5 * 1 + y6_av6 * (-1) + y7_av7 * (
            -1) + y8_av8 * 1) / 15
        beta7 = (y1_av1 * (-1) + y2_av2 * 1 + y3_av3 * 1 + y4_av4 * (-1) + y5_av5 * 1 + y6_av6 * (-1) + y7_av7 * (
            -1) + y8_av8 * 1) / 15
        beta8 = (y1_av1 * 1 + y2_av2 * 1 + y3_av3 * 1 + y4_av4 * 1 + y5_av5 * 1 + y6_av6 * 1 + y7_av7 * 1 + y8_av8 * 1
                 + y9_av9 * 1.46723 + y10_av10 * 1.46723) / 15
        beta9 = (y1_av1 * 1 + y2_av2 * 1 + y3_av3 * 1 + y4_av4 * 1 + y5_av5 * 1 + y6_av6 * 1 + y7_av7 * 1 + y8_av8 * 1
                 + y11_av11 * 1.46723 + y12_av12 * 1.46723) / 15
        beta10 = (y1_av1 * 1 + y2_av2 * 1 + y3_av3 * 1 + y4_av4 * 1 + y5_av5 * 1 + y6_av6 * 1 + y7_av7 * 1 + y8_av8 * 1
                  + y13_av13 * 1.46723 + y14_av14 * 1.46723) / 15

        f3 = f1 * f2
        ttabl = round(abs(t.ppf(q / 2, f3)), 4)

        d = 11

        koef = 0
        quantity = 0

        for i in range(11):
            if (abs(globals()['beta%s' % i]) / sbs) < ttabl:
                print("t%s < ttabl, b%s не значимий" % (i, i))
                globals()['b%s' % i] = 0
                d = d - 1

            else:

                print("t%s >= ttabl, b%s значимий" % (i, i))
                koef += b[i]
                quantity += 1

        print("\nПеревірка при підстановці в спрощене рівняння регресії:")
        for i in range(15):
            print("y" + str(i + 1) + "_av" + str(i + 1) + " = " + str(round(
                b[0] + b[1] * X1[i] + b[2] * X2[i] + b[3] * X3[i] + b[4] * X1[i] * X2[i] + b[5] * X1[i] * X3[i] + b[6] *
                X2[
                    i] * X3[i] + b[7] * X1[i] * X2[i] * X3[i] + b[8] * X1_kv[i] + b[9] * X2_kv[i] + b[10] * X3_kv[i],
                3)) + " = " + str(round(globals()['y%s_av%s' % (i + 1, i + 1)], 3)))

        yy1 = b[0] + b[1] * x1_min + b[2] * x2_min + b[3] * x3_min + b[4] * x1_min * x2_min + b[5] * x1_min * x3_min + \
              b[
                  6] * x2_min * x3_min + b[7] * x1_min * x2_min * x3_min + b[8] * x1_min * x1_min + b[
                  9] * x2_min * x2_min + b[
                  10] * x3_min * x3_min
        yy2 = b[0] + b[1] * x1_min + b[2] * x2_min + b[3] * x3_max + b[4] * x1_min * x2_min + b[5] * x1_min * x3_max + \
              b[
                  6] * x2_min * x3_max + b[7] * x1_min * x2_min * x3_max + b[8] * x1_min * x1_min + b[
                  9] * x2_min * x2_min + b[
                  10] * x3_max * x3_max
        yy3 = b[0] + b[1] * x1_min + b[2] * x2_max + b[3] * x3_min + b[4] * x1_min * x2_max + b[5] * x1_min * x3_min + \
              b[
                  6] * x2_max * x3_min + b[7] * x1_min * x2_max * x3_min + b[8] * x1_min * x1_min + b[
                  9] * x2_max * x2_max + b[
                  10] * x3_min * x3_min
        yy4 = b[0] + b[1] * x1_min + b[2] * x2_max + b[3] * x3_max + b[4] * x1_min * x2_max + b[5] * x1_min * x3_max + \
              b[
                  6] * x2_max * x3_max + b[7] * x1_min * x2_max * x3_max + b[8] * x1_min * x1_min + b[
                  9] * x2_max * x2_max + b[
                  10] * x3_max * x3_max
        yy5 = b[0] + b[1] * x1_max + b[2] * x2_min + b[3] * x3_min + b[4] * x1_max * x2_min + b[5] * x1_max * x3_min + \
              b[
                  6] * x2_min * x3_min + b[7] * x1_max * x2_min * x3_min + b[8] * x1_max * x1_max + b[
                  9] * x2_min * x2_min + b[
                  10] * x3_min * x3_min
        yy6 = b[0] + b[1] * x1_max + b[2] * x2_min + b[3] * x3_max + b[4] * x1_max * x2_min + b[5] * x1_max * x3_max + \
              b[
                  6] * x2_min * x3_max + b[7] * x1_max * x2_min * x3_max + b[8] * x1_max * x1_max + b[
                  9] * x2_min * x2_min + b[
                  10] * x3_max * x3_max
        yy7 = b[0] + b[1] * x1_max + b[2] * x2_max + b[3] * x3_min + b[4] * x1_max * x2_max + b[5] * x1_max * x3_min + \
              b[
                  6] * x2_max * x3_min + b[7] * x1_max * x2_max * x3_min + b[8] * x1_max * x1_max + b[
                  9] * x2_max * x2_max + b[
                  10] * x3_min * x3_min
        yy8 = b[0] + b[1] * x1_max + b[2] * x2_max + b[3] * x3_max + b[4] * x1_max * x2_max + b[5] * x1_max * x3_max + \
              b[
                  6] * x2_max * x3_max + b[7] * x1_max * x2_max * x3_max + b[8] * x1_max * x1_max + b[
                  9] * x2_max * x2_max + b[
                  10] * x3_max * x3_max

        yy9 = b[0] + b[1] * X1[8] + b[2] * X2[8] + b[3] * X3[8] + b[4] * X12[8] + b[5] * X13[8] + b[6] * X23[8] + b[7] * \
              X123[8] + b[8] * X1_kv[8] + b[9] * X2_kv[8] + b[10] * X3_kv[8]
        yy10 = b[0] + b[1] * X1[9] + b[2] * X2[9] + b[3] * X3[9] + b[4] * X12[9] + b[5] * X13[9] + b[6] * X23[9] + b[
            7] * \
               X123[9] + b[8] * X1_kv[9] + b[9] * X2_kv[9] + b[10] * X3_kv[9]
        yy11 = b[0] + b[1] * X1[10] + b[2] * X2[10] + b[3] * X3[10] + b[4] * X12[10] + b[5] * X13[10] + b[6] * X23[10] + \
               b[
                   7] * X123[10] + b[8] * X1_kv[10] + b[9] * X2_kv[10] + b[10] * X3_kv[10]
        yy12 = b[0] + b[1] * X1[11] + b[2] * X2[11] + b[3] * X3[11] + b[4] * X12[11] + b[5] * X13[11] + b[6] * X23[11] + \
               b[
                   7] * X123[11] + b[8] * X1_kv[11] + b[9] * X2_kv[11] + b[10] * X3_kv[11]
        yy13 = b[0] + b[1] * X1[12] + b[2] * X2[12] + b[3] * X3[12] + b[4] * X12[12] + b[5] * X13[12] + b[6] * X23[12] + \
               b[
                   7] * X123[12] + b[8] * X1_kv[12] + b[9] * X2_kv[12] + b[10] * X3_kv[12]
        yy14 = b[0] + b[1] * X1[13] + b[2] * X2[13] + b[3] * X3[13] + b[4] * X12[13] + b[5] * X13[13] + b[6] * X23[13] + \
               b[
                   7] * X123[13] + b[8] * X1_kv[13] + b[9] * X2_kv[13] + b[10] * X3_kv[13]
        yy15 = b[0] + b[1] * X1[14] + b[2] * X2[14] + b[3] * X3[14] + b[4] * X12[14] + b[5] * X13[14] + b[6] * X23[14] + \
               b[
                   7] * X123[14] + b[8] * X1_kv[14] + b[9] * X2_kv[14] + b[10] * X3_kv[14]

        print("\nКритерій Фішера")
        print(d, "значимих коефіцієнтів")

        print("\nСереднє значення значимих коефіцієнтів =", koef / quantity)

        f4 = N - d
        sad = ((yy1 - y1_av1) ** 2 + (yy2 - y2_av2) ** 2 + (yy3 - y3_av3) ** 2 + (yy4 - y4_av4) ** 2 + (
                yy5 - y5_av5) ** 2 +
               (yy6 - y6_av6) ** 2 + (yy7 - y7_av7) ** 2 + (yy8 - y8_av8) ** 2 + (yy9 - y9_av9) ** 2 +
               (yy10 - y10_av10) ** 2 + (yy11 - y11_av11) ** 2 + (yy12 - y12_av12) ** 2 + (yy13 - y13_av13) ** 2 +
               (yy14 - y14_av14) ** 2 + (yy15 - y15_av15) ** 2) * (m / (N - d))

        Fp = sad / sb
        print("\nFp =", round(Fp, 2))

        Ft = round(abs(f.isf(q, f4, f3)), 4)
        print("Ft =", round(Ft, 2))
        if Fp > Ft:
            print("Fp > Ft -> Рівняння неадекватне оригіналу")
        else:
            print("Fp < Ft -> Рівняння адекватне оригіналу")
            break
    break
