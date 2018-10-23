import dwavebinarycsp as dbc
# Add an AND gate as a constraint to CSP and_csp defined for binary variables
and_gate = dbc.factories.and_gate(["x1", "x2", "x3"])
and_csp = dbc.ConstraintSatisfactionProblem('BINARY')
and_csp.add_constraint(and_gate)

# Test that for input x1,x2=1,1 the output is x3=1 (both switches on and light shining)
and_csp.check({"x1": 1, "x2": 1, "x3": 1})

# Use itertools to produce all possible 3-bit binary combinations for x1, x2, x3
import itertools
configurations = []
for (x1, x2, x3) in list(itertools.product([0, 1], repeat=3)):
	E = 3 * x3 + x1 * x2 - 2 * x1 * x3 - 2 * x2 * x3
	configurations.append((E, x1, x2, x3))
# Sort from lowest to highest value of the BQM
configurations.sort()
# Print BQM value under "E" and all configurations under "x1, x2, x3"
print("E, x1, x2, x3")
print(configurations)

# Convert the CSP into BQM and_bqm
and_bqm = dbc.stitch(and_csp)
and_bqm.remove_offset()
# Print the linear and quadratic coefficients. These are the programable inputs to a D-Wave system
print(and_bqm.linear) # {'x1': 0.0, 'x2': 0.0, 'x3': 6.0}
print(and_bqm.quadratic) # {('x2', 'x1'): 2.0, ('x3', 'x1'): -4.0, ('x3', 'x2'): -4.0}

# Use a dimod test sampler that gives the BQM value for all values of its variables
from dimod import ExactSolver
sampler = ExactSolver()

# Solve the BQM
solution = sampler.sample(and_bqm)
list(solution.data())

# Set an integer to factor
P = 21

# A binary representation of P ("{:06b}" formats for 6-bit binary)
bP = "{:06b}".format(P)
print(bP)

csp = dbc.factories.multiplication_circuit(3)
# Print one of the CSP's constraints, the gates that constitute 3-bit binary multiplication
print(next(iter(csp.constraints)))

# Convert the CSP into BQM bqm
bqm = dbc.stitch(csp, min_classical_gap=.1)
# Print a sample coefficient (one of the programable inputs to a D-Wave system)
print("p0: ", bqm.linear['p0'])

# To see helper functions, select Jupyter File Explorer View from the Online Learning page
from helpers import draw
draw.circuit_from(bqm)

# Our multiplication_circuit() creates these variables
p_vars = ['p0', 'p1', 'p2', 'p3', 'p4', 'p5']

# Convert P from decimal to binary
fixed_variables = dict(zip(reversed(p_vars), "{:06b}".format(P))) # {'p5': '0', 'p4': '1', 'p3': '0', 'p2': '1', 'p1': '0', 'p0': '1'}
fixed_variables = {var: int(x) for(var, x) in fixed_variables.items()}

# Fix product variables
for var, value in fixed_variables.items():
	bqm.fix_variable(var, value)

# Confirm that a P variable has been removed from the BQM, for example, "p0"
print("Variable p0 in BQM: ", 'p0' in bqm)
print("Variable a0 in BQM: ", 'a0' in bqm)

from dwave.system.samplers import DWaveSampler
# Use a D-Wave system as the sampler
sampler = DWaveSampler()
# sampler = DWaveSampler(solver=my_solver, token=my_token)
_, target_edgelist, target_adjacency = sampler.structure

import dimod
from helpers.embedding import embeddings

# Set a pre-calculated minor-embeding
embedding = embeddings[sampler.solver.id]
bqm_embedded = dimod.embed_bqm(bqm, embedding, target_adjacency, 3.0)

# Confirm mapping of variables from a0, b0, etc to indexed qubits
print("Variable a0 in embedded BQM: ", 'a0' in bqm_embedded) # False
print("First five nodes in QPU graph: ", sampler.structure.nodelist[:5]) # [0, 1, 2, 3, 4]

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
# Select just just the first sample.
sample = next(response.samples(n=1))
dict(sample)
a, b = to_base_ten(sample)

print("Given integer P={}, found factors a={} and b={}".format(P, a, b))
