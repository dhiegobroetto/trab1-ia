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
    best_state = []
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

def crossover(VT, states, crossover_ratio) :
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

def mutate(VT, states, mutation_ratio) :
    for _ in range(len(states)) :
        mutation_probability = random.uniform(0, 1)
        if(mutation_ratio >= mutation_probability) :
            state = random.randint(0, len(states) -1)
            states[state][0] = mutateState(states[state][0])
            states[state][1] = getValueState(VT, states[state][0])
    return states

def genetic(VT, max_size, population_size, k, max_iteration, crossover_ratio, mutation_ratio):
    population = []
    best_solution = [0] * len(VT)
    best_state = []
    best_value = getValueState(VT, best_solution)
    for _ in range(population_size):
        state = generateRandomState(VT, max_size)
        value = getValueState(VT, state)
        population.append([state, value])
    for _ in range(max_iteration) :
        sortList(population)
        state = population.pop()
        if(max_size >= getSizeState(VT, state[0])):
            if(best_value < state[1]) :
                best_state = state
        population = tournamentSearch(VT, max_size, population, k)
        population = crossover(VT, population, crossover_ratio)
        population = mutate(VT, population, mutation_ratio)
        population.append(state)
        if(len(population) > 1 ) : 
            population = [state for state in population if getSizeState(VT, state[0]) <= max_size]
        if(len(population) < population_size) :
            for _ in range(population_size - len(population)):
                state = generateRandomState(VT, max_size)
                value = getValueState(VT, state)
                population.append([state, value])
    return best_state

def generateRandomState(VT, max_size) :
    state = []
    while(True) :
        state = [random.randint(0, 3) for i in range(3)]
        if(getSizeState(VT, state) <= max_size and getValueState(VT, state) != 0) :
            return state

def sortList(population) :
    population.sort(key = lambda pos: pos[1], reverse = False)

# Max size
max_size = 19 
# Object array
VT = [(1, 3), (4, 6), (5, 7)]
population_size = 5

max_iteration = 100
crossover_ratio = 0.5
mutation_ratio = 0.1
k = 2

# Genetic
states_list = []
best_genetic = genetic(VT, max_size, population_size, k, max_iteration, crossover_ratio, mutation_ratio)

# Results
total_value_genetic = best_genetic[1]
total_size_genetic = getSizeState(VT, best_genetic[0])

print("Genetic Algorithm")
print ("[Total Value => ", total_value_genetic, ", Total Size => ", total_size_genetic, ", Best State => ", best_genetic)