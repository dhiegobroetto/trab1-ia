# ----- Dhiego Santos Broetto ----- #
# ---------- 2016204404 ----------- #
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

def hill_climbing(VT, T, timer, time_limit) :
    best_value = [(0, 0)]
    states = [0] * len(VT)
    while(True) :
        if(not stateExpand(VT, states, T)) :
            return states
        if timer != 0 and (timeit.default_timer() - timer) > time_limit :
            print("Hill Climbing exceeded time limit\n")
            break

def hill_climbing_train(params, filename, time_limit) :
    print("---- Hill Climbing ----")
    with open(filename, mode='w') as csv_file:
        fieldnames = ['hp', 'value', 'time']
        writer = DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        results_hc = defaultdict(float)
        count = 0
        print("Begin HP => ", count)
        for param in params :
            start = timeit.default_timer()
            state = hill_climbing(param['vt'], param['t'], start, time_limit)
            stop = timeit.default_timer()
            state_value = getValueState(param['vt'], state)
            if float(count) not in results_hc :
                results_hc[float(count)] = []
            results_hc[float(count)].append([{'value': state_value, 'time': (stop - start)}])
            writer.writerow({'hp': float(count), 'value': state_value, 'time': (stop - start)})
            print("Value =>", state_value, " Total time => ", stop - start, " Params: (", param['vt'], param['t'], ")")
            count += 1
        print("Finish HP => ", count, " Result list => ", results_hc)
    return results_hc
