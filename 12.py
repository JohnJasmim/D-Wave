#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://support.dwavesys.com/hc/en-us/community/posts/360029524913-QUBO-embedding-and-Solver

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import FixedEmbeddingComposite
from minorminer import find_embedding

solver = DWaveSampler()

Q1 = [('x1', 'x2'), ('x1', 'z'), ('x2', 'z')]
Q2 = {('x1', 'x2'): 2, ('x1', 'z'): -2, ('x2', 'z'): 3}
Q3 = {('x1', 'x2'): 1, ('x1', 'z'): 5, ('x2', 'z'): 20}

__, target_edgelist, target_adjacency = solver.structure

emb1 = find_embedding(Q1, target_edgelist, verbose=1) # get the list of variables and nodes
emb2 = find_embedding(Q2, target_edgelist, verbose=1)
emb3 = find_embedding(Q3, target_edgelist, verbose=1)

sampler1 = FixedEmbeddingComposite(solver, emb1) # knows nothing about the origianl QUBO matrix
result1 = sampler1.sample_qubo(Q2, num_reads=10) # uses the original matrix on the phisical embedding

sampler2 = FixedEmbeddingComposite(solver, emb2)
result2 = sampler2.sample_qubo(Q2, num_reads=10)

sampler3 = FixedEmbeddingComposite(solver, emb3)
result3 = sampler3.sample_qubo(Q3, num_reads=10)

print('\nresult1', result1)
print('\nresult2', result2)
print('\nresult3', result3)

print('\nemb1', emb1)
print('\nemb2', emb2)
print('\nemb3', emb3)

# import pdb; pdb.set_trace() # debug
