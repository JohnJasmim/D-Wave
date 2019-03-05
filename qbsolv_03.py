#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://support.dwavesys.com/hc/en-us/community/posts/360022231294-How-to-use-D-wave-with-qbsolv-command-

from dwave_qbsolv import QBSolv
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import itertools
import random

# Make a small QUBO
Q1 = {(0, 0): 1, (1, 1): 1, (0, 1): 1}

# Make a large QUBO
qubo_size = 200
Q2 = {t: random.uniform(-1, 1) for t in itertools.product(range(qubo_size), repeat=2)}

# Set up a composite QPU sampler
sampler = EmbeddingComposite(DWaveSampler())

print('Solve the small QUBO')
response1 = QBSolv().sample_qubo(Q1, solver=sampler)
print('energies=' + str(list(response1.data_vectors['energy'])))

print(type(Q2), Q2)

print('Solve the large QUBO')
response2 = QBSolv().sample_qubo(Q2, solver=sampler)
print('energies=' + str(list(response2.data_vectors['energy'])))
