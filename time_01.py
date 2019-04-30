#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs.dwavesys.com/docs/latest/c_timing_5.html
# https://docs.dwavesys.com/docs/latest/c_timing_2.html

import random
import datetime as dt
from dwave.cloud import Client

# Connect using the default or environment connection information
with Client.from_config() as client:

    # Load the default solver
    solver = client.get_solver()

    # Build a random Ising model to exactly fit the graph the solver supports
    linear = {index: random.choice([-1, 1]) for index in solver.nodes}
    quad = {key: random.choice([-1, 1]) for key in solver.undirected_edges}

    # Send the problem for sampling, include solver-specific parameter 'num_reads'
    computation = solver.sample_ising(linear, quad, num_reads=100)
    computation.wait()

    # Print the first sample out of a hundred
    print(computation.samples[0])
    timing = computation['timing']


    # Service time
    time_format = "%Y-%m-%d %H:%M:%S.%f"
    start_time = dt.datetime.strptime(str(computation.time_received)[:-6], time_format)
    finish_time = dt.datetime.strptime(str(computation.time_solved)[:-6], time_format)
    service_time = finish_time - start_time
    qpu_access_time = timing['qpu_access_time']
    print("start_time="+str(start_time)+", finish_time="+str(finish_time)+ \
            ", service_time="+str(service_time)+", qpu_access_time="       \
            +str(float(qpu_access_time)/1000000))
