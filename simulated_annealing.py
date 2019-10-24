# ----- Dhiego Santos Broetto ----- #
# ---------- 2016204404 ----------- #

from random import shuffle
import math
import random
import timeit

def getValueState(VT, states) :
    total_value = 0
    for i in range(0, len(states)) :
        total_value += VT[i][0] * states[i]
    return total_value

def getSizeState(VT, states) :
    total_size = 0
    for i in range(0, len(states)) :
        total_size += VT[i][1] * states[i]
    return total_size

# ------------------------ Simulated Annealing ------------------------ #

def getPositiveNeighbor(VT, state, states_list, max_size) :
    for i in range(0, len(state)):
        state_aux = state.copy()
        state_aux[i] += 1
        if(getSizeState(VT, state_aux) <= max_size) :
            states_list.append(state_aux)

def getNegativeNeighbor(VT, state, states_list, max_size) :
    for i in range(0, len(state)):
        if state[i] > 0:
            state_aux = state.copy()
            state_aux[i] -= 1
            if(getValueState(VT, state_aux) != 0 and getSizeState(VT, state_aux) <= max_size) :
                states_list.append(state_aux)


def defineNeighborhood(VT, state, states_list, max_size) :
    getPositiveNeighbor(VT, state, states_list, max_size)
    getNegativeNeighbor(VT, state, states_list, max_size)

def probabilityState(worst_case, state, t) :
    p = 1 / math.exp(1) ** ((worst_case - state) / t)
    r = random.uniform(0, 1)
    return r < p

def simulated_annealing(VT, max_size, t, alpha, max_iteration, timer = 0) :
    best_value = 0
    best_state = []
    states_list = []
    iterate_value = 0
    iterate_state = [0] * len(VT)
    while(t >= 1) :
        for _ in range(max_iteration) :
            defineNeighborhood(VT, iterate_state, states_list, max_size)
            shuffle(states_list)
            state = states_list.pop()
            if(max_size >= getSizeState(VT, state)):
                if(getValueState(VT, state) > iterate_value) :
                    iterate_value = getValueState(VT, state)
                    iterate_state = state
                    if(best_value < getValueState(VT, state)) :
                        best_value = getValueState(VT, state)
                        best_state = state
                        states_list.clear()
                else :
                    if(probabilityState(getValueState(VT, state), getValueState(VT, iterate_state), t)) :
                        iterate_value = getValueState(VT, state)
                        iterate_state = state
            if timer != 0 and (timeit.default_timer() - timer) > 120 :
                break
        t = alpha * t
        if timer != 0 and (timeit.default_timer() - timer) > 120 :
            print("Simulated Annealing exceeded time limit (120 seconds)\n")
            break
    return best_state

def simulated_annealing_train(sa_to, sa_alpha, sa_max_iteration, params) :
    print("---- Simulated Annealing ----")
    f = open("results/SA.txt", "w+")
    i = 0
    results_sa = []
    for to in sa_to :
        for alpha in sa_alpha :
            for max_iteration in sa_max_iteration :
                results_sa_param = []
                f.write("Begin HP => %d, " % to)
                f.write("%f, " % alpha)
                f.write("%d\n" %  max_iteration)
                print("Begin HP => ", to, ", ", alpha, ", ", max_iteration)
                for param in params :
                    start = timeit.default_timer()
                    state = simulated_annealing(param['vt'], param['t'], to, alpha, max_iteration, start)
                    stop = timeit.default_timer()
                    state_value = getValueState(param['vt'], state)
                    results_sa_param.append({'value': state_value, 'time': (stop - start)})
                    f.write("(%d): " % i)
                    i+=1
                    f.write("Value => %d " % (state_value))
                    f.write(" Total time => %f\n" % (stop - start))
                    print("(",i,") Value =>", state_value, " Total time => ", stop - start, " Params: (", param['vt'], param['t'], ")")
            results_sa.append([results_sa_param.copy(), [to, alpha, max_iteration]])
            results_sa_param.clear()
            i = 0
        print("Finish HP => ", [to, alpha, max_iteration], " Result list => ", results_sa)
    f.close()
    return results_sa

# # Max size
# max_size = 19 
# # Object array
# VT = [(1, 3), (4, 6), (5, 7)]
# t = 100
# alpha = 0.5
# max_iteration = 40

# # Simulated Annealing
# states_list = []
# best_simulated_annealing = simulated_annealing(VT, max_size, t, alpha, max_iteration)

# # Results
# total_value_simple = getValueState(VT, best_simulated_annealing)
# total_size_simple = getSizeState(VT, best_simulated_annealing)

# print("Simulated Annealing")
# print ("[Total Value => ", total_value_simple, ", Total Size => ", total_size_simple, ", Best State => ", best_simulated_annealing)