from csv import DictReader
from csv import DictWriter
from hill_climbing import hill_climbing_train
from beam_search import beam_search_train
from simulated_annealing import simulated_annealing_train
from grasp import grasp_train
from genetic import genetic_algorithm_train
from collections import defaultdict

# from seaborn import boxplot
# from matplotlib.pyplot import show, title
# from pandas import DataFrame

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

# results_hc = hill_climbing_train(params, 'results/test/HC.csv', 300)
# results_beam = beam_search_train(beam_hp, params, 'results/test/beam.csv', 300)
# results_sa = simulated_annealing_train([sa_hp[0]], [sa_hp[1]], [sa_hp[2]], params, 'results/test/SA.csv', 300)
# results_grasp = grasp_train([grasp_hp[0]], [grasp_hp[1]], params, 'results/test/GRASP.csv', 300)
results_ga = genetic_algorithm_train([10], [0,75], [0.10], params, 'results/test/GA.csv', 300)
