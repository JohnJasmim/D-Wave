#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://ocean.dwavesys.com/

import dwavebinarycsp
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

sampler = EmbeddingComposite(DWaveSampler())

csp = dwavebinarycsp.factories.random_2in4sat(10, 7)
bqm = dwavebinarycsp.stitch(csp)

solution = sampler.sample(bqm)

print(solution)
