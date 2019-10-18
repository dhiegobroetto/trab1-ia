# ----- Dhiego Santos Broetto ----- #
# ---------- 2016204404 ----------- #

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
            if(len(states_list) <= queue_size) :
                addToList(VT, states, states_list)
        states[i] -= 1
    sortList(states_list)

def beam_search(VT, T, states_list, queue_size) :
    best_state = [0] * len(VT)
    addStateList(VT, best_state, T, states_list, queue_size)
    while(states_list != []) :
        state = states_list.pop()
        if(state[1] >= getValueState(VT, best_state)) :
            best_state = state[0].copy()
        addStateList(VT, state[0], T, states_list, queue_size)
    return best_state

def addToList(VT, state, states_list) :
    state_copy = state.copy()
    states_list.append([state_copy, getValueState(VT, state), getSizeState(VT, state)])

def sortList(states_list) :
    states_list.sort(key = lambda pos: pos[1], reverse = False)

# Max size
T = 19 
# Objects array
VT = [(1, 3), (4, 6), (5, 7)]

# Trivial solution
states = [0] * len(VT)
best_state_trivial = hillClimbing(VT, states, T)

# Beam search
states_list = []
queue_size = 5
best_state_beam = beam_search(VT, T, states_list, queue_size)

# Results
total_value_trivial = getValueState(VT, best_state_trivial)
total_size_trivial = getSizeState(VT, best_state_trivial)

total_value_beam = getValueState(VT, best_state_beam)
total_size_beam = getSizeState(VT, best_state_beam)

print("Trivial Solution")
print ("[Total Value => ", total_value_trivial, ", Total Size => ", total_size_trivial, ", Best State => ", best_state_trivial)

print("Beam Search")
print ("[Total Value => ", total_value_beam, ", Total Size => ", total_size_beam, ", Best State => ", best_state_beam)