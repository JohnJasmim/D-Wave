#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs.ocean.dwavesys.com/en/latest/overview/solving_problems.html

import dwavebinarycsp
import dwavebinarycsp.factories.constraint.gates as gates
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
csp.add_constraint(gates.and_gate(['x1', 'x2', 'y1']))  # add an AND gate
bqm = dwavebinarycsp.stitch(csp)

''' The members of the two dicts are linear and quadratic coefficients, respectively, the third term is a constant offset associated with the model, and the fourth shows the variable types in this model are binary. '''
print(bqm) # BQM of the AND gate created

print('################################################################################')

from dimod.reference.samplers import ExactSolver
sampler = ExactSolver()
response = sampler.sample(bqm)

print(response)

for datum in response.data():
	print(datum)

for sample, energy in response.data(fields=['sample', 'energy'], sorted_by='energy'):
	print(sample, energy)

print('################################################################################')

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = EmbeddingComposite(DWaveSampler()) # EmbeddingComposite() composite that maps unstructured problems to the graph structure of the selected sampler, a process known as minor-embedding.
response = sampler.sample(bqm, num_reads=1000) # Because of the sampler's probabilistic nature, you typically request multiple samples for a problem; this example sets num_reads to 1000.

print(response)

for sample, energy, num_occurrences in response.data(fields=['sample', 'energy', 'num_occurrences'], sorted_by='num_occurrences'):
	print(sample, energy, "Occurrences: ", num_occurrences)

print('################################################################################')

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import VirtualGraphComposite # simplify minor-embedding
print(DWaveSampler().properties['extended_j_range'])

# maps a problem's variables x, y to qubits 1, 5 and variable z to two qubits 0 and 4
embedding = {'x': {1}, 'y': {5}, 'z': {0, 4}}
# checks some features supported on the D-Wave system used as a sampler
sampler = VirtualGraphComposite(DWaveSampler(), embedding)
print(sampler.parameters)
