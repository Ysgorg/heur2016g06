from time import sleep


def get_corner_residence(R, plan, x0, y0, x_dir, y_dir,frame,slow):

    x = x0 + x_dir
    y = y0 + y_dir
    x_offset = 0
    y_offset = 0
    if x_dir < 0: x_offset = R(0, 0).width
    if y_dir < 0: y_offset = R(0, 0).height

    while not plan.correctlyPlaced(R(x - x_offset, y - y_offset)):

        assert x >= 0 and x < plan.width
        assert y >= 0 and y < plan.height
        x += x_dir
        y += y_dir

        if frame is not None:
            t = plan.deepCopy()
            t.addResidence(R(x,y))
            frame.repaint(t)
            if slow: sleep(0.1)
    m = R(x - x_offset, y - y_offset)
    assert plan.correctlyPlaced(m)

    while plan.correctlyPlaced(m):
        m.minimumClearance += 0.1
    else:
        m.minimumClearance -= 0.1


    assert plan.correctlyPlaced(m)

    return m