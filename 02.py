#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs.ocean.dwavesys.com/en/latest/overview/dwavesys.html#querying-available-solvers

from dwave.system.samplers import DWaveSampler
sampler = DWaveSampler()

print('\nsampler.parameters', sampler.parameters, sep='\n')

print('\nsampler.properties.keys()', sampler.properties.keys(), sep='\n')

print('\nresp1', sampler.sample_ising({0: 0.0}, {}, num_reads=1), sep='\n')

print('\nresp2', sampler.sample_ising({0: 2.0}, {}), sep='\n')
