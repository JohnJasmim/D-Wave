#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs.ocean.dwavesys.com/en/latest/examples/not.html
# http://www.ee.surrey.ac.uk/Projects/CAL/digital-logic/gatesfunc/

r''' Representing the Problem With a Penalty Function
	2xz -x -z +1
	state x,z=0,1 -> 2xz -x -z +1 = 2*0*1 -0 -1 +1 = -1+1 = 0
	state x,z=0,0 -> 2xz -x -z +1 = 2*0*0 -0 -0 +1 = 1

	QUBO formulation:
	-x1 -x2 +2x1x2
	where z=x2 is the NOT gate's output, x=x1 the input, linear coefficients are q1=q2=-1, and quadratic coefficient is q1,2=2
		Often it is convenient to format the coefficients as an upper-triangular matrix:
				 x		z
	Q =	| -1   2 |	x
			|  0  -1 |	z
'''

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = DWaveSampler()
sampler_embedded = EmbeddingComposite(sampler)

Q = {('x', 'x'): -1, ('x', 'z'): 2, ('z', 'x'): 0, ('z', 'z'): -1} # Matrix Q - Row * Column

print(sampler.adjacency[sampler.nodelist[0]])
response = sampler_embedded.sample_qubo(Q, num_reads=50)
for sample, energy, num_occurrences in response.data(['sample', 'energy', 'num_occurrences'], sorted_by='num_occurrences'):
	print(sample, "Energy: ", energy, "Occurrences: ", num_occurrences)

print('################################################################################')

from dwave.system.composites import FixedEmbeddingComposite
sampler_embedded = FixedEmbeddingComposite(sampler, {'x': [0], 'z': [4]}) # manually minor-embed the problem

print(sampler_embedded.adjacency)
response = sampler_embedded.sample_qubo(Q, num_reads=50)
for sample, energy, num_occurrences in response.data(['sample', 'energy', 'num_occurrences'], sorted_by='num_occurrences'):
	print(sample, "Energy: ", energy, "Occurrences: ", num_occurrences)


'''
{128, 4, 5, 6, 7}
{'x': 0, 'z': 0} Energy:  0.0 Occurrences:  2
{'x': 0, 'z': 1} Energy:  -1.0 Occurrences:  2355
{'x': 1, 'z': 0} Energy:  -1.0 Occurrences:  2643
################################################################################
{'x': {'z'}, 'z': {'x'}}
{'x': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x': 1, 'z': 0} Energy:  -1.0 Occurrences:  1753
{'x': 0, 'z': 1} Energy:  -1.0 Occurrences:  3245
'''
