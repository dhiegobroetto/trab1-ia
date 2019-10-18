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
    best_value = [(0, 0)]
    while(True) :
        if(not stateExpand(VT, states, T)) :
            return states

# Max size
T = 19 
# Objects array
VT = [(1, 3), (4, 6), (5, 7)]

# Hill Climbing
states = [0] * len(VT)
best_state = hillClimbing(VT, states, T)

# Results
total_value = getValueState(VT, best_state)
total_size = getSizeState(VT, best_state)
print("Hill Climbing")
print ("[Total Value => ", total_value, ", Total Size => ", total_size, ", Best State => ", best_state)