from pprint import pprint

from data_analysis.get_data import get_main_rows


def make_boxplot(data,num_per_cluster,path):
    from pylab import plot, show, savefig, xlim, figure,hold, ylim, legend, boxplot, setp, axes

    ax = axes()
    hold(True)

    ps = [[j+i*num_per_cluster+i+1 for j in range(num_per_cluster)] for i in range(len(data))]

    for i in range(len(data)):

        boxplot(data[i], positions = ps[i], widths = 0.2)

    last_ps = ps[len(ps)-1]
    last_len = len(last_ps)
    last_val = last_ps[last_len-1]+1

    xlim(0,last_val)
    savefig(path)
    ax.clear()

# for nh=40

## impact of base b

def box_plots(header,rows,var_col_index,vars,title,path):

    nh_col_index = header.index('Number of residences')
    val_col_index = header.index('Plan value')

    groups = []

    for nh in [40,70,100]:

        group = []

        for v in vars:
            print v
            l = []

            for d in rows:

                assert isinstance(d,list)
                assert isinstance(d[var_col_index],str)
                d[nh_col_index] = int(d[nh_col_index])
                assert isinstance(d[nh_col_index],int)
                if d[var_col_index]==v and d[nh_col_index]==nh:
                    l.append(float(d[val_col_index]))
            group.append([val for val in l if val > 0])
        groups.append(group)

    make_boxplot(groups,len(vars),path)

def join_imgs(names,new_name):

    import sys
    from PIL import Image

    images = map(Image.open, names)
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    new_im.save(new_name)


def make_boxplots(raw_data):

    header = raw_data[0]
    rows = raw_data[1:]

    b = '../docs/final/images/'
    e = '.png'
    names = [b+i+e for i in ['vary_base','vary_tf','vary_nc','vary_sf','bung','man','fh']]
    i=0
    box_plots(header,rows,header.index('Base'),['base_a','base_b','base_dynamic'],'Plan value spread per base',names[i])
    i+=1
    box_plots(header,rows,header.index('Residence placer'),['TightFit_A','TightFit_B','HC'],'Plan value spread per tf',names[i])
    i+=1
    box_plots(header,rows,header.index('Number of candidates'),['2','4','6'],'Plan value spread per nc',names[i])
    i+=1
    box_plots(header,rows,header.index('Search function'),['SA','Zoom'],'Plan value spread per search function',names[i])

    join_imgs(names[:2],b+'variants1'+e)
    join_imgs(names[2:4],b+'variants2'+e)

