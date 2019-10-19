import timeit

from beam_search import beam_search as bs

params = [
    {
        't' : 19,
        'vt' : [(1,3),(4,6),(5,7)]
    },
    {
        't' : 58,
        'vt' : [(1,3),(4,6),(5,7),(3,4)]
    },
    {
        't' : 58,
        'vt' : [(1,3),(4,6),(5,7),(3,4),(8,10),(4,8),(3,5),(6,9)]
    },
    {
        't' : 58,
        'vt' : [(1,3),(4,6),(5,7),(3,4),(8,10),(4,8),(3,5),(6,9),(2,1)]
    },
    {
        't' : 120,
        'vt' : [(1,2),(2,3),(4,5),(5,10),(14,15),(15,20),(24,25),(29,30),(50,50)]
    },
    {
        't' : 120,
        'vt' : [(1,2),(2,3),(3,5),(7,10),(10,15),(13,20),(24,25),(29,30),(50,50)]
    },
    {
        't' : 120,
        'vt' : [(24,25),(29,30),(50,50)]
    },
    {
        't' : 138,
        'vt' : [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2), (2,3), (3,5), (7,10), (10,15), (13,20), (24,25), (29,30), (50,50)]
    }
    ,
    {
        't' : 13890000,
        'vt' : [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2),(3,5),(7,10),(10,15),(13,20),(24,25),(29,37)]
    },
    {
        't' : 45678901,
        'vt' : [(1,3),(4,6),(5,7),(3,4),(2,6),(1,2),(3,5),(7,10),(10,15),(13,20),(15,20)]
    }
]

def getValueState(VT, states) :
    total_value = 0
    for i in range(0, len(states)) :
        total_value += VT[i][0] * states[i]
    return total_value

#Your statements here

f = open("results/beam.txt", "w+")
results_beam = []
beam_search_hyperparams = [10, 25, 50, 100]
i = 0
for beam_hp in beam_search_hyperparams :
    results_beam_param = []
    f.write("Begin HP => %d\n" % beam_hp)
    print("Begin HP => ", beam_hp)
    for param in params :
        start = timeit.default_timer()
        state = bs(param['vt'], param['t'], beam_hp, start)
        stop = timeit.default_timer()
        state_value = getValueState(param['vt'], state)
        results_beam_param.append({'value': state_value, 'time': (stop - start)})
        f.write("(%d): " % i)
        i+=1
        f.write("Value => %d " % (state_value))
        f.write(" Total time => %f\n" % (stop - start))
        print("(",i,") Value =>", state_value, " Total time => ", stop - start, " Params: (", param['vt'], param['t'], ")")
    results_beam.append([results_beam_param.copy(), beam_hp])
    results_beam_param.clear()
    i = 0
    print("Finish HP => ", beam_hp, " Result list => ", results_beam)
f.close()
