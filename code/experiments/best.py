def report(r):

    best_v = None
    best = None
    for r2 in r:
        for r1 in r[r2]:
            #print r1
            v = r1[len(r1)-1]
            if best is None or v > best_v:
                best_v = v
                best = r1
   # print best
    return best

