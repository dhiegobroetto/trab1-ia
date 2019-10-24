import timeit
import sys
import csv
from beam_search import beam_search_train
from simulated_annealing import simulated_annealing_train
from grasp import grasp_train
from genetic import genetic_algorithm_train

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

params = [
    {
        't' : 19,
        'vt' : [(1,3),(4,6),(5,7)]
    }
    ,
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
    # ,
    # {
    #     't' : 13890000,
    #     'vt' : [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2),(3,5),(7,10),(10,15),(13,20),(24,25),(29,37)]
    # },
    # {
    #     't' : 45678901,
    #     'vt' : [(1,3),(4,6),(5,7),(3,4),(2,6),(1,2),(3,5),(7,10),(10,15),(13,20),(15,20)]
    # }
]

def readTrainResults(filename) :
    read = pd.read_csv(filename)
    # results = []
    # for r in read :
    #     if 'hp' in r :

    return read
    return results
    # f = open(filename, 'r')
    # hp = 0
    # val = 0
    # time = 0.0
    # count = -1
    # for l in f :
    #     if "Begin HP =>" in l :
    #         count += 1
    #         hp = l.replace("Begin HP => ", "").replace('\n', "").split(", ")
    #         hp = [float(num) for num in hp]
    #         results.append([[], [hp]])
    #     if "Value =>" in l :
    #         val = int(l.split("Value => ")[1].split("  Total time => ")[0])
    #         time = float(l.split("Total time => ")[1].split('\n')[0])
    #         results[count][0].append([val, time])
    # f.close()
    # return results

def normalize(results) :
    best_value = 0
    for i in range(10) :
        val = []
        time = []
        for j in range(len(results)) :
            val.append(results[j][0][i][0])
            time.append(results[j][0][i][1])
        best_value = max(val)
        best_time = max(time)
        for j in range(len(results)) :
            results[j][0][i][0] /= best_value
            results[j][0][i][1] /= best_time
    for i in range(len(results)) :
        total = 0
        for j in range(len(results[i][0])) :
            total += results[i][0][j][0]
        results[i].append([total / len(results[i][0])])
    results.sort(key = lambda pos: pos[2], reverse = True)
    return results

# ----- Values methods ----- #

def get_formatted_values(results) :
    data = pd.DataFrame()
    for r1 in results :
        data[str(r1[1])] = r1[0]
    return data

def get_values(results) :
    values = []
    for r1 in results :
        v = []
        for r2 in r1[0] :
            v.append(r2[0])
        v.sort(reverse=True)
        values.append([v, r1[1][0]])
    return values[:10]

# ----- Times methods ----- #

def get_formatted_times(results) :
    data = pd.DataFrame()
    for r1 in results :
        data[str(r1[1])] = r1[1]
    return data

def get_times(results) :
    values = []
    for r1 in results :
        v = []
        for r2 in r1[0] :
            v.append(r2[1])
        v.sort(reverse=True)
        values.append([v, r1[1][0]])
    return values[:10]

# ----- Main ----- #

# Params from metaheuristics

# beam_search_hyperparams = [10, 25, 50, 100]
beam_search_hyperparams = [10, 25, 50, 100]

sa_to = [500, 100, 50]
sa_alpha = [0.95, 0.85, 0.7]
sa_max_iteration = [350, 500]

grasp_best_elements = [2, 5, 10, 15]
grasp_max_iteration = [50, 100, 200, 350, 500]

ga_population = [10, 20, 30]
ga_crossover = [0.75, 0.85, 0.95]
ga_mutation = [0.10, 0.20, 0.30]

# DataFrames to Boxplots

data_value_beam = pd.DataFrame()
data_value_sa = pd.DataFrame()
data_value_grasp = pd.DataFrame()
data_value_ga = pd.DataFrame()

data_time_beam = pd.DataFrame()
data_time_sa = pd.DataFrame()
data_time_grasp = pd.DataFrame()
data_time_ga = pd.DataFrame()

# Execution of meta-heuristics
# results_beam = beam_search_train(beam_search_hyperparams, params)
# results_sa = simulated_annealing_train(sa_to, sa_alpha, sa_max_iteration, params)
# results_grasp = grasp_train(grasp_best_elements, grasp_max_iteration, params)
# results_ga = genetic_algorithm_train(ga_population, ga_crossover, ga_mutation, params)

# Obtains data from txt file
results_beam = readTrainResults("results/beam.csv")
# df = pd.read_csv('results/beam.csv')
results_sa = readTrainResults("results/SA.csv")
results_grasp = readTrainResults("results/GRASP.csv")
results_ga = readTrainResults("results/GA.csv")

# print(results_beam)
# print("\n")
# print(results_beam2)

# Normalization of data
results_beam = normalize(results_beam)
results_sa = normalize(results_sa)
results_grasp = normalize(results_grasp)
results_ga = normalize(results_ga)

# ------ Values ------ #

# Getting values of results
# results_value_beam = get_values(results_beam)
# results_value_sa = get_values(results_sa)
# results_value_grasp = get_values(results_grasp)
# results_value_ga = get_values(results_ga)

# Getting values to DataFrame format
# data_value_beam = get_formatted_values(results_value_beam)
# data_value_sa = get_formatted_values(results_value_sa)
# data_value_grasp = get_formatted_values(results_value_grasp)
# data_value_ga = get_formatted_values(results_value_ga)

# sns.boxplot(data = data_value_beam)
# plt.title("Boxplot dos valores obtidos no treino da meta-heurística Beam Search")
# plt.show()
# sns.boxplot(data = data_value_sa)
# plt.title("Boxplot dos valores obtidos no treino da meta-heurística Simulated Annealing")
# plt.show()
# sns.boxplot(data = data_value_grasp)
# plt.title("Boxplot dos valores obtidos no treino da meta-heurística GRASP")
# plt.show()
# sns.boxplot(data = data_value_ga)
# plt.title("Boxplot dos valores obtidos no treino da meta-heurística Algoritmo Genético")
# plt.show()

# # ------ Times ------ #

# # Getting times of results
# results_time_beam = get_times(results_beam)
# results_time_sa = get_times(results_sa)
# results_time_grasp = get_times(results_grasp)
# results_time_ga = get_times(results_ga)

# # Getting times to DataFrame format
# data_time_beam = get_formatted_times(results_time_beam)
# data_time_sa = get_formatted_times(results_time_sa)
# data_time_grasp = get_formatted_times(results_time_grasp)
# data_time_ga = get_formatted_times(results_time_ga)

# sns.boxplot(data = data_time_beam)
# plt.title("Boxplot dos tempos obtidos no treino da meta-heurística Beam Search")
# plt.show()
# sns.boxplot(data = data_time_sa)
# plt.title("Boxplot dos tempos obtidos no treino da meta-heurística Simulated Annealing")
# plt.show()
# sns.boxplot(data = data_time_grasp)
# plt.title("Boxplot dos tempos obtidos no treino da meta-heurística GRASP")
# plt.show()
# sns.boxplot(data = data_time_ga)
# plt.title("Boxplot dos tempos obtidos no treino da meta-heurística Algoritmo Genético")
# plt.show()