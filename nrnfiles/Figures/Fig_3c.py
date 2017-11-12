#!/usr/bin/python
#Figure 3c

from neuron import h,gui

execfile('Cell.py')
execfile('STN.py')
execfile('GPe.py')
execfile('simrun.py')
execfile('Network.py')

tstop = 2000

# Control
amp=-0.25
g2s=0
s2g=0
g2g=0
network_run('RSC',tstop=tstop,amp=amp,g2s=g2s,s2g=s2g,g2g=g2g)

# Sparse-Irregular
amp=5
g2s=200
s2g=0.2
g2g=0.02
network_run('RSC',tstop=tstop,amp=amp,g2s=g2s,s2g=s2g,g2g=g2g)

# Episodic
amp=-1.2
g2s=2.5
s2g=0.016
g2g=0
network_run('SSC',tstop=tstop,amp=amp,g2s=g2s,s2g=s2g,g2g=g2g)

# Continuous
amp=-1.2
g2s=0.5
s2g=2.5
g2g=0.02
network_run('RSC',tstop=tstop,amp=amp,g2s=g2s,s2g=s2g,g2g=g2g)
