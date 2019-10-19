# ----- Dhiego Santos Broetto ----- #
# ---------- 2016204404 ----------- #

from random import shuffle
import math
import random

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
    states_aux = []
    for i in range(0, len(states)) :
        total += getValueState(VT, states[i])
    for i in range(0, len(states)) :
        states_aux.append([states[i],(getValueState(VT, states[i]) / total)])
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

def getValidPositiveNeighbor(state, states_list, max_size) :
    for i in range(0, len(state)):
        state_aux = state.copy()
        state_aux[i] += 1
        if getSizeState(VT, state_aux) <= round(max_size/2) :
            states_list.append(state_aux)

def defineValidNeighborhood(VT, state, states_list, max_size) :
    getValidPositiveNeighbor(state, states_list, max_size)

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

def hill_climbing_roulette(VT, max_size, states_list) :
    best_value = 0
    best_state = [0] * len(VT)
    while(True) :
        find_best = False
        defineValidNeighborhood(VT, best_state, states_list, max_size)
        while(len(states_list) > 0) :
            state = roulette(VT, states_list)
            states_list.remove(state)
            state_value = getValueState(VT, state)
            if state_value > best_value :
                best_value = state_value
                best_state = state
                find_best = True
                break
        if not find_best :
            break
    return best_state

# ------ Local Search ------ #

def simple_descent(VT, T, best_state_trivial, states_list) :
    best_value = 0
    best_state = [0] * len(VT)
    while(True) :
        find_best = False
        defineNeighborhood(VT, best_state, states_list)
        shuffle(states_list)
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

def greedy_random_construct(VT, max_size, states_list) :
    return hill_climbing_roulette(VT, max_size, states_list)

def grasp(VT, max_size, states_list, max_iteration) :
    best_value = 0
    best_state = [0] * len(VT)
    for _ in range(max_iteration) :
        state = greedy_random_construct(VT, max_size, states_list)
        state_local = simple_descent(VT, max_size, state, states_list)
        state_local_value = getValueState(VT, state_local)
        if getSizeState(VT, state_local) <= max_size :
            if state_local_value > best_value :
                best_value = state_local_value
                best_state = state_local
    return best_state

# ------ Program ------ #

# Max size
max_size = 19
# Max iteration
max_iteration = 50
# Object array
VT = [(1, 3), (4, 6), (5, 7)]
states_list = []

best_state_grasp = grasp(VT, max_size, states_list, max_iteration)

# Results
total_value_grasp = getValueState(VT, best_state_grasp)
total_size_grasp = getSizeState(VT, best_state_grasp)

print("GRASP")
print ("[Total Value => ", total_value_grasp, ", Total Size => ", total_size_grasp, ", Best State => ", best_state_grasp)