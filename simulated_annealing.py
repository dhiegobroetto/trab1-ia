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

def simulated_annealing(VT, max_size, t, alpha, states_list, max_iteration) :
    best_value = 0
    best_state = []
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

        t = alpha * t
    return best_state

# Max size
max_size = 19 
# Object array
VT = [(1, 3), (4, 6), (5, 7)]
t = 100
alpha = 0.5
max_iteration = 40

# Simulated Annealing
states_list = []
best_simulated_annealing = simulated_annealing(VT, max_size, t, alpha, states_list, max_iteration)

# Results
total_value_simple = getValueState(VT, best_simulated_annealing)
total_size_simple = getSizeState(VT, best_simulated_annealing)

print("Simulated Annealing")
print ("[Total Value => ", total_value_simple, ", Total Size => ", total_size_simple, ", Best State => ", best_simulated_annealing)