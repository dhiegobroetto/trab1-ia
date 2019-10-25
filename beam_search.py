# ----- Dhiego Santos Broetto ----- #
# ---------- 2016204404 ----------- #
import timeit
import csv
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

def stateExpand(VT, states, T) :
    best_index = findBestState(VT, states, T)
    if(best_index >= 0) :
        states[best_index] += 1
        return True
    else :
        return False

def getValidState(VT, states, T) :
    if(getSizeState(VT, states) <= T) :
        return True
    else :
        return False

def findBestState(VT, states, T) :
    total_value = 0
    best_index = -1
    for i in range(0, len(states)) :
        states[i] += 1
        if(getValidState(VT, states, T)) :
            state_value = getValueState(VT, states)
            if(state_value > total_value) :
                best_index = i
                total_value = state_value
        states[i] -= 1
    return best_index

def hillClimbing(VT, states, T) :
    while(True) :
        if(not stateExpand(VT, states, T)) :
            return states

# ------------------------ Beam Search ------------------------ #

def addStateList(VT, states, T, states_list, queue_size) :
    for i in range(len(states)) :
        states[i] += 1
        if(getValidState(VT, states, T)) :
            if(len(states_list) < queue_size) :
                addToList(VT, states, states_list)
            else :
                sortList(states_list)
                if(states_list[0][1] < getValueState(VT, states)) :
                    states_list.pop(0)
                    addToList(VT, states, states_list)
        states[i] -= 1
    sortList(states_list)

def beam_search(VT, T, queue_size, timer = 0) :
    states_list = []
    best_state = [0] * len(VT)
    addStateList(VT, best_state, T, states_list, queue_size)
    while(states_list != []) :
        state = states_list.pop()
        if(state[1] >= getValueState(VT, best_state)) :
            best_state = state[0].copy()
        addStateList(VT, state[0], T, states_list, queue_size)
        if timer != 0 and (timeit.default_timer() - timer) > 120 :
            print("Beam Search exceeded time limit (120 seconds)\n")
            break
        
    return best_state

def addToList(VT, state, states_list) :
    state_copy = state.copy()
    state_aux = [state_copy, getValueState(VT, state), getSizeState(VT, state)]
    if state_aux not in states_list :
        states_list.append(state_aux)

def sortList(states_list) :
    states_list.sort(key = lambda pos: pos[1], reverse = False)

def beam_search_train(beam_search_hyperparams, params) :
    print("---- Beam Search ----")

    with open('results/beam.csv', mode='w') as csv_file:
        fieldnames = ['hp', 'value', 'time']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        results_beam = defaultdict(float)
        writer.writeheader()
        for beam_hp in beam_search_hyperparams :
            print("Begin HP => ", beam_hp)
            for param in params :
                start = timeit.default_timer()
                state = beam_search(param['vt'], param['t'], beam_hp, start)
                stop = timeit.default_timer()
                state_value = getValueState(param['vt'], state)
                if float(beam_hp) not in results_beam :
                    results_beam[float(beam_hp)] = []
                results_beam[float(beam_hp)].append([{'value': state_value, 'time': (stop - start)}])
                writer.writerow({'hp': beam_hp, 'value': state_value, 'time': (stop - start)})
                print("Value =>", state_value, " Total time => ", stop - start, " Params: (", param['vt'], param['t'], ")")
            print("Finish HP => ", beam_hp, " Result list => ", results_beam)
    return results_beam

# # Max size
# T = 19 
# # Objects array
# VT = [(1, 3), (4, 6), (5, 7)]
# T = 58
# VT = [(1,3),(4,6),(5,7),(3,4),(8,10),(4,8),(3,5),(6,9)]

# # Trivial solution
# states = [0] * len(VT)
# best_state_trivial = hillClimbing(VT, states, T)

# # Beam search
# states_list = []
# queue_size = 3
# best_state_beam = beam_search(VT, T, queue_size)

# # Results
# total_value_trivial = getValueState(VT, best_state_trivial)
# total_size_trivial = getSizeState(VT, best_state_trivial)

# total_value_beam = getValueState(VT, best_state_beam)
# total_size_beam = getSizeState(VT, best_state_beam)

# print("Trivial Solution")
# print ("[Total Value => ", total_value_trivial, ", Total Size => ", total_size_trivial, ", Best State => ", best_state_trivial)

# print("Beam Search")
# print ("[Total Value => ", total_value_beam, ", Total Size => ", total_size_beam, ", Best State => ", best_state_beam)