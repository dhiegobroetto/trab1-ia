from csv import DictReader
from csv import DictWriter
from beam_search import beam_search_train
from simulated_annealing import simulated_annealing_train
from grasp import grasp_train
from genetic import genetic_algorithm_train
from collections import defaultdict

from seaborn import boxplot
from matplotlib.pyplot import show, title
from pandas import DataFrame

params = [
    {
        't' : 19,
        'vt' : [(1,3),(4,6),(5,7)]
    }
    ,
    {
        't' : 58,
        'vt' : [(1,3),(4,6),(5,7),(3,4)]
    }
    ,
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

def readTrainResults(filename) :
    with open(filename, newline='') as csvfile:
        r = DictReader(csvfile)
        results = defaultdict(str)
        for l in r :
            hp = l['hp'].split('[')[1].split(']')[0].split(', ')
            hp = [float(num) for num in hp]
            if str(hp) not in results :
                results[str(hp)] = []
            results[str(hp)] += [{'value': int(l['value']), 'time': float(l['time'])}]
    return results

def normalize(results) :
    best_value = 0
    for i in range(10) :
        val = []
        time = []
        for key in results :
            val.append(results[key][i]['value'])
            time.append(results[key][i]['time'])
        best_value = max(val)
        best_time = max(time)
        for key in results :
            results[key][i]['value'] /= best_value
            results[key][i]['time'] /= best_time
    for key in results :
        total = 0
        results[key].sort(key = lambda pos: pos['value'], reverse = True)
        for val in results[key] :
            total += val['value']
        results[key].insert(0, {'mean': ( total / len(results[key]) ) } )
    return results

def ordered_results(results) :
    res = []
    for key in results :
        res.append([results[key][0]['mean'], key, results[key]])
        results[key][0].pop('mean')
        res.sort(key = lambda pos: pos[0], reverse=True)
    return res

# ----- Values methods ----- #

def get_formatted_values(results) :
    data = DataFrame()
    for r1 in results :
        data[r1[1]] = r1[0]
    return data

def get_values(results) :
    values = []
    for r1 in results :
        v = []
        for r2 in r1[2] :
            if('value' in r2) :
                v.append(r2['value'])
        values.append([v, r1[1]])
    return values[:10]

# ----- Times methods ----- #

def get_formatted_times(results) :
    data = DataFrame()
    for r1 in results :
        data[r1[1]] = r1[0]
    return data

def get_times(results) :
    values = []
    for r1 in results :
        v = []
        for r2 in r1[2] :
            if('time' in r2) :
                v.append(r2['time'])
        values.append([v, r1[1]])
    return values[:10]

# ----- Main ----- #

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

# DataFrames to Boxplots

data_value_beam = DataFrame()
data_value_sa = DataFrame()
data_value_grasp = DataFrame()
data_value_ga = DataFrame()

data_time_beam = DataFrame()
data_time_sa = DataFrame()
data_time_grasp = DataFrame()
data_time_ga = DataFrame()

# Execution of meta-heuristics
results_beam = beam_search_train(beam_search_hyperparams, params, 'results/training/beam.csv', 120)
results_sa = simulated_annealing_train(sa_to, sa_alpha, sa_max_iteration, params, 'results/training/SA.csv', 120)
results_grasp = grasp_train(grasp_best_elements, grasp_max_iteration, params, 'results/training/GRASP.csv', 120)
results_ga = genetic_algorithm_train(ga_population, ga_crossover, ga_mutation, params, 'results/training/GA.csv', 120)

# # Obtains data from csv file
results_beam = readTrainResults("results/training/beam.csv")
results_sa = readTrainResults("results/training/SA.csv")
results_grasp = readTrainResults("results/training/GRASP.csv")
results_ga = readTrainResults("results/training/GA.csv")

# Normalization of data
results_beam = normalize(results_beam)
results_sa = normalize(results_sa)
results_grasp = normalize(results_grasp)
results_ga = normalize(results_ga)

ordered_beam = ordered_results(results_beam)
ordered_sa = ordered_results(results_sa)
ordered_grasp = ordered_results(results_grasp)
ordered_ga = ordered_results(results_ga)

# ------ Values ------ #

# Getting values of results
results_value_beam = get_values(ordered_beam)
results_value_sa = get_values(ordered_sa)
results_value_grasp = get_values(ordered_grasp)
results_value_ga = get_values(ordered_ga)

# Getting values to DataFrame format
data_value_beam = get_formatted_values(results_value_beam)
data_value_sa = get_formatted_values(results_value_sa)
data_value_grasp = get_formatted_values(results_value_grasp)
data_value_ga = get_formatted_values(results_value_ga)

# Getting best hyperparams from all algorithms
beam_hp = data_value_beam.mean().sort_values(ascending=False).keys()[0]
sa_hp = data_value_sa.mean().sort_values(ascending=False).keys()[0]
grasp_hp = data_value_grasp.mean().sort_values(ascending=False).keys()[0]
ga_hp = data_value_ga.mean().sort_values(ascending=False).keys()[0]

# Printing hyperparams into csv file
with open('results/hyperparams/training_results.csv', mode='w') as csv_file:
    fieldnames = ['beam', 'sa', 'grasp', 'ga']
    writer = DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'beam': beam_hp, 
                    'sa': sa_hp, 
                    'grasp': grasp_hp, 
                    'ga': ga_hp, })
print("Results:")
print("Beam Search: ", beam_hp)
print("Simulated Annealing: ", sa_hp)
print("GRASP: ", grasp_hp)
print("Genetic Algorithm: ", ga_hp)

# Boxplots of values
boxplot(data = data_value_beam)
title("Boxplot dos valores obtidos no treino da meta-heurística Beam Search")
show()
boxplot(data = data_value_sa)
title("Boxplot dos valores obtidos no treino da meta-heurística Simulated Annealing")
show()
boxplot(data = data_value_grasp)
title("Boxplot dos valores obtidos no treino da meta-heurística GRASP")
show()
boxplot(data = data_value_ga)
title("Boxplot dos valores obtidos no treino da meta-heurística Algoritmo Genético")
show()

# ------ Times ------ #

# Getting times of results
results_time_beam = get_times(ordered_beam)
results_time_sa = get_times(ordered_sa)
results_time_grasp = get_times(ordered_grasp)
results_time_ga = get_times(ordered_ga)

# Getting times to DataFrame format
data_time_beam = get_formatted_times(results_time_beam)
data_time_sa = get_formatted_times(results_time_sa)
data_time_grasp = get_formatted_times(results_time_grasp)
data_time_ga = get_formatted_times(results_time_ga)

# Boxplots of times
boxplot(data = data_time_beam)
title("Boxplot dos tempos obtidos no treino da meta-heurística Beam Search")
show()
boxplot(data = data_time_sa)
title("Boxplot dos tempos obtidos no treino da meta-heurística Simulated Annealing")
show()
boxplot(data = data_time_grasp)
title("Boxplot dos tempos obtidos no treino da meta-heurística GRASP")
show()
boxplot(data = data_time_ga)
title("Boxplot dos tempos obtidos no treino da meta-heurística Algoritmo Genético")
show()