# ----- Dhiego Santos Broetto ----- #
# ---------- 2016204404 ----------- #

from random import shuffle
import math
import random
import timeit
from csv import DictWriter
from collections import defaultdict

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
    if (t < 0.1):
        return 0
    p = 1 / math.exp((-1 * (worst_case - state)) / t)
    r = random.uniform(0, 1)
    return r < p

def simulated_annealing(VT, max_size, t, alpha, max_iteration, timer = 0, time_limit = 0) :
    best_value = 0
    best_state = []
    states_list = []
    iterate_value = 0
    iterate_state = [0] * len(VT)
    while(t > 0.001) :
        for _ in range(max_iteration) :
            defineNeighborhood(VT, iterate_state, states_list, max_size)
            index = random.randint(0, len(states_list) -1)
            state = states_list[index]
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
            if timer != 0 and (timeit.default_timer() - timer) > time_limit :
                break
        t = alpha * t
        if timer != 0 and (timeit.default_timer() - timer) > time_limit :
            print("Simulated Annealing exceeded time limit\n")
            break
    return best_state

def simulated_annealing_train(sa_to, sa_alpha, sa_max_iteration, params, filename, time_limit) :
    print("---- Simulated Annealing ----")
    with open(filename, mode='w') as csv_file:
        fieldnames = ['hp', 'value', 'time']
        writer = DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        results_sa = defaultdict(float)
        for to in sa_to :
            for alpha in sa_alpha :
                for max_iteration in sa_max_iteration :
                    print("Begin HP => ", to, ", ", alpha, ", ", max_iteration)
                    for param in params :
                        start = timeit.default_timer()
                        state = simulated_annealing(param['vt'], param['t'], to, alpha, int(max_iteration), start, time_limit)
                        stop = timeit.default_timer()
                        state_value = getValueState(param['vt'], state)
                        key = str([float(to), float(alpha), float(max_iteration)])
                        if key not in results_sa :
                            results_sa[key] = []
                        results_sa[key].append([{'value': state_value, 'time': (stop - start)}])
                        writer.writerow({'hp': [float(to), float(alpha), float(max_iteration)], 'value': state_value, 'time': (stop - start)})
                        print("Value =>", state_value, " Total time => ", stop - start, " Params: (", param['vt'], param['t'], ")")
            print("Finish HP => ", [to, alpha, max_iteration], " Result list => ", results_sa)
    return results_sa