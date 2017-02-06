

def make_ijk_plots(data):

    header = data[0]
    i_col = header.index('Mansion clearance')
    j_col = header.index('Bungalow clearance')
    k_col = header.index('Familyhome clearance')
    i_list = []
    j_list = []
    k_list = []
    val_list = []
    for row in data[1:]:
        assert isinstance(row,list)
        try:
            iv = float(row[i_col])
            jv = float(row[j_col])
            kv = float(row[k_col])
        except:
            iv=0.0
            jv=0.0
            kv=0.0
        i_list.append(iv)
        j_list.append(jv)
        k_list.append(kv)
        val_list.append(row[header.index('Plan value')])


    import numpy as np
    import matplotlib.pyplot as plt

    plt.clf()
    plt.boxplot(i_list, val_list)
    plt.boxplot(j_list, val_list)
    plt.boxplot(k_list, val_list)

    plt.show()
