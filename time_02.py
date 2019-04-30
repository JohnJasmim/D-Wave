#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs.dwavesys.com/docs/latest/c_timing_6.html

from dwave_sapi2.local import local_connection
from dwave_sapi2.core import async_solve_ising, await_completion
import datetime

h,J = build_hamiltonian()
solver = local_connection.get_solver('example_solver')
submitted_qmi = async_solve_ising(solver, h, J, num_reads=100)
await_completion([submitted_qmi], min_done=2, timeout=1.0)

# QPU and PP times
result = submitted_qmi.result()
timing = result['timing']

# Service time
time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
status = submitted_qmi.status()
start_time = datetime.datetime.strptime(status ['time_received'], time_format)
finish_time = datetime.datetime.strptime(status['time_solved'], time_format)
service_time = finish_time - start_time
