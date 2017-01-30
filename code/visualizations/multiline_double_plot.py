
X=0
Y1=1
Y2=2

def multiline_double_plot(
        dataseries,
        x_name="Number of houses",
        y1_name="Plan value",
        y2_name="Processing time",
        main_label="Performace Overview"):

    # assert that the input is as expected

    assert isinstance(x_name,str)
    assert isinstance(y1_name,str)
    assert isinstance(y2_name,str)
    assert isinstance(main_label,str)

    assert isinstance(dataseries,list)
    assert len(dataseries) > 0

    for series in dataseries:
        assert isinstance(series,list)
        assert len(series)==2

        # metadata can optionally be put somewhere on the visualization
        meta = series[0]
        assert 'pg' in meta # enable playground
        assert 'nh' in meta # number of houses
        assert 'base' in meta # which base to use
        assert 'algo' in meta # algorithm (zoom/sa/hillclimber)
        assert 'tf' in meta or 'nc' in meta # tight fit algo or number of candidates (hill climber)
        assert meta[meta['variant']] == '**variant**'

        datapoints = series[1]

        for d in datapoints:
            assert isinstance(d, list)
            assert len(d) == 3
            assert isinstance(d[X],float) or isinstance(d[X],int)
            assert isinstance(d[Y1],float) or d[Y1] == 0
            assert isinstance(d[Y2],float)

    # plot the values



def test_mdp(): # test multiline double plot

    multiline_double_plot([
        [ # this is a separate data series. it should have it's own color in the output visualization
            {   # this part is meta data that can optionally be put on the plot in some way
                'pg':True,
                'nh':'**variant**',
                'base':'base_dynamic',
                'algo':'Zoom',
                'tf':'TightFit_WB',
                'variant':'nh'
            },
            [
                [
                    50, # x
                    200.0, # y1
                    210.0 # y2
                ],
                [
                    60,
                    110.0,
                    90.9
                ]
            ]
        ],
        [ # another separate dataset
            {
                'pg':False,
                'nh':'**variant**',
                'base':'base_a',
                'algo':'SimmulatedAnnealing_2',
                'tf':'TightFit_WB',
                'variant':'nh'
            },
            [
                [
                    50, # x
                    160.6, # y1
                    180.0 # y2
                ],
                [
                    60,
                    110.0,
                    90.9
                ]
            ]
        ]]
    )