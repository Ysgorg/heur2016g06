
X=0
Y1=1
Y2=2

def multiline_double_plot(
        datapoints,
        x_name="Number of houses",
        y1_name="Plan value",
        y2_name="Processing time",
        main_label="Performace Overview"):

    assert isinstance(x_name,str)
    assert isinstance(y1_name,str)
    assert isinstance(y2_name,str)
    assert isinstance(main_label,str)

    assert isinstance(datapoints,list)
    assert len(datapoints[0]) > 0

    for d in datapoints:
        assert type(d) == list
        assert len(d) == 3
        assert isinstance(d[X],float) or isinstance(d[X],int)
        assert isinstance(d[Y1],float)
        assert isinstance(d[Y2],float)


    # plot the values







multiline_double_plot([
    [
        50, # x
        200.0, # y1
        210.0 # y2
    ],[
        60,
        110.0,
        90.9
    ]
])