#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://support.dwavesys.com/hc/en-us/community/posts/360029545074-Displaying-Embedding-Generated-by-EmbeddingComposite

from dimod import BinaryQuadraticModel
from dwave.embedding import embed_bqm, unembed_sampleset
from dwave.system.samplers import DWaveSampler
from minorminer import find_embedding
from dwave.embedding.chain_breaks import majority_vote
from dwave.embedding.chain_breaks import MinimizeEnergy

solver = DWaveSampler()

__, target_edgelist, target_adjacency = solver.structure

Q = {(0,1):1}

bqm = BinaryQuadraticModel.from_qubo(Q)

emb = find_embedding(Q, target_edgelist)

embedded_bqm = embed_bqm(bqm, emb, target_adjacency)

result = solver.sample(embedded_bqm, num_reads=1)

# unembedded = unembed_sampleset(result, emb, bqm, chain_break_method=majority_vote(bqm, emb))
unembedded = unembed_sampleset(result, emb, bqm, MinimizeEnergy(bqm, emb))

print(unembedded)
