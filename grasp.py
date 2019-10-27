# ----- Dhiego Santos Broetto ----- #
# ---------- 2016204404 ----------- #

import math
import random
import timeit
import csv
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

def getValidState(VT, states, max_size) :
    if(getSizeState(VT, states) <= max_size) :
        return True
    else :
        return False

# ------ Roulette ------ #

def roulette(VT, states) :
    total = 0
    states_best = states.copy()
    for i in range(0, len(states_best)) :
        total += getValueState(VT, states_best[i])
    
    states_roulette = []
    for i in range(0, len(states_best)) :
        states_roulette.append([states_best[i],(getValueState(VT, states_best[i]) / total)])
    sortList(states_roulette)
    
    rand = random.uniform(0, 1)
    percent = 0
    for i in range(0, len(states_roulette)) :
        if rand <= (states_roulette[i][1] + percent) :
            return states_roulette[i][0]
        percent += states_roulette[i][1]
    return -1

def sortList(list) :
    list.sort(key = lambda pos: pos[1], reverse = False)

# ------ Neighborhood ------ #

def getValidPositiveNeighbor(VT, state, max_size) :
    states_list = []
    for i in range(0, len(state)):
        state_aux = state.copy()
        state_aux[i] += 1
        states_list.append(state_aux)
    return states_list

def defineValidNeighborhood(VT, state, max_size) :
    return getValidPositiveNeighbor(VT, state, max_size)

def getPositiveNeighbor(state, states_list) :
    for i in range(0, len(state)):
        state_aux = state.copy()
        state_aux[i] += 1
        states_list.append(state_aux)

def getNegativeNeighbor(state, states_list) :
    for i in range(0, len(state)):
        if state[i] > 0:
            state_aux = state.copy()
            state_aux[i] -= 1
            states_list.append(state_aux)

def defineNeighborhood(VT, state, states_list) :
    getPositiveNeighbor(state, states_list)
    getNegativeNeighbor(state, states_list)

# ------ Hill Climbing ------ #

def hill_climbing_roulette(VT, max_size, states_list, best_element, timer, time_limit) :
    best_value = 0
    best_state = [0] * len(VT)
    while(True) :
        states_list = defineValidNeighborhood(VT, best_state, max_size)
        states_list.sort(key = lambda state: getValueState(VT, state), reverse = True)
        state = roulette(VT, states_list[0:best_element])
        state_value = getValueState(VT, state)
        if getSizeState(VT, state) <= round(max_size/2) :
            if state_value > best_value :
                best_value = state_value
                best_state = state
        else :
            return best_state
        if timer != 0 and (timeit.default_timer() - timer) > time_limit :
            break
    return best_state

# ------ Local Search ------ #

def deepest_descent(VT, T, best_state_trivial, states_list) :
    best_state = best_state_trivial
    best_value = getValueState(VT, best_state_trivial)
    while(True) :
        find_best = False
        defineNeighborhood(VT, best_state, states_list)
        while(states_list != []) :
            state = states_list.pop()
            if(T >= getSizeState(VT, state)):
                if(best_value < getValueState(VT, state)) :
                    best_value = getValueState(VT, state)
                    best_state = state
                    find_best = True
                    states_list.clear()
        if(not find_best) :
            break
    return best_state

# ------ GRASP ------ #
def greedy_random_construct(VT, max_size, states_list, best_element, timer, time_limit) :
    return hill_climbing_roulette(VT, max_size, states_list, best_element, timer, time_limit)

def grasp(VT, max_size, best_element, max_iteration, timer = 0, time_limit = 0) :
    best_value = 0
    best_state = [0] * len(VT)
    states_list = [[0] * len(VT)]
    for i in range(max_iteration) :
        state = greedy_random_construct(VT, max_size, states_list, best_element, timer, time_limit)
        if timer != 0 and (timeit.default_timer() - timer) > time_limit :
            print("GRASP exceeded time limit\n")
            return state
        state_local = deepest_descent(VT, max_size, state, states_list)
        state_local_value = getValueState(VT, state_local)
        if getSizeState(VT, state_local) <= max_size :
            if state_local_value > best_value :
                best_value = state_local_value
                best_state = state_local
        if timer != 0 and (timeit.default_timer() - timer) > time_limit :
            print("GRASP exceeded time limit\n")
            return best_state
    return best_state

def grasp_train(grasp_best_elements, grasp_max_iteration, params, filename, time_limit) :
    print("---- GRASP ----")
    with open(filename, mode='w') as csv_file:
        fieldnames = ['hp', 'value', 'time']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        results_grasp = defaultdict(float)
        writer.writeheader()
        for best_element in grasp_best_elements :
            for max_iteration in grasp_max_iteration :
                print("Begin HP => ", best_element, ", ", max_iteration)
                for param in params :

                    start = timeit.default_timer()
                    state = grasp(param['vt'], param['t'], int(best_element), int(max_iteration), start, time_limit)
                    stop = timeit.default_timer()

                    state_value = getValueState(param['vt'], state)

                    key = str([float(best_element), float(max_iteration)])
                    if key not in results_grasp :
                        results_grasp[key] = []
                    results_grasp[key].append([{'value': state_value, 'time': (stop - start)}])
                    writer.writerow({'hp': [float(best_element), float(max_iteration)], 'value': state_value, 'time': (stop - start)})
                    print("Value =>", state_value, " Total time => ", stop - start, " Params: (", param['vt'], param['t'], ")")
            print("Finish HP => ", [best_element, max_iteration], " Result list => ", results_grasp)
    return results_grasp