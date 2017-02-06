from matplotlib.pyplot import savefig


def filtered_out(filters,params):
    for f in filters:
        if f not in params:return True
    return False



import matplotlib.pyplot as plt

def make_lineplot(lines,title,xlab,ylab):

    plt.clf()
    for l in lines:plt.scatter(l['xes'],l['yes'],color=l['color'])
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)

    sub_parts = [p.split('=')[1] for p in title.split(',')]
    new = [sub_parts[i] for i in range(len(sub_parts))]
    fname='../docs/final/images/'+'-'.join(new)+'.png'
    print fname, len(lines)
    savefig(fname)
    plt.clf()

def get_dataseries(lines,filters,color_conditions):

    res=[]
    for l in lines:
        if filtered_out(filters,l[0]): continue
        color=None
        for i in color_conditions:
            if i['key'] in l[0]: color = i['val']
        if color is None: continue
        xes = [i[0] for i in l[1] if i is not False]
        yes = [i[1] for i in l[1] if i is not False]
        res.append({'xes':xes,'yes':yes,'color':color})

    return res

def make_lineplots(lines):

    variants = [
        ['base_a','base_b','base_dynamic'],
        [2,3,4,5,6],
        ['TightFit_A','TightFit_B'],
        ['SA','Zoom']
    ]

    colors = ['red','green','blue','brown','yellow']


    for var in variants:

        ar = []

        if var[0]==2:ar = ['HC']

        color_conditions = [{'key':var[i],'val':colors[i]} for i in range(len(var))]
        series = get_dataseries(lines,ar,color_conditions)
        title = ','.join([str(i['val'])+'=' + str(i['key'])  for i in color_conditions])
        make_lineplot(series,title,'processing time (seconds)','plan value')

    pass
