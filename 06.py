#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs.ocean.dwavesys.com/en/latest/overview/cpu.html

import neal
solver = neal.SimulatedAnnealingSampler()
response = solver.sample_ising({'a': -0.5, 'b': 1.0}, {('a', 'b'): -1}, num_reads=2)

print(response.data_vectors['energy'])
