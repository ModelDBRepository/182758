#!/usr/bin/python
#Figure 3d

from neuron import h,gui

execfile('Cell.py')
execfile('STN.py')
execfile('GPe.py')
execfile('simrun.py')
execfile('network.py')

tstop = 2000

# Control
amp=-.25
g2s=2.5
s2g=0.03
g2g=0.2
traces_run('RSC','gpe','practice.png',tstop=tstop,amp=amp,g2s=g2s,s2g=s2g,g2g=g2g)

# Sparse-Irregular
amp=-0.25
g2s=2.5
s2g=0.03
g2g=0.2
network_run('RSC',tstop=tstop,amp=amp,g2s=g2s,s2g=s2g,g2g=g2g)

# Episodic
amp=-1.2
g2s=2.5
s2g=0.016
g2g=0
network_run('RSC',tstop=tstop,amp=amp,g2s=g2s,s2g=s2g,g2g=g2g)

# Continuous
amp=-1.2
g2s=2.5
s2g=0.1
g2g=0.02
network_run('RSC',tstop=tstop,amp=amp,g2s=g2s,s2g=s2g,g2g=g2g)
