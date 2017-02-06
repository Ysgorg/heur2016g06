
from useful_scripts.get_corner_residence import get_corner_residence
from useful_scripts.new_grid import NewGrid


def corner_grid(plan,residence_type,rows,cols,x_anchor,y_anchor,x_dir,y_dir,frame,slow):

    m = get_corner_residence(residence_type,plan,x_anchor,y_anchor,x_dir,y_dir,frame,slow)

    g = NewGrid(plan,rows,cols,residence_type,plan.getMinimumDistance(m),[x_anchor,y_anchor],[x_dir,y_dir])

    for s in g.residences:
        for t in s:
            assert plan.correctlyPlaced(t, verbose=False)

    return g