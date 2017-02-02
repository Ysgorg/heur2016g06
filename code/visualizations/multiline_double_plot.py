
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np

X = 0
Y1 = 1
Y2 = 2

def plot_it(x_list, y1_list, y2_list, x_label, y1_label, y2_label, main_label, names, draw_separate_legend=True):
    fig, ax1 = plt.subplots()

    ax1.set_xlabel(x_label)

    ax1.set_ylabel(y1_label, color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    ax2.set_ylabel(y2_label, color='r')
    ax2.tick_params('y', colors='r')

    legends = []
    labels = []

    for i in range(len(y1_list)):

        l1 = names[i]
        l2 = names[i]

        s1 = y1_list[i]
        s2 = y2_list[i]
        p1, = ax1.plot(x_list[i], s1, '-', label=l1)
        p2, = ax2.plot(x_list[i], s2, '.', label=l2)

        legends.append(p1)
        legends.append(p2)

        labels.append(l1)
        labels.append(l2)

    if draw_separate_legend:
        fig_legend = pylab.figure()
        fig_legend.legend(legends, labels, 'center')
        fig_legend.show()
    else:
        plt.legend(legends, labels)

    fig.tight_layout()
    plt.show()

def prettify(param):

    parts = [param['algo'], param['base']]
    if 'nc' in param: parts.append(param['nc'])
    elif 'tf' in param : parts.append(param['tf'])
    s=''
    for i in parts: s+=str(i)+':'

    assert isinstance(s,str)
    return s


def multiline_double_plot(
        dataseries,
        x_name="Number of houses",
        y1_name="Plan value",
        y2_name="Processing time",
        main_label="Performace Overview",
        separate_legend=False):

    # assert that the input is as expected


    assert isinstance(x_name, str)
    assert isinstance(y1_name, str)
    assert isinstance(y2_name, str)
    assert isinstance(main_label, str)

    assert isinstance(dataseries, list)
    assert len(dataseries) > 0

    x_lists = []
    y1_lists = []
    y2_lists = []
    names = []

    for series in dataseries:
        assert isinstance(series, list)
        assert len(series) == 2

        # metadata can optionally be put somewhere on the visualization
        meta = series[0]
        assert 'pg' in meta  # enable playground
        assert 'nh' in meta  # number of houses
        assert 'base' in meta  # which base to use
        assert 'algo' in meta  # algorithm (zoom/sa/hillclimber)
        assert 'tf' in meta or 'nc' in meta  # tight fit algo or number of candidates (hill climber)
        assert meta[meta['variant']] == '**variant**'

        datapoints = series[1]

        x_list = []
        y1_list = []
        y2_list = []
        for d in datapoints:
            assert isinstance(d, list)
            assert len(d) == 3
            assert isinstance(d[X], float) or isinstance(d[X], int)
            assert isinstance(d[Y1], float) or d[Y1] == 0
            assert isinstance(d[Y2], float)

            x_list.append(d[X])
            y1_list.append(d[Y1])
            y2_list.append(d[Y2])
        prettified = prettify(meta)
        assert isinstance(prettified,str)

        names.append(prettified)
        x_lists.append(x_list)
        y1_lists.append(y1_list)
        y2_lists.append(y2_list)

        # plot the values

    plot_it(x_lists, y1_lists, y2_lists, x_name, y1_name, y2_name, main_label, names, separate_legend)



def test_mdp():  # test multiline double plot

    #plot_2_vals()

    multiline_double_plot([
        [  # this is a separate data series. it should have it's own color in the output visualization
            {   # this part is meta data that can optionally be put on the plot in some way
                'pg': True,
                'nh': '**variant**',
                'base': 'base_dynamic',
                'algo': 'Zoom',
                'tf': 'TightFit_WB',
                'variant': 'nh'
            },
            [
                [
                    50,  # x
                    200.0,  # y1
                    210.0  # y2
                ],
                [
                    60,
                    110.0,
                    90.9
                ]
            ]
        ],
        [  # another separate dataset
            {
                'pg': False,
                'nh': '**variant**',
                'base': 'base_a',
                'algo': 'SA',
                'tf': 'TightFit_WB',
                'variant': 'nh'
            },
            [
                [
                    50,  # x
                    160.6,  # y1
                    180.0  # y2
                ],
                [
                    60,
                    110.0,
                    90.9
                ]
            ]
        ]]
    )

#test_mdp()
