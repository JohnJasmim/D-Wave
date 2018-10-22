#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import dwave_networkx as dnx
import dwave_micro_client_dimod as micro
import dwave_qbsolv

urlc = 'https://cloud.dwavesys.com/sapi'
tokenc = 'SE-bb7f104b4a99cf9a10eeb9637f0806761c9fcedc'
solver_namec = 'DW_2000Q_1'

structured_samplerc = micro.DWaveSampler(solver_namec, urlc, tokenc)
samplerc = micro.EmbeddingComposite(structured_samplerc)
samplerq = dwave_qbsolv.QBSolv()
cloudsi = dnx.structural_imbalance(G, samplerc , num_reads=10000)
qbsolvsi = dnx.structural_imbalance (G, samplerq , solver= samplerc)

h = {v: node_values [v] for v in G.nodes }
J = {(u, v): eval for u, v in G.edges }

response = samplerc.sample_ising (h, J, num_reads=10000)
