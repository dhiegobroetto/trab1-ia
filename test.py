from csv import DictReader
from csv import DictWriter
from pandas import read_csv
from hill_climbing import hill_climbing_train
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
        't': 192,
        'vt': [(1,3),(4,6),(5,7)]
    },
    {
        't': 287,
        'vt': [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10)]
    },
    {
        't': 120,
        'vt': [(1,2),(2,3),(4,5),(5,10),(14,15),(13,20),(24,25),(29,30),(50,50)]
    },
    {
        't': 1240,
        'vt': [(1,2),(2,3),(3,5),(7,10),(10,15),(13,20),(24,25),(29,30),(50,50)]
    },
    {
        't': 104,
        'vt': [(25,26),(29,30),(49,50)]
    },
    {
        't': 138,
        'vt': [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8)]
    },
    {
        't': 13890,
        'vt': [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2), (2,3), (3,5), (7,10), (10,15), (13,20), (24,25),(29,30), (50,50)]
    },
    {
        't': 13890,
        'vt': [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2),(3,5),(7,10),(10,15),(13,20),(24,25),(29,37)]
    },
    {
        't': 190000,
        'vt': [(1,3),(4,6),(5,7)]
    },
    {
        't': 4567,
        'vt': [(1,3),(4,6),(5,7),(3,4),(2,6),(1,2),(3,5),(7,10),(10,15),(13,20),(15,20)]
    }
]

def normalize(results) :
    for i in range(len(results[0])) :
        val = []
        time = []
        for r1 in results :
            val.append(r1[i])
        best_value = max(val)
        for j in range(len(results)) :
            results[j][i] /= best_value
    return results


with open('results/hyperparams/training_results.csv', newline='') as csvfile:
    r = DictReader(csvfile)
    results = defaultdict(str)
    for l in r :
        beam_hp = l['beam']
        sa_hp = l['sa']
        grasp_hp = l['grasp']
        ga_hp = l['ga']

hp = beam_hp.split('[')[1].split(']')[0].split(', ')
beam_hp = [float(num) for num in hp]

hp = sa_hp.split('[')[1].split(']')[0].split(', ')
sa_hp = [float(num) for num in hp]

hp = grasp_hp.split('[')[1].split(']')[0].split(', ')
grasp_hp = [float(num) for num in hp]

hp = ga_hp.split('[')[1].split(']')[0].split(', ')
ga_hp = [float(num) for num in hp]

results_hc = hill_climbing_train(params, 'results/test/HC.csv', 300)
results_beam = beam_search_train(beam_hp, params, 'results/test/beam.csv', 300)
results_sa = simulated_annealing_train([sa_hp[0]], [sa_hp[1]], [sa_hp[2]], params, 'results/test/SA.csv', 300)
results_grasp = grasp_train([grasp_hp[0]], [grasp_hp[1]], params, 'results/test/GRASP.csv', 300)
results_ga = genetic_algorithm_train([ga_hp[0]], [ga_hp[1]], [ga_hp[2]], params, 'results/test/GA.csv', 300)

results_hc = read_csv('results/test/HC.csv', delimiter = ',')
results_beam = read_csv('results/test/beam.csv', delimiter = ',')
results_sa = read_csv('results/test/SA.csv', delimiter = ',')
results_grasp = read_csv('results/test/GRASP.csv', delimiter = ',')
results_ga = read_csv('results/test/GA.csv', delimiter = ',')

value_hc = results_hc['value']
time_hc = results_hc['time']
value_beam = results_beam['value']
time_beam = results_beam['time']
value_sa = results_sa['value']
time_sa = results_sa['time']
value_grasp = results_grasp['value']
time_grasp = results_grasp['time']
value_ga = results_ga['value']
time_ga = results_ga['time']

# ------ Normalize values ------ #
results = [ value_hc.values.tolist(), 
        value_beam.values.tolist(), 
        value_sa.values.tolist(), 
        value_grasp.values.tolist(), 
        value_ga.values.tolist() ]
normalized_values = normalize(results)
norm_value_hc = DataFrame()
norm_value_beam = DataFrame()
norm_value_sa = DataFrame()
norm_value_grasp = DataFrame()
norm_value_ga = DataFrame()
norm_value_hc['value'], norm_value_beam['value'], norm_value_sa['value'], norm_value_grasp['value'], norm_value_ga['value'] = normalized_values

# ------ Normalize times ------ #
results_time = [ time_hc.values.tolist(), 
        time_beam.values.tolist(), 
        time_sa.values.tolist(), 
        time_grasp.values.tolist(), 
        time_ga.values.tolist() ]
normalized_times = normalize(results_time)
norm_time_hc = DataFrame()
norm_time_beam = DataFrame()
norm_time_sa = DataFrame()
norm_time_grasp = DataFrame()
norm_time_ga = DataFrame()
norm_time_hc['time'], norm_time_beam['time'], norm_time_sa['time'], norm_time_grasp['time'], norm_time_ga['time'] = normalized_times

with open("results/test/results_table.csv", mode='w') as csv_file:
    fieldnames = ['hill', 'beam', 'sa', 'grasp', 'ga']
    writer = DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(
        {
            'hill': [
                    value_hc.mean(), 
                    value_hc.std(), 
                    norm_value_hc.mean().values.tolist()[0], 
                    norm_value_hc.std().values.tolist()[0],
                    time_hc.mean(),
                    time_hc.std()
            ],
            'beam': [
                    value_beam.mean(), 
                    value_beam.std(), 
                    norm_value_beam.mean().values.tolist()[0], 
                    norm_value_beam.std().values.tolist()[0],
                    time_beam.mean(),
                    time_beam.std()
            ],
            'sa': [
                    value_sa.mean(), 
                    value_sa.std(), 
                    norm_value_sa.mean().values.tolist()[0], 
                    norm_value_sa.std().values.tolist()[0],
                    time_sa.mean(),
                    time_sa.std()
            ],
            'grasp': [
                    value_grasp.mean(), 
                    value_grasp.std(), 
                    norm_value_grasp.mean().values.tolist()[0], 
                    norm_value_grasp.std().values.tolist()[0],
                    time_grasp.mean(),
                    time_grasp.std()
            ],
            'ga': [
                    value_ga.mean(), 
                    value_ga.std(), 
                    norm_value_ga.mean().values.tolist()[0], 
                    norm_value_ga.std().values.tolist()[0],
                    time_ga.mean(),
                    time_ga.std()
            ]
        }
    )

rank_abs = DataFrame()
rank_abs['hc'] = value_hc
rank_abs['beam'] = value_beam
rank_abs['sa'] = value_sa
rank_abs['grasp'] = value_grasp
rank_abs['ga'] = value_ga
probs = []
for i in range(len(rank_abs)) :
    probs.append(rank_abs.loc[[i]].sort_values(by=i, axis=1, ascending = False).columns.values.tolist())
print(probs)
rank_hc = 0
rank_beam = 0
rank_sa = 0
rank_grasp = 0
rank_ga = 0
for prob in probs :
    for i in range(len(prob)) :
        if 'hc' in prob[i] :
            rank_hc += i
        if 'beam' in prob[i] :
            rank_beam += i
        if 'sa' in prob[i] :
            rank_sa += i
        if 'grasp' in prob[i] :
            rank_grasp += i
        if 'ga' in prob[i] :
            rank_ga += i

rank_hc /= len(rank_abs)
rank_beam /= len(rank_abs)
rank_sa /= len(rank_abs)
rank_grasp /= len(rank_abs)
rank_ga /= len(rank_abs)

with open("results/test/ranking.csv", mode='w') as csv_file:
    fieldnames = ['hill', 'beam', 'sa', 'grasp', 'ga']
    writer = DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(
        {
            'hill': [
                rank_hc
            ],
            'beam': [
                rank_beam
            ],
            'sa': [
                rank_sa
            ],
            'grasp': [
                rank_grasp
            ],
            'ga': [
                rank_ga
            ]
        }
    )

# ------ Boxplots ------ #

norm_hc = DataFrame()
norm_hc['value'] = norm_value_hc['value']
norm_hc['time'] = results_hc['time']

norm_beam = DataFrame()
norm_beam['value'] = norm_value_beam['value']
norm_beam['time'] = results_beam['time']

norm_sa = DataFrame()
norm_sa['value'] = norm_value_sa['value']
norm_sa['time'] = results_sa['time']

norm_grasp = DataFrame()
norm_grasp['value'] = norm_value_grasp['value']
norm_grasp['time'] = results_grasp['time']

norm_ga = DataFrame()
norm_ga['value'] = norm_value_ga['value']
norm_ga['time'] = results_ga['time']

norm_values = DataFrame()
norm_values['Hill Climbing'] = norm_hc['value']
norm_values['Beam Search'] = norm_beam['value']
norm_values['Simulated Annealing'] = norm_sa['value']
norm_values['GRASP'] = norm_grasp['value']
norm_values['Genetic Algorithm'] = norm_ga['value']

norm_times = DataFrame()
norm_times['Hill Climbing'] = norm_hc['time']
norm_times['Beam Search'] = norm_beam['time']
norm_times['Simulated Annealing'] = norm_sa['time']
norm_times['GRASP'] = norm_grasp['time']
norm_times['Genetic Algorithm'] = norm_ga['time']

# Boxplots of values
boxplot(data = norm_values)
title("Boxplot dos valores obtidos no teste de cada meta-heurística")
show()
boxplot(data = norm_times)
title("Boxplot dos tempos obtidos no teste de cada meta-heurística")
show()