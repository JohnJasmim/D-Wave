#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://quantumcomputing.stackexchange.com/questions/1451/how-do-you-write-a-simple-program-for-a-d-wave-device

from dwave_sapi2.core import solve_ising
from dwave_sapi2.embedding import find_embedding, embed_problem, unembed_answer
from dwave_sapi2.util import get_hardware_adjacency
from dwave_sapi2.remote import RemoteConnection

# In order to connect to the D-Wave Solver API you will need a valid API token for their SAPI solver, the SAPI URL and you need to decide which quantum processor you want to use:
DWAVE_SAPI_URL = 'https://cloud.dwavesys.com/sapi'
DWAVE_TOKEN = [your D-Wave API token]
DWAVE_SOLVER = 'DW_2000Q_VFYC_1'

# define h as a list and J as a dictionary:
J = {(0,4): 1, (4,3): 1, (3,7): 1, (7,0): 1}
h = [-1,0,0,0,0,0,0,0,0]

# h has 8 entries since we use qubits 0 to 7. We now establish connection to the Solver API and request the D-Wave 2000Q VFYC solver
connection = RemoteConnection(DWAVE_SAPI_URL, DWAVE_TOKEN)
solver = connection.get_solver(DWAVE_SOLVER)

# define the number of readouts and choose answer_mode to be "histogram" which already sorts the results by the number of occurrences
params = {"answer_mode": 'histogram', "num_reads": 10000}
results = solve_ising(solver, h, J, **params)
print results

'''
following result

{
  'timing': {
    'total_real_time': 1655206,
    'anneal_time_per_run': 20,
    'post_processing_overhead_time': 13588,
    'qpu_sampling_time': 1640000,
    'readout_time_per_run': 123,
    'qpu_delay_time_per_sample': 21,
    'qpu_anneal_time_per_sample': 20,
    'total_post_processing_time': 97081,
    'qpu_programming_time': 8748,
    'run_time_chip': 1640000,
    'qpu_access_time': 1655206,
    'qpu_readout_time_per_sample': 123
  },
  'energies': [-5.0],
  'num_occurrences': [10000],
  'solutions': [
      [1, 3, 3, 1, -1, 3, 3, -1, {
          lots of 3 's that I am omitting}]]}
'''

# Heuristic embedding
# suppose we can't manually embed our 2D checkerboard example. J and h then remain unchanged from our initial definitions:
J = {(0,1): 1, (0,2): 1, (1,3): 1, (2,3): 1}
h = [-1,0,0,0]

connection = RemoteConnection(DWAVE_SAPI_URL, DWAVE_TOKEN)
solver = connection.get_solver(DWAVE_SOLVER)

# first get the adjacency matrix of the current hardware graph:

adjacency = get_hardware_adjacency(solver)

# Now let's try to find an embedding of our problem:

embedding = find_embedding(J.keys(), adjacency)

# We are now ready to embed our problem onto the graph:

[h, j0, jc, embeddings] = embed_problem(h, J, embedding, adjacency)

# j0 contains the original couplings that we defined and jc contains the couplings that enforce the integrity of the chains (they correlate the qubits within the chains). Thus, we need to combine them again into one big J dictionary:

J = j0.copy()
J.update(jc)

# Now, we're ready to solve the embedded problem:

params = {"answer_mode": 'histogram', "num_reads": 10000}
raw_results = solve_ising(solver, h, J, **params)

print 'Lowest energy found: {}'.format(raw_results['energies'])
print 'Number of occurences: {}'.format(raw_results['num_occurrences'])

unembedded_results = unembed_answer(raw_results['solutions'], embedding, broken_chains='vote')

print 'Solution string: {}'.format(unembedded_results)

'''
you should get the correct result in all readouts:

Lowest energy found: [-5.0]
Number of occurences: [10000]
Solution string: [[1, -1, -1, 1]]
'''


