#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs.ocean.dwavesys.com/en/latest/examples/min_vertex.html

import networkx as nx
s5 = nx.star_graph(4) # create a star graph where node 0 is hub to four other nodes.

# Solving Classically on a CPU

from dimod.reference.samplers import ExactSolver
sampler = ExactSolver() # returns the BQM's value for every possible assignment of variable values

import dwave_networkx as dnx
print(dnx.min_vertex_cover(s5, sampler)) # produce a BQM for our s5 graph and solve it on our selected sampler

print('################################################################################')

# Solving on a D-Wave System

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite # EmbeddingComposite(), maps unstructured problems to the graph structure of the selected sampler, a process known as minor-embedding
sampler = EmbeddingComposite(DWaveSampler()) # endpoint='https://URL_to_my_D-Wave_system/', token='ABC-123456789012345678901234567890', solver='My_D-Wave_Solver'
print(dnx.min_vertex_cover(s5, sampler))

print('################################################################################')

w5 = nx.wheel_graph(5) # creates a new graph
print(dnx.min_vertex_cover(w5, sampler)) # solves on a D-Wave system
print(dnx.min_vertex_cover(w5, sampler))

print('################################################################################')

c5 = nx.circular_ladder_graph(5) # replaces the problem graph
print(dnx.min_vertex_cover(c5, sampler)) # submits twice to the D-Wave system for solution
print(dnx.min_vertex_cover(c5, sampler)) # producing two of the possible valid solutions.
