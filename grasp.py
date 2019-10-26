# ----- Dhiego Santos Broetto ----- #
# ---------- 2016204404 ----------- #

from random import shuffle
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

def roulette(VT, states, best_element) :
    total = 0
    states_aux = states.copy()

    for i in range(len(states_aux)) :
        states_aux[i] = [states_aux[i], getValueState(VT, states_aux[i])]
    states_aux.sort(key = lambda pos: pos[1], reverse = True)
    states_best = states_aux[0:best_element].copy()
    for i in range(len(states_best)) :
        states_best[i] = states_best[i][0]

    for i in range(0, len(states_best)) :
        total += getValueState(VT, states_best[i])
    
    for i in range(0, len(states_best)) :
        states_aux.append([states_best[i],(getValueState(VT, states_best[i]) / total)])
    sortList(states_aux)
    
    rand = random.uniform(0, 1)
    percent = 0
    for i in range(0, len(states_aux)) :
        if rand <= (states_aux[i][1] + percent) :
            return states_aux[i][0]
        percent += states_aux[i][1]
    return -1

def sortList(list) :
    list.sort(key = lambda pos: pos[1], reverse = False)

# ------ Neighborhood ------ #

def getValidPositiveNeighbor(VT, state, states_list, max_size) :
    for i in range(0, len(state)):
        state_aux = state.copy()
        state_aux[i] += 1
        if getSizeState(VT, state_aux) <= round(max_size/2) :
            states_list.append(state_aux)

def defineValidNeighborhood(VT, state, states_list, max_size) :
    getValidPositiveNeighbor(VT, state, states_list, max_size)

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

def hill_climbing_roulette(VT, max_size, states_list, best_element, timer) :
    best_value = 0
    best_state = [0] * len(VT)
    while(True) :
        find_best = False
        defineValidNeighborhood(VT, best_state, states_list, max_size)
        while(len(states_list) > 0) :
            state = roulette(VT, states_list, best_element)
            states_list.remove(state)
            state_value = getValueState(VT, state)
            if state_value > best_value :
                best_value = state_value
                best_state = state
                states_list.clear()
                find_best = True
                break
            if timer != 0 and (timeit.default_timer() - timer) > 120 :
                break
        if not find_best :
            break
        if timer != 0 and (timeit.default_timer() - timer) > 120 :
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

def greedy_random_construct(VT, max_size, states_list, best_element, timer) :
    return hill_climbing_roulette(VT, max_size, states_list, best_element, timer)

def grasp(VT, max_size, best_element, max_iteration, timer = 0) :
    best_value = 0
    best_state = [0] * len(VT)
    states_list = []
    for i in range(max_iteration) :
        state = greedy_random_construct(VT, max_size, states_list, best_element, timer)
        if timer != 0 and (timeit.default_timer() - timer) > 120 :
            print("GRASP exceeded time limit (120 seconds)\n")
            break
        state_local = deepest_descent(VT, max_size, state, states_list)
        state_local_value = getValueState(VT, state_local)
        if getSizeState(VT, state_local) <= max_size :
            if state_local_value > best_value :
                best_value = state_local_value
                best_state = state_local
        if timer != 0 and (timeit.default_timer() - timer) > 120 :
            print("GRASP exceeded time limit (120 seconds)\n")
            break
    return best_state

def grasp_train(grasp_best_elements, grasp_max_iteration, params) :
    print("---- GRASP ----")
    with open('results/training/GRASP.csv', mode='w') as csv_file:
        fieldnames = ['hp', 'value', 'time']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        results_grasp = defaultdict(float)
        writer.writeheader()
        for best_element in grasp_best_elements :
            for max_iteration in grasp_max_iteration :
                print("Begin HP => ", best_element, ", ", max_iteration)
                for param in params :

                    start = timeit.default_timer()
                    state = grasp(param['vt'], param['t'], best_element, max_iteration, start)
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