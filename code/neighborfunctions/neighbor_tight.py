from src.validstate_tight import validstate_tight
from src.GroundplanFrame import GroundplanFrame

def neighbor_tight(state, temperature):
    MIN = 10.0
    MAX = 80.0

    def generate_state(i,j,k):
        state = validstate_tight(base.deepCopy(),float(i)/10,float(j)/10,float(k/10),visualize=False).getPlan().deepCopy()
        return state

    def factor():
        v = random()*tempertature
        if random()>0.5:v*=-1.0
        return v

    def set_param(p,f):
        if random()<0.9:
            p += f*(0.5)
            if p > MAX: p = MAX
            elif p < MIN : p = MIN
        return p

    print "Starting"
    a = state[0]
    b = state[1]
    c = state[2]

    i = set_param(a,factor())
    j = set_param(b,factor())
    k = set_param(c,factor())

    #print "a to i",a,i
    #while True:pass

    print "Generating state"
    return generate_state(i,j,k)
