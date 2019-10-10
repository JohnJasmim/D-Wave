#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://support.dwavesys.com/hc/en-us/community/posts/360029545074-Displaying-Embedding-Generated-by-EmbeddingComposite

# Initialize some settings for this test.
manual_embed = True
num_samples = 256
qubo = {(0, 0): 0, (1, 1): 0, (2, 2): 0.0, (3, 3): 0, (4, 4): 7.5, (5, 5): 7.5, (6, 6): 0.5, (7, 7): 11.75, (0, 1): 0, (0, 2): 5.5, (0, 3): 5.5, (0, 4): 0, (0, 5): -11.0, (0, 6): 0, (0, 7): -11.0, (1, 2): 5.5, (1, 3): 5.5, (1, 4): -11.0, (1, 5): 0, (1, 6): -11.0, (1, 7): 0, (2, 3): 0, (2, 4): -11.0, (2, 5): 0, (2, 6): 0, (2, 7): -11.0, (3, 4): 0, (3, 5): -11.0, (3, 6): -11.0, (3, 7): 0, (4, 5): 2.0, (4, 6): 4.0, (4, 7): 1.0, (5, 6): 4, (5, 7): 1.0, (6, 7): 2.0}

# qubo = {(0, 0): 0, (1, 1): 0, (2, 2): 0.0, (3, 3): 0, (4, 4): 7.5, (5, 5): 7.5, (6, 6): 0.5, (7, 7): 11.75, (0, 2): 5.5, (0, 3): 5.5, (0, 5): -11.0, (0, 7): -11.0, (1, 2): 5.5, (1, 3): 5.5, (1, 4): -11.0, (1, 6): -11.0, (2, 4): -11.0, (2, 7): -11.0, (3, 5): -11.0, (3, 6): -11.0, (4, 5): 2.0, (4, 6): 4.0, (4, 7): 1.0, (5, 6): 4, (5, 7): 1.0, (6, 7): 2.0}


# Construct a sampler over a real quantum annealer.
from dwave.system.samplers import DWaveSampler
sampler = DWaveSampler()


# Construct an automatic embedding over the machine architecture.
_, edgelist, adjacency = sampler.structure
from minorminer import find_embedding
embedding = find_embedding(qubo, edgelist, random_seed=0) # random_seed=0 - which ensures that the same embedding is always generated.


if manual_embed:
	# Pick the method for fixing broken chains.
	from dwave.embedding.chain_breaks import majority_vote # weighted_random
	method = majority_vote
	# Submit the job via an embedded BinaryQuadraticModel.
	from dimod import BinaryQuadraticModel as BQM
	from dwave.embedding import embed_bqm, unembed_sampleset
	# Generate a BQM from the QUBO.
	q = BQM.from_qubo(qubo)
	# Embed the BQM onto the target structure.
	embedded_q = embed_bqm(q, embedding, adjacency) # chain_strength=chain_strength, smear_vartype=dimod.SPIN
	# Collect the sample output.
	response = unembed_sampleset(
	   sampler.sample(embedded_q, num_reads=num_samples),
	   embedding, q, chain_break_method=method,
	   chain_break_fraction=True)
else:
	# Use a FixedEmbeddingComposite if we don't care about chains.
	from dwave.system.composites import FixedEmbeddingComposite
	system_composite = FixedEmbeddingComposite(sampler, embedding)
	response = system_composite.sample_qubo(qubo, num_reads=num_samples)


constant = 0

# Cycle through the results and yield them to the caller.
for out in response.data():
	# Get the output from the data.
	bits = (out.sample[b] for b in sorted(out.sample))
	occurrence = out.num_occurrences
	chain_break_fraction = out.chain_break_fraction
	energy = out.energy + constant
	print('Bits \t\t\t\t Occurrence \t Chain \t breaks \t Energy')
	print(bits, occurrence, 100 * chain_break_fraction, energy)
