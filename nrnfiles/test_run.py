#!/usr/bin/python
# Basic test

from neuron import h,gui

execfile('Cell.py')
execfile('STN.py')
execfile('GPe.py')
execfile('simrun.py')
execfile('spikes.py')

test1 = None
test1 = STN()


soma_v_vec, t_vec = set_recording_vectors(test1)

tstop = test1.dur = 2000
test1.dur = 500
test1.amp = 60
test1.delay = 0
stim = test1.attach_current_clamp()

simulate(tstop)

show_output(soma_v_vec, t_vec)
