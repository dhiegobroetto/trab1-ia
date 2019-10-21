import timeit

from beam_search import beam_search as bs
from simulated_annealing import simulated_annealing as sa
from grasp import grasp
from genetic import genetic as ga

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

params = [
    {
        't' : 19,
        'vt' : [(1,3),(4,6),(5,7)]
    },
    {
        't' : 58,
        'vt' : [(1,3),(4,6),(5,7),(3,4)]
    },
    {
        't' : 58,
        'vt' : [(1,3),(4,6),(5,7),(3,4),(8,10),(4,8),(3,5),(6,9)]
    },
    {
        't' : 58,
        'vt' : [(1,3),(4,6),(5,7),(3,4),(8,10),(4,8),(3,5),(6,9),(2,1)]
    },
    {
        't' : 120,
        'vt' : [(1,2),(2,3),(4,5),(5,10),(14,15),(15,20),(24,25),(29,30),(50,50)]
    },
    {
        't' : 120,
        'vt' : [(1,2),(2,3),(3,5),(7,10),(10,15),(13,20),(24,25),(29,30),(50,50)]
    },
    {
        't' : 120,
        'vt' : [(24,25),(29,30),(50,50)]
    },
    {
        't' : 138,
        'vt' : [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2), (2,3), (3,5), (7,10), (10,15), (13,20), (24,25), (29,30), (50,50)]
    }
    ,
    {
        't' : 13890000,
        'vt' : [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2),(3,5),(7,10),(10,15),(13,20),(24,25),(29,37)]
    },
    {
        't' : 45678901,
        'vt' : [(1,3),(4,6),(5,7),(3,4),(2,6),(1,2),(3,5),(7,10),(10,15),(13,20),(15,20)]
    }
]

def getValueState(VT, states) :
    total_value = 0
    for i in range(0, len(states)) :
        total_value += VT[i][0] * states[i]
    return total_value

def beam_search_train(bean_search_hyperparams) :
    print("---- Beam Search ----")
    f = open("results/beam.txt", "w+")
    i = 0
    for beam_hp in beam_search_hyperparams :
        results_beam_param = []
        f.write("Begin HP => %d\n" % beam_hp)
        print("Begin HP => ", beam_hp)
        for param in params :
            start = timeit.default_timer()
            state = bs(param['vt'], param['t'], beam_hp, start)
            stop = timeit.default_timer()
            state_value = getValueState(param['vt'], state)
            results_beam_param.append({'value': state_value, 'time': (stop - start)})
            f.write("(%d): " % i)
            i+=1
            f.write("Value => %d " % (state_value))
            f.write(" Total time => %f\n" % (stop - start))
            print("(",i,") Value =>", state_value, " Total time => ", stop - start, " Params: (", param['vt'], param['t'], ")")
        results_beam.append([results_beam_param.copy(), beam_hp])
        results_beam_param.clear()
        i = 0
        print("Finish HP => ", beam_hp, " Result list => ", results_beam)
    f.close()
    return results_beam

def simulated_annealing_train(sa_to, sa_alpha, sa_max_iteration) :
    print("---- Simulated Annealing ----")
    f = open("results/SA.txt", "w+")
    i = 0
    for to in sa_to :
        for alpha in sa_alpha :
            for max_iteration in sa_max_iteration :
                results_sa_param = []
                f.write("Begin HP => %d, " % to)
                f.write("%f, " % alpha)
                f.write("%d\n" %  max_iteration)
                print("Begin HP => ", to, ", ", alpha, ", ", max_iteration)
                for param in params :
                    start = timeit.default_timer()
                    state = sa(param['vt'], param['t'], to, alpha, max_iteration, start)
                    stop = timeit.default_timer()
                    state_value = getValueState(param['vt'], state)
                    results_sa_param.append({'value': state_value, 'time': (stop - start)})
                    f.write("(%d): " % i)
                    i+=1
                    f.write("Value => %d " % (state_value))
                    f.write(" Total time => %f\n" % (stop - start))
                    print("(",i,") Value =>", state_value, " Total time => ", stop - start, " Params: (", param['vt'], param['t'], ")")
            results_sa.append([results_sa_param.copy(), [to, alpha, max_iteration]])
            results_sa_param.clear()
            i = 0
        print("Finish HP => ", [to, alpha, max_iteration], " Result list => ", results_sa)
    f.close()

def grasp_train(grasp_best_elements, grasp_max_iteration) :
    print("---- GRASP ----")
    f = open("results/GRASP.txt", "w+")
    i = 0
    for best_element in grasp_best_elements :
        for max_iteration in grasp_max_iteration :
            results_grasp_param = []
            f.write("Begin HP => %d, " % best_element)
            f.write("%d\n" % max_iteration)
            print("Begin HP => ", best_element, ", ", max_iteration)
            for param in params :
                start = timeit.default_timer()
                state = grasp(param['vt'], param['t'], best_element, max_iteration, start)
                stop = timeit.default_timer()
                state_value = getValueState(param['vt'], state)
                results_grasp_param.append({'value': state_value, 'time': (stop - start)})
                f.write("(%d): " % i)
                i+=1
                f.write("Value => %d " % (state_value))
                f.write(" Total time => %f\n" % (stop - start))
                print("(",i,") Value =>", state_value, " Total time => ", stop - start, " Params: (", param['vt'], param['t'], ")")
        results_grasp.append([results_grasp_param.copy(), [best_element, max_iteration]])
        results_grasp_param.clear()
        i = 0
        print("Finish HP => ", [best_element, max_iteration], " Result list => ", results_grasp)
    f.close()

def genetic_algorithm_train(ga_population, ga_crossover, ga_mutation) :
    print("---- Genetic Algorithm ----")
    f = open("results/GA.txt", "w+")
    i = 0
    for population in ga_population :
        for crossover in ga_crossover :
            for mutation in ga_mutation :
                results_ga_param = []
                f.write("Begin HP => %d, " % population)
                f.write("%f, " % crossover)
                f.write("%f\n" % mutation)
                print("Begin HP => ", population, ", ", crossover, ", ", mutation)
                for param in params :
                    start = timeit.default_timer()
                    state = ga(param['vt'], param['t'], population, 2, 100, crossover, mutation, start)
                    stop = timeit.default_timer()
                    state_value = getValueState(param['vt'], state)
                    results_ga_param.append({'value': state_value, 'time': (stop - start)})
                    f.write("(%d): " % i)
                    i+=1
                    f.write("Value => %d " % (state_value))
                    f.write(" Total time => %f\n" % (stop - start))
                    print("(",i,") Value =>", state_value, " Total time => ", stop - start, " Params: (", param['vt'], param['t'], ")")
            results_ga.append([results_ga_param.copy(), [population, crossover, mutation]])
            results_ga_param.clear()
            i = 0
        print("Finish HP => ", [population, crossover, mutation], " Result list => ", results_ga)
    f.close()

def readTrainResults(filename) :
    f = open(filename, 'r')
    hp = 0
    val = 0
    time = 0.0
    count = -1
    results = []
    for l in f :
        if "Begin HP =>" in l :
            count += 1
            hp = l.replace("Begin HP => ", "").replace('\n', "").split(", ")
            hp = [float(num) for num in hp]
            results.append([[], [hp]])
        if "Value =>" in l :
            val = int(l.split("Value => ")[1].split("  Total time => ")[0])
            time = float(l.split("Total time => ")[1].split('\n')[0])
            results[count][0].append([val, time])
    f.close()
    return results

def normalize(results) :
    for i in range(len(results)) :
        results[i][0].sort(reverse = True)
        best_value = results[i][0][0][0]
        for j in range(len(results[i][0])) :
            results[i][0][j][0] /= best_value
    return results

#Your statements here

# Params from metaheuristics

beam_search_hyperparams = [10, 25, 50, 100]

sa_to = [500, 100, 50]
sa_alpha = [0.95, 0.85, 0.7]
sa_max_iteration = [350, 500]

grasp_best_elements = [2, 5, 10, 15]
grasp_max_iteration = [50, 100, 200, 350, 500]

ga_population = [10, 20, 30]
ga_crossover = [0.75, 0.85, 0.95]
ga_mutation = [0.10, 0.20, 0.30]

# results_beam = beam_search_train(beam_search_hyperparams)

# results_sa = simulated_annealing_train(sa_to, sa_alpha, sa_max_iteration)

# results_grasp = grasp_train(grasp_best_elements, grasp_max_iteration)

# results_ga = genetic_algorithm_train(ga_population, ga_crossover, ga_mutation)

results_beam = readTrainResults("results/beam.txt")
results_sa = readTrainResults("results/SA.txt")
results_grasp = readTrainResults("results/GRASP.txt")
results_ga = readTrainResults("results/GA.txt")

results_beam = normalize(results_beam)
results_sa = normalize(results_sa)
results_grasp = normalize(results_grasp)
results_ga = normalize(results_ga)

results = []
results.append(results_beam)
results.append(results_sa)
results.append(results_grasp)
results.append(results_ga)

data = []
data = [a[0] for beam in results_beam for val in beam for a in val]
print(data)

hyperparams = []

for i in range(len(results)) : # roda 4 vezes (algoritmos)
    for j in range(len(results[i])) : # roda 4 vezes bs (combinação dos HP)
        avg_training = 0
        for training_result in results[i][j][0] : # + Combinações dos parâmetros / tamanho do vetor
            avg_training += training_result[0]
        avg_training /= len(results[i][j])
        results[i][j].append(avg_training)
    results[i].sort(key = lambda pos: pos[2], reverse = True)
    hyperparams.append(results[i][0][1][0])
# print("Valores dos hiperparâmetros selecionados para o teste:\nBeam Search: ", hyperparams[0], "\nSimulated Annealing: ", hyperparams[1], "\nGRASP: ", hyperparams[2], "\nGenetic Algorithm: ", hyperparams[3])
# print(results_ga)
sns.boxplot(data=data) # Also accepts numpy arrays
plt.show()