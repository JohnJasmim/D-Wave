#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs.ocean.dwavesys.com/en/latest/examples/multi_gate.html
# https://docs.ocean.dwavesys.com/en/latest/examples/multi_gate_results.html

# two formulations of constraints from the problem's logic gates
import dwavebinarycsp


''' Single comprehensive constraint '''
def logic_circuit(a, b, c, d, z):
	r''' consolidates the circuit as a single constraint, yields a binary quadratic model with 7 variables: 4 inputs, 1, output, and 2 ancillary variables '''
	not1 = not b
	or2 = b or c
	and3 = a and not1
	or4 = or2 or d
	and5 = and3 and or4
	not6 = not or4
	or7 = and5 or not6
	return (z == or7)


csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
csp.add_constraint(logic_circuit, ['a', 'b', 'c', 'd', 'z'])

''' Multiple small constraints '''
import dwavebinarycsp.factories.constraint.gates as gates
import operator

''' creates a constraint satisfaction problem from multiple small constraints, yields a binary quadratic model with 11 variables: 4 inputs, 1 output, and 6 intermediate outputs of the logic gates '''
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
csp.add_constraint(operator.ne, ['b', 'not1']) # add NOT 1 gate
csp.add_constraint(gates.or_gate(['b', 'c', 'or2'])) # add OR 2 gate
csp.add_constraint(gates.and_gate(['a', 'not1', 'and3'])) # add AND 3 gate
csp.add_constraint(gates.or_gate(['d', 'or2', 'or4'])) # add OR 4 gate
csp.add_constraint(gates.and_gate(['and3', 'or4', 'and5'])) # add AND 5 gate
csp.add_constraint(operator.ne, ['or4', 'not6']) # add NOT 6 gate
csp.add_constraint(gates.or_gate(['and5', 'not6', 'z'])) # add OR 7 gate

bqm = dwavebinarycsp.stitch(csp) # Convert the binary constraint satisfaction problem to a binary quadratic model

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

sampler = EmbeddingComposite(DWaveSampler()) # Set up a D-Wave system as the sampler

response = sampler.sample(bqm, num_reads=1000)

# Check how many solutions meet the constraints (are valid)
valid, invalid, data = 0, 0, []
for datum in response.data():
	sample, energy, num = datum
	if (csp.check(sample)):
		valid = valid + num
		for i in range(num):
			data.append((sample, energy, '1'))
	else:
		invalid = invalid + num
		for i in range(num):
			data.append((sample, energy, '0'))
print(valid, invalid)

print(next(response.samples()))

import matplotlib.pyplot as plt
plt.ion()
plt.scatter(range(len(data)), [x[1] for x in data], c=['y' if (x[2] == '1') else 'r' for x in data], marker='.')
plt.xlabel('Sample')
plt.ylabel('Energy')

for datum in response.data():
	print(datum)

# Constraint.from_configurations(frozenset([(1, 0, 0), (0, 1, 0), (0, 0, 0), (1, 1, 1)]), ('a', 'not1', 'and3'), Vartype.BINARY, name='AND')
