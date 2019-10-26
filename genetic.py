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

def getValidState(VT, states, max_size) :
    if(getSizeState(VT, states) <= max_size) :
        return True
    else :
        return False

# ------------------------ Genetic ------------------------ #

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

def findBestState(VT, states, max_size) :
    total_value = 0
    best_state = states[0]
    if(len(states) == 0) : return best_state
    for state in states :
        if(getValidState(VT, state[0], max_size)) :
            if(state[1] > total_value) :
                best_state = state
                total_value = state[1]
    return best_state


def tournamentSearch(VT, max_size, population, k) :
    best_genetic = []
    if(len(population) == 0) :
        return best_genetic
    shuffle(population)
    subgroups = [population[i:i + k] for i in range(0, len(population), k)]
    for group in subgroups :
        best_genetic.append(findBestState(VT, group, max_size))
    return best_genetic


def defineNeighborhood(VT, state, states_list) :
    getPositiveNeighbor(state, states_list)
    getNegativeNeighbor(state, states_list)   

def crossStates(state1, state2) :
    middle_index = round(len(state1)/2)
    child1 = state1[0:middle_index] + state2[middle_index:len(state2)]
    child2 = state2[0:middle_index] + state1[middle_index:len(state1)]
    return child1, child2

def crossover(VT, states, crossover_ratio, timer = 0, time_limit = 0) :
    for _ in range(round(len(states)/2)) :
        crossover_probability = random.uniform(0, 1)
        if(crossover_ratio >= crossover_probability) :
            state1 = random.randint(0,len(states)-1)
            state2 = random.randint(0,len(states)-1)
            while state1 == state2:
                state2 = random.randint(0,len(states)-1)
            states[state1][0], states[state2][0] = crossStates(states[state1][0], states[state2][0])
            states[state1][1] = getValueState(VT, states[state1][0])
            states[state2][1] = getValueState(VT, states[state2][0])
        if timer != 0 and (timeit.default_timer() - timer) > time_limit :
            break
    return states

def mutateState(state) :
    value1 = random.randint(0,len(state)-1)
    value2 = random.randint(0,len(state)-1)
    while value1 == value2:
        value2 = random.randint(0,len(state)-1)
    aux = state[value1]
    state[value1] = state[value2]
    state[value2] = aux
    return state

def mutate(VT, states, mutation_ratio, timer = 0, time_limit = 0) :
    for _ in range(len(states)) :
        mutation_probability = random.uniform(0, 1)
        if(mutation_ratio >= mutation_probability) :
            state = random.randint(0, len(states) -1)
            states[state][0] = mutateState(states[state][0])
            states[state][1] = getValueState(VT, states[state][0])
        if timer != 0 and (timeit.default_timer() - timer) > time_limit :
            break
    return states

def genetic(VT, max_size, population_size, k, max_iteration, crossover_ratio, mutation_ratio, timer = 0, time_limit = 0):
    population = []
    best_solution = [0] * len(VT)
    best_state = []
    best_value = getValueState(VT, best_solution)
    for _ in range(population_size):
        state = generateRandomState(VT, max_size)
        value = getValueState(VT, state)
        population.append([state, value])
        if timer != 0 and (timeit.default_timer() - timer) > time_limit :
            break
    if timer != 0 and (timeit.default_timer() - timer) > time_limit :
        print("Genetic Algorithm exceeded time limit\n")
    else : 
        for _ in range(int(max_iteration)) :
            sortList(population)
            state = population.pop()
            if(max_size >= getSizeState(VT, state[0])):
                if(best_value < state[1]) :
                    best_state = state[0]
            population = tournamentSearch(VT, max_size, population, k)
            population = crossover(VT, population, crossover_ratio, timer, time_limit)
            if timer != 0 and (timeit.default_timer() - timer) > time_limit :
                print("Genetic Algorithm exceeded time limit\n")
                break
            population = mutate(VT, population, mutation_ratio, timer, time_limit)
            if timer != 0 and (timeit.default_timer() - timer) > time_limit :
                print("Genetic Algorithm exceeded time limit\n")
                break
            population.append(state)
            if(len(population) > 1 ) :
                population = [state for state in population if len(state) != 0 and state[1] != 0 and getSizeState(VT, state[0]) <= max_size]
            if(len(population) < population_size) :
                for _ in range(population_size - len(population)):
                    state = generateRandomState(VT, max_size)
                    value = getValueState(VT, state)
                    population.append([state, value])
                    if timer != 0 and (timeit.default_timer() - timer) > time_limit :
                        break
            if timer != 0 and (timeit.default_timer() - timer) > time_limit :
                print("Genetic Algorithm exceeded time limit\n")
                break
    return best_state

def generateRandomState(VT, max_size) :
    state = []
    state = [random.randint(0, 1000000) for i in range(3)]
    if(getSizeState(VT, state) <= max_size and getValueState(VT, state) != 0) :
        return state
    else :
        state = state = [random.randint(0, 10000) for i in range(3)]
        if(getSizeState(VT, state) <= max_size and getValueState(VT, state) != 0) :
            return state
        else :
            state = state = [random.randint(0, 100) for i in range(3)]
            if(getSizeState(VT, state) <= max_size and getValueState(VT, state) != 0) :
                return state
            else :
                state = state = [random.randint(0, 10) for i in range(3)]
                if(getSizeState(VT, state) <= max_size and getValueState(VT, state) != 0) :
                    return state
                else :
                    state = state = [random.randint(0, 3) for i in range(3)]
                    if(getSizeState(VT, state) <= max_size and getValueState(VT, state) != 0) :
                        return state
                    else :
                        return [1] * len(VT)      

def sortList(population) :
    population.sort(key = lambda pos: pos[1], reverse = False)

def genetic_algorithm_train(ga_population, ga_crossover, ga_mutation, params, filename, time_limit) :
    print("---- Genetic Algorithm ----")
    with open(filename, mode='w') as csv_file:
        fieldnames = ['hp', 'value', 'time']
        writer = DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        results_ga = defaultdict(float)
        for population in ga_population :
            for crossover in ga_crossover :
                for mutation in ga_mutation :
                    print("Begin HP => ", population, ", ", crossover, ", ", mutation)
                    for param in params :
                        start = timeit.default_timer()
                        state = genetic(param['vt'], param['t'], int(population), 2, 100, crossover, mutation, start, time_limit)
                        stop = timeit.default_timer()
                        state_value = getValueState(param['vt'], state)
                        key = str([float(population), float(crossover), float(mutation)])
                        if key not in results_ga :
                            results_ga[key] = []
                        results_ga[key].append([{'value': state_value, 'time': (stop - start)}])
                        writer.writerow({'hp': [float(population), float(crossover), float(mutation)], 'value': state_value, 'time': (stop - start)})
                        print("Value =>", state_value, " Total time => ", stop - start, " Params: (", param['vt'], param['t'], ")")
        print("Finish HP => ", [population, crossover, mutation], " Result list => ", results_ga)
    return results_ga