#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs.ocean.dwavesys.com/projects/qbsolv/

from dwave_qbsolv import QBSolv
Q = {(0, 0): 1, (1, 1): 1, (0, 1): 1}
response = QBSolv().sample_qubo(Q)

print("samples=" + str(list(response.samples())))
print("energies=" + str(list(response.data_vectors['energy'])))
