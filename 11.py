#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs.ocean.dwavesys.com/projects/system/en/latest/reference/generated/dwave.embedding.unembed_sampleset.html

import dimod
from dwave.embedding import unembed_sampleset

# Triangular binary quadratic model and an embedding
J = {('a', 'b'): -1, ('b', 'c'): -1, ('a', 'c'): -1}
bqm = dimod.BinaryQuadraticModel.from_ising({}, J)
embedding = {'a': [0, 1], 'b': [2], 'c': [3]}
# Samples from the embedded binary quadratic model
samples = [{0: -1, 1: -1, 2: -1, 3: -1},  # [0, 1] is unbroken
					 {0: -1, 1: +1, 2: +1, 3: +1}]  # [0, 1] is broken
energies = [-3, 1]
embedded = dimod.SampleSet.from_samples(samples, dimod.SPIN, energies)
# Unembed
samples = unembed_sampleset(embedded, embedding, bqm)

print(samples.record.sample) # doctest: +SKIP

