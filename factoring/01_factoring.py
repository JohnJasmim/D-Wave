#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://cloud.dwavesys.com/learning/hub/home
# Notebook: Factoring

import itertools # imported but unused

import dwavebinarycsp as dbc
# Add an AND gate as a constraint to CSP and_csp defined for binary variables
and_gate = dbc.factories.and_gate(["x1", "x2", "x3"])
and_csp = dbc.ConstraintSatisfactionProblem('BINARY')
and_csp.add_constraint(and_gate)

# Convert the CSP into BQM and_bqm
and_bqm = dbc.stitch(and_csp)
and_bqm.remove_offset()

P = 21 # Set an integer to factor
bP = "{:06b}".format(P) # A binary representation of P ("{:06b}" formats for 6-bit binary)
csp = dbc.factories.multiplication_circuit(3)
bqm = dbc.stitch(csp, min_classical_gap=.1) # Convert the CSP into BQM bqm

p_vars = ['p0', 'p1', 'p2', 'p3', 'p4', 'p5'] # Our multiplication_circuit() creates these variables
# Convert P from decimal to binary
fixed_variables = dict(zip(reversed(p_vars), "{:06b}".format(P))) # {'p5': '0', 'p4': '1', 'p3': '0', 'p2': '1', 'p1': '0', 'p0': '1'}
fixed_variables = {var: int(x) for(var, x) in fixed_variables.items()}

# Fix product variables
for var, value in fixed_variables.items():
	bqm.fix_variable(var, value)

from dwave.system.samplers import DWaveSampler
sampler = DWaveSampler() # Use a D-Wave system as the sampler
_, target_edgelist, target_adjacency = sampler.structure

import dimod
from helpers.embedding import embeddings

# Set a pre-calculated minor-embeding
embedding = embeddings[sampler.solver.id]
bqm_embedded = dimod.embed_bqm(bqm, embedding, target_adjacency, 3.0)

# Return num_reads solutions (responses are in the D-Wave's graph of indexed qubits)
kwargs = {}
if 'num_reads' in sampler.parameters:
	kwargs['num_reads'] = 50
if 'answer_mode' in sampler.parameters:
	kwargs['answer_mode'] = 'histogram'
response = sampler.sample(bqm_embedded, **kwargs)
print("A solution indexed by qubits: \n", next(response.data(fields=['sample'])))

# Map back to the BQM's graph (nodes labeled "a0", "b0" etc,)
response = dimod.unembed_response(response, embedding, source_bqm=bqm)
print("\nThe solution in problem variables: \n", next(response.data(fields=['sample'])))

from helpers.convert import to_base_ten

# print(response.samples) # see below
''' FIXME: ERROR:
File "/usr/lib/python3.7/site-packages/dimod/sampleset.py", line 517, in samples
	for sample in itertools.islice(self.samples(n=None, sorted_by=sorted_by), n):

NameError: name 'itertools' is not defined
'''
sample = next(response.samples(n=1)) # Select just just the first sample. # FIXME: BUG: 'next()'

dict(sample)
a, b = to_base_ten(sample)

# TODO: Expected: Given integer P=21, found factors a=7 and b=3
print("Given integer P={}, found factors a={} and b={}".format(P, a, b))

''' OUTPUT
A solution indexed by qubits:
	Sample(sample={1481: 1, 1482: 1, 1483: 0, 1484: 0, 1485: 1, 1487: 1, 1488: 0, 1489: 1, 1490: 1, 1491: 0, 1492: 0, 1493: 0, 1494: 0, 1495: 1, 1501: 0, 1506: 0, 1509: 0, 1608: 0, 1609: 1, 1610: 1, 1611: 0, 1612: 1, 1614: 0, 1615: 0, 1616: 0, 1617: 1, 1618: 1, 1619: 0, 1620: 1, 1621: 1, 1622: 0, 1623: 0, 1624: 1, 1625: 1, 1626: 1, 1627: 1, 1628: 1, 1629: 1, 1630: 1, 1631: 1, 1632: 1, 1634: 0, 1637: 0, 1638: 1, 1736: 0, 1737: 1, 1738: 1, 1739: 1, 1740: 1, 1741: 1, 1742: 1, 1743: 1, 1744: 0, 1745: 1, 1747: 0, 1748: 1, 1750: 1, 1751: 1, 1752: 1, 1753: 1, 1754: 1, 1755: 1, 1756: 1, 1757: 1, 1758: 1, 1759: 1, 1760: 1, 1864: 1, 1871: 1, 1879: 1, 1887: 1, 1888: 1, 1895: 1})

The solution in problem variables:
	Sample(sample={'a0': 1, 'b0': 1, 'and0,1': 1, 'b1': 1, 'and0,2': 0, 'b2': 0, 'a1': 1, 'and1,0': 1, 'carry1,0': 1, 'and1,1': 1, 'carry1,1': 0, 'sum1,1': 1, 'and1,2': 0, 'a2': 1, 'and2,0': 1, 'carry2,0': 1, 'and2,1': 1, 'carry2,1': 0, 'sum2,1': 1, 'and2,2': 0, 'carry3,0': 1})
'''

''' print(response.samples)
<bound method SampleSet.samples of Response(rec.array([([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0], 0., 10),
	([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], 1.,  1),
	([1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 1.,  1),
	([1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], 2.,  1),
	([1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0], 2.,  1),
	([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1], 2.,  1),
	([1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0], 4.,  3),
	([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0], 4.,  2),
	([1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1], 4.,  1),
	([1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1], 2.,  1),
	([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0], 4.,  1),
	([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0], 7.,  2),
	([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0], 8.,  1),
	([1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1], 3.,  1),
	([1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], 3.,  1),
	([1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1], 3.,  1),
	([1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0], 3.,  1),
	([1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], 3.,  1),
	([1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1], 3.,  1),
	([1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1], 3.,  1),
	([1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1], 3.,  1),
	([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0], 3.,  1),
	([1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0], 3.,  1),
	([1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], 4.,  1),
	([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0], 9.,  2),
	([1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1], 6.,  1),
	([1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1], 4.,  1),
	([1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1], 4.,  1),
	([1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], 4.,  1),
	([1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], 5.,  1),
	([1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0], 7.,  1),
	([1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0], 5.,  1),
	([1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1], 6.,  1),
	([1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], 7.,  1),
	([1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0], 6.,  1),
	([1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1], 9.,  1)],
		dtype=[('sample', 'i1', (21,)), ('energy', '<f8'), ('num_occurrences', '<i8')]), ['a0', 'b0', 'and0,1', 'b1', 'and0,2', 'b2', 'a1', 'and1,0', 'carry1,0', 'and1,1', 'carry1,1', 'sum1,1', 'and1,2', 'a2', 'and2,0', 'carry2,0', 'and2,1', 'carry2,1', 'sum2,1', 'and2,2', 'carry3,0'], {'timing': {'total_real_time': 15962, 'qpu_access_overhead_time': 1939, 'anneal_time_per_run': 20, 'post_processing_overhead_time': 408, 'qpu_sampling_time': 8198, 'readout_time_per_run': 123, 'qpu_delay_time_per_sample': 21, 'qpu_anneal_time_per_sample': 20, 'total_post_processing_time': 408, 'qpu_programming_time': 7764, 'run_time_chip': 8198, 'qpu_access_time': 15962, 'qpu_readout_time_per_sample': 123}}, 'BINARY')>
'''

''' print(response.samples(n=1))
<generator object SampleSet.samples at 0x7f222021a570>
'''

'''
OS: Archlinux Kernel: x86_64 Linux 4.14.72-1-lts
Python version: 3.7.0
dwave-cloud-client           0.4.15
dwave-drivers                0.4.1
dwave-neal                   0.4.2
dwave-networkx               0.6.6
dwave-ocean-sdk              1.0.1
dwave-qbsolv                 0.2.9
dwave-system                 0.5.4
dwavebinarycsp               0.0.6
'''
