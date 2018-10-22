#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dimod

# https://docs.ocean.dwavesys.com/en/latest/overview/cpu.html
''' ExactSolver() that calculates the energy of all possible samples for a given problem. This example solves a two-variable Ising model classically on your local machine '''
solver = dimod.ExactSolver()
response = solver.sample_ising({'a': -0.5, 'b': 1.0}, {('a', 'b'): -1})

print(response)
print('response.data_vectors-energy', response.data_vectors['energy'])

# https://docs.ocean.dwavesys.com/projects/dimod/
''' This example constructs a simple QUBO and converts it to Ising format. '''
bqm = dimod.BinaryQuadraticModel({0: -1, 1: -1}, {(0, 1): 2}, 0.0, dimod.BINARY)  # QUBO
bqm_ising = bqm.change_vartype(dimod.SPIN, inplace=False)  # Ising

print('bqm', bqm)
print('bqm_ising', bqm_ising)

''' This example uses one of dimod's test samplers, ExactSampler, a solver that calculates the energies of all possible samples. '''
h = {0: 0.0, 1: 0.0}
J = {(0, 1): -1.0}
bqm = dimod.BinaryQuadraticModel.from_ising(h, J)
response = dimod.ExactSolver().sample(bqm)

print(response)

for sample, energy in response.data(['sample', 'energy']):
	print(sample, energy)
