#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs.ocean.dwavesys.com/en/latest/examples/and.html
# http://www.ee.surrey.ac.uk/Projects/CAL/digital-logic/gatesfunc/

r''' Representing the Problem With a Penalty Function
	x1x2−2(x1+x2)z+3z

	QUBO formulation:

	E(qi,qi,j;xi)=3x3+x1x2−2x1x3−2x2x3

	where z=x3 is the AND gate’s output, x1,x2 the inputs, linear coefficients are q1=3, and quadratic coefficients are q1,2=1,q1,3=−2,q2,3=−2

	Often it is convenient to format the coefficients as an upper-triangular matrix:
				x1		 x2	 z
			|	0		 1		-2	|	x1
	Q =	|	0		 0		-2	|	x2
			|	0		 0		 3	|	z
'''

def run(sampler_embedded):
	response = sampler_embedded.sample_qubo(Q, num_reads=50)
	for sample, energy, num_occurrences in response.data(['sample', 'energy', 'num_occurrences'], sorted_by='num_occurrences'):
		print(sample, "Energy: ", energy, "Occurrences: ", num_occurrences)
	print('################################################################################')


from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = DWaveSampler()
Q = {('x1', 'x2'): 1, ('x1', 'z'): -2, ('x2', 'z'): -2, ('z', 'z'): 3} # Matrix Q - Row * Column

sampler_embedded = EmbeddingComposite(sampler)
print(sampler.adjacency[sampler.nodelist[0]])
run(sampler_embedded)

from dwave.system.composites import VirtualGraphComposite
embedding = {'x1': {1}, 'x2': {5}, 'z': {0, 4}}
sampler_embedded = VirtualGraphComposite(sampler, embedding)
print(sampler_embedded.adjacency)
run(sampler_embedded)

print(sampler.properties['extended_j_range']) # prints the range of values available for the D-Wave system
sampler_embedded = VirtualGraphComposite(sampler, embedding, chain_strength=0.1) # weakens the chain strength (strength of the coupler between qubits 0 and 4, which represents variable z)
# By setting it to a low value of 0.1, the two qubits are not strongly correlated and the result is that many returned samples represent invalid states for an AND gate.
run(sampler_embedded)


'''
{128, 4, 5, 6, 7}
{'z': 1, 'x1': 1, 'x2': 0} Energy:  1.0 Occurrences:  1
{'z': 1, 'x1': 0, 'x2': 0} Energy:  3.0 Occurrences:  1
{'z': 1, 'x1': 1, 'x2': 1} Energy:  0.0 Occurrences:  1025
{'z': 0, 'x1': 1, 'x2': 0} Energy:  0.0 Occurrences:  1032
{'z': 0, 'x1': 0, 'x2': 0} Energy:  0.0 Occurrences:  1398
{'z': 0, 'x1': 0, 'x2': 1} Energy:  0.0 Occurrences:  1543
################################################################################
{'x1': {'x2', 'z'}, 'x2': {'z', 'x1'}, 'z': {'x2', 'x1'}}
{'z': 0, 'x1': 1, 'x2': 1} Energy:  1.0 Occurrences:  1
{'z': 1, 'x1': 1, 'x2': 1} Energy:  0.0 Occurrences:  1154
{'z': 0, 'x1': 0, 'x2': 1} Energy:  0.0 Occurrences:  1251
{'z': 0, 'x1': 0, 'x2': 0} Energy:  0.0 Occurrences:  1264
{'z': 0, 'x1': 1, 'x2': 0} Energy:  0.0 Occurrences:  1330
################################################################################
[-2.0, 1.0]
{'z': 1, 'x1': 0, 'x2': 1} Energy:  1.0 Occurrences:  1
{'z': 1, 'x1': 0, 'x2': 1} Energy:  1.0 Occurrences:  1
{'z': 1, 'x1': 0, 'x2': 0} Energy:  3.0 Occurrences:  1
{'z': 1, 'x1': 1, 'x2': 1} Energy:  0.0 Occurrences:  808
{'z': 0, 'x1': 0, 'x2': 1} Energy:  0.0 Occurrences:  1052
{'z': 0, 'x1': 1, 'x2': 0} Energy:  0.0 Occurrences:  1566
{'z': 0, 'x1': 0, 'x2': 0} Energy:  0.0 Occurrences:  1571
'''
