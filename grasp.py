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

def roulette(VT, states) :
# TODO: Fazer a roleta ainda
    total = 0
    states_aux = []
    for i in range(0, len(states)) :
        total += getValueState(VT, states[i])
    for i in range(0, len(states)) :
        states_aux += ([states[i],(getValueState(VT, states[i]) / total)])
    sortList(states_aux)
    rand = random.randint(0, 1)
    percent = 0
    for i in range(0, len(states_aux)) :
        if (rand + percent) >= states_aux[i][1] :
            return i
        percent += states_aux[i][1]
    return -1
def sortList(list) :
    list.sort(key = lambda pos: pos[1], reverse = False)
    # state = []
    # while(True) :
    #     state = [random.randint(0, 3) for i in range(3)]
    #     if(getSizeState(VT, state) <= max_size and getValueState(VT, state) != 0) :
    #         return state

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
    # getNegativeNeighbor(state, states_list)  

# Max size
max_size = 19
# Object array
VT = [(1, 3), (4, 6), (5, 7)]
states_list = []
defineNeighborhood(VT, [0]*len(VT), states_list)

print(roulette(VT, states_list))