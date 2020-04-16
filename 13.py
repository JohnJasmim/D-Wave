#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Manual Minor-Embedding

from dwave.system.samplers import DWaveSampler
# Set Q for the minor-embedded problem QUBO
qubit_biases = {(0, 0): 0.3333, (1, 1): -0.333, (4, 4): -0.333, (5, 5): 0.333}
coupler_strengths = {(0, 4): 0.667, (0, 5): -1, (1, 4): 0.667, (1, 5): 0.667}
Q = dict(qubit_biases)
Q.update(coupler_strengths)
print(DWaveSampler().nodelist[0:8])
# Sample once on a D-Wave system and print the returned sample
response = DWaveSampler().sample_qubo(Q, num_reads=1)
print(next(response.samples()))

response = DWaveSampler().sample_qubo(Q, num_reads=100)
for rd in response.data():
	print(rd.sample, "Energy: ", rd.energy, "Occurrences: ", rd.num_occurrences)

import pdb; pdb.set_trace() # debug


# Automatic

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

# Set Q for the problem QUBO
# linear = {(0, 0): -1, (1, 1): -1, (2, 2): -1}
# quadratic = {(0, 1): 2, (0, 2): 2, (1, 2): 2}
linear = {('x0', 'x0'): -1, ('x1', 'x1'): -1, ('x2', 'x2'): -1}
quadratic = {('x0', 'x1'): 2, ('x0', 'x2'): 2, ('x1', 'x2'): 2}
Q = dict(linear)
Q.update(quadratic)

# Minor-embed and sample 1000 times on a default D-Wave system
response = EmbeddingComposite(DWaveSampler()).sample_qubo(Q, num_reads=100)

for rd in response.data():
	print(rd.sample, "Energy: ", rd.energy, "Occurrences: ", rd.num_occurrences)

import pdb; pdb.set_trace() # debug
