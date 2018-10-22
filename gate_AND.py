#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' ******************** This code takes more than 20 seconds to finish. ******************** '''

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

Q_and = {('x1', 'x2'): 1, ('x1', 'z'): -2, ('x2', 'z'): -2, ('z', 'z'): 3} # gate AND # Matrix Q - Row * Column
Q_not = {('x', 'x'): -1, ('x', 'z'): 2, ('z', 'x'): 0, ('z', 'z'): -1} # gate NOT
num_reads = 50


def run(sampler_embedded, Q, chain_strength=1.0):
	response = sampler_embedded.sample_qubo(Q, num_reads=num_reads, chain_strength=chain_strength)
	for sample, energy, num_occurrences in response.data(['sample', 'energy', 'num_occurrences'], sorted_by='num_occurrences'):
		print(sample, "Energy: ", energy, "Occurrences: ", num_occurrences)
	print('################################################################################')


from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = DWaveSampler()

sampler_embedded = EmbeddingComposite(sampler)

print('Q_and - EmbeddingComposite', sampler.adjacency[sampler.nodelist[0]])
run(sampler_embedded, Q_and)

################################################################################

from dwave.system.composites import FixedEmbeddingComposite
embedding = {'x': [0], 'z': [4]}
sampler_embedded = FixedEmbeddingComposite(sampler, embedding) # manually minor-embed the NOT problem

print('Q_not - FixedEmbeddingComposite manually', sampler_embedded.adjacency)
run(sampler_embedded, Q_not)

################################################################################

embedding = {'x1': {1}, 'x2': {5}, 'z': {0, 4}}
sampler_embedded = FixedEmbeddingComposite(sampler, embedding) # manual minor-embedding the AND problem

print('Q_and - FixedEmbeddingComposite manually', sampler_embedded.adjacency)
run(sampler_embedded, Q_and)

################################################################################

print('Q_and - chain_strength', sampler.properties['extended_j_range']) # prints the range of values available for the D-Wave system
run(sampler_embedded, Q_and, chain_strength=0.25)

################################################################################

''' BUG - VirtualGraphComposite consumes several seconds, use instead FixedEmbeddingComposite
from dwave.system.composites import VirtualGraphComposite
embedding = {'x1': {1}, 'x2': {5}, 'z': {0, 4}}
sampler_embedded = VirtualGraphComposite(sampler, embedding)

print('Q_and - VirtualGraphComposite', sampler_embedded.adjacency)
run(sampler_embedded, Q_and)

################################################################################

print(sampler.properties['extended_j_range']) # prints the range of values available for the D-Wave system
sampler_embedded = VirtualGraphComposite(sampler, embedding, chain_strength=0.1) # weakens the chain strength (strength of the coupler between qubits 0 and 4, which represents variable z)
# By setting it to a low value of 0.1, the two qubits are not strongly correlated and the result is that many returned samples represent invalid states for an AND gate.
run(sampler_embedded, Q_and)
'''

################################################################################


'''
num_reads=5000 = 3.310 seconds | "Problem IDs" = 4

Q_and - EmbeddingComposite {128, 4, 5, 6, 7}
{'z': 1, 'x1': 1, 'x2': 1} Energy:  0.0 Occurrences:  1
{'z': 0, 'x1': 1, 'x2': 0} Energy:  0.0 Occurrences:  2
{'z': 0, 'x1': 1, 'x2': 0} Energy:  0.0 Occurrences:  730
{'z': 1, 'x1': 1, 'x2': 1} Energy:  0.0 Occurrences:  1352
{'z': 0, 'x1': 0, 'x2': 0} Energy:  0.0 Occurrences:  1360
{'z': 0, 'x1': 0, 'x2': 1} Energy:  0.0 Occurrences:  1555
################################################################################
Q_not - FixedEmbeddingComposite manually {'x': {'z'}, 'z': {'x'}}
{'x': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x': 1, 'z': 0} Energy:  -1.0 Occurrences:  2494
{'x': 0, 'z': 1} Energy:  -1.0 Occurrences:  2505
################################################################################
Q_and - FixedEmbeddingComposite manually {'x1': {'x2', 'z'}, 'x2': {'x1', 'z'}, 'z': {'x1', 'x2'}}
{'z': 1, 'x1': 0, 'x2': 1} Energy:  1.0 Occurrences:  1
{'z': 1, 'x1': 1, 'x2': 0} Energy:  1.0 Occurrences:  1
{'z': 0, 'x1': 1, 'x2': 1} Energy:  1.0 Occurrences:  1
{'z': 1, 'x1': 1, 'x2': 1} Energy:  0.0 Occurrences:  922
{'z': 0, 'x1': 0, 'x2': 1} Energy:  0.0 Occurrences:  1137
{'z': 0, 'x1': 0, 'x2': 0} Energy:  0.0 Occurrences:  1383
{'z': 0, 'x1': 1, 'x2': 0} Energy:  0.0 Occurrences:  1555
################################################################################
Q_and - chain_strength [-2.0, 1.0]
{'z': 0, 'x1': 1, 'x2': 0} Energy:  0.0 Occurrences:  587
{'z': 1, 'x1': 1, 'x2': 1} Energy:  0.0 Occurrences:  726
{'z': 1, 'x1': 1, 'x2': 0} Energy:  1.0 Occurrences:  766
{'z': 1, 'x1': 0, 'x2': 1} Energy:  1.0 Occurrences:  883
{'z': 0, 'x1': 0, 'x2': 0} Energy:  0.0 Occurrences:  1014
{'z': 0, 'x1': 0, 'x2': 1} Energy:  0.0 Occurrences:  1024
################################################################################

$ pip list | grep dwave
dwave-cloud-client           0.4.15
dwave-drivers                0.4.1
dwave-neal                   0.4.2
dwave-networkx               0.6.6
dwave-ocean-sdk              1.0.1
dwave-qbsolv                 0.2.9
dwave-system                 0.5.4
dwavebinarycsp               0.0.6

$ python --version
Python 3.7.0
'''
