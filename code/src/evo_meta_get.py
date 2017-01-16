import json
import matplotlib.pyplot as plt


def plot_evo_meta(p):
    with open(p, 'r') as data:
        d = json.load(data)['d']
        r1 = []
        r2 = []
        for i in d:
            print i
            r1.append(i[5])
            r2.append(i[6])
        print r1
        plt.plot(r1)

        plt.show()

        plt.plot(r2)
        plt.show()
