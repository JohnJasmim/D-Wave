#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs.ocean.dwavesys.com/en/latest/examples/scheduling.html
import dwavebinarycsp

r''' D-Wave systems solve binary quadratic models, so the first step is to express the problem with binary variables.
	Time of day is represented by binary variable "time" with value
		1 	for business hours and
		0 	for hours outside the business day.
	Venue is represented by binary variable "location" with value
		1 	for office and
		0	for teleconference.
	Participation is represented by variable "mandatory" with value
		1 for mandatory participation and
		0 for optional participation.:
	Meeting duration is represented by variable "length" with value
		1 	for short meetings (under 30 minutes) and
		0 for meetings of longer duration.
'''


def scheduling(time, location, length, mandatory):
	if time:														# Business hours
		return (location and mandatory)			# In office and mandatory participation
	else:															# Outside business hours
		return ((not location) and length)	# Teleconference for a short duration


csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
csp.add_constraint(scheduling, ['time', 'location', 'length', 'mandatory']) # create a constraint from this function and adds it to CSP instance

bqm = dwavebinarycsp.stitch(csp) # convert the binary CSP to a BQM
print('bqm.linear', bqm.linear)
print('bqm.quadratic', bqm.quadratic)

print('################################################################################')

# Solving Classically on a CPU
from dimod.reference.samplers import ExactSolver
sampler = ExactSolver()
solution = sampler.sample(bqm) # returns the BQM's value (energy) for every possible assignment of variable values.

min_energy = next(solution.data(['energy']))[0]
print(min_energy) # assignments of variables that do not violate any constraint-should have the lowest value of the BQM

for sample, energy in solution.data(['sample', 'energy']):
	if energy == min_energy: # prints all those solutions (assignments of variables) for which the BQM has its minimum value.
		time = 'business hours' if sample['time'] else 'evenings'
		location = 'office' if sample['location'] else 'home'
		length = 'short' if sample['length'] else 'long'
		mandatory = 'mandatory' if sample['mandatory'] else 'optional'
		print("During {} at {}, you can schedule a {} meeting that is {}".format(time, location, length, mandatory))

print('################################################################################')

# Solving on a D-Wave System
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = EmbeddingComposite(DWaveSampler()) # endpoint='https://URL_to_my_D-Wave_system/', token='ABC-123456789012345678901234567890', solver='My_D-Wave_Solver'
response = sampler.sample(bqm, num_reads=50) # map our unstructured problem (variables such as time etc.) to the sampler's graph structure (the QPU's numerically indexed qubits) in a process known as minor-embedding.

total = 0
for sample, energy, occurrences in response.data(['sample', 'energy', 'num_occurrences'], sorted_by='num_occurrences'):
	total = total + occurrences
	if energy == min_energy: # prints all those solutions (assignments of variables) for which the BQM has its minimum value and the number of times it was found
		time = 'business hours' if sample['time'] else 'evenings'
		location = 'office' if sample['location'] else 'home'
		length = 'short' if sample['length'] else 'long'
		mandatory = 'mandatory' if sample['mandatory'] else 'optional'
		print("{}: During {} at {}, you can schedule a {} meeting that is {}".format(occurrences, time, location, length, mandatory))
print("Total occurrences: ", total)
