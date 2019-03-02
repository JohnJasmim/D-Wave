#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://support.dwavesys.com/hc/en-us/articles/360003718693-Define-a-Simple-Problem-and-Submit-it-to-the-QPU-Ising-Example-
# https://support.dwavesys.com/hc/en-us/articles/360003718733-View-Results-Problem-Solution-

from dwave.system.samplers import DWaveSampler
solver = DWaveSampler() # Access the solver

qubits = solver.properties['qubits'] # enumerate the qubits
couplers = solver.properties['couplers'] # enumerate the qubits couplers

# print('qubits', qubits)
# print('couplers', couplers)

qubit_1 = 0
qubit_2 = 4
coupler = [qubit_1, qubit_2] # Two qubits that we can use (that are coupled) are 0 and 4.

if (qubit_1 in qubits) and (qubit_2 in qubits) and (coupler in couplers): # let's ensure both are available in our system
	print('Qubits {} and {} and their coupler {} are available'.format(qubit_1, qubit_2, coupler))

# Define a problem: Force the qubits to be spin-up by setting h_0 = h_4 = -1 and have a FM coupling between them. We expect to get samples with spin up (1) qubits and an energy of -1 + -1 + -1 = -3.

# H = h_1 * s_1 + h_2 * s_2 + J_{1,2} * s_1 * s_2
# h1 and h2 are biases on individual qubits and J_{1,2} is the coupling term

h = {qubit_1: -1, qubit_2: -1} # force the qubits to be spin-up
J = {tuple(coupler): -1} # we expect to get samples with spin up (1) qubits and an energy of -1 + -1 + -1 = -3

solution = solver.sample_ising(h, J, num_reads=10) # ask for a solution with 10 samples (reads):

print('Solution:', solution)

print('\nsamples in dict format\n' + str(list(solution.samples())))

# print('\nsamples in matrix format\n' + str(list(solution.samples_matrix))) # AttributeError: 'SampleSet' object has no attribute 'samples_matrix'

print('\nenergies of samples\n' + str(list(solution.data_vectors)))

print('\ntiming information\n' + str(list(solution.info)))

# Response = rec.array([([1, 1], -3., 10)]
