from neuron import h
from matplotlib import pyplot
import numpy

def set_recording_vectors(cell):
	"""Set soma, dendrite, and time recording vectors on the cell.
	#
	:param cell: Cell to record from.
	:return: the soma, dendrite, and time vectors as a tuple.
	"""
	soma_v_vec = h.Vector()   # Membrane potential vector at soma
	t_vec = h.Vector()        # Time stamp vector
	soma_v_vec.record(cell.soma(0.5)._ref_v)
	t_vec.record(h._ref_t)
	#
	return soma_v_vec, t_vec
#
def simulate(tstop):
	"""Initialize and run a simulation.
	#
	:param tstop: Duration of the simulation.
	"""

	h.tstop = tstop
	h.run()
#
def show_output(soma_v_vec, t_vec, clear_fig=True):	
	"""Draw the output.
	#
	:param soma_v_vec: Membrane potential vector at the soma.
	:param dend_v_vec: Membrane potential vector at the dendrite.
	:param t_vec: Timestamp vector.
	:param clear_fig: Flag to clear the figure or draw on top of
	#        previous results.
	"""
	if clear_fig:
		pyplot.clf()
		pyplot.figure(1) # Default figsize is (8,6)
	soma_plot = pyplot.plot(t_vec, soma_v_vec, color='black',label='soma')
	pyplot.legend()
	pyplot.xlabel('time (ms)')
	pyplot.ylabel('mV')
	#pyplot.axis([0,1000,-100,100])
	pyplot.show()
#
def network_run(type,tstop=2000,N=8,delay=0,dur=1e9,amp=0,loc=0.5,g2s=0,s2g=0,g2g=0):
	net = None

	if type == 'RSC':
		net = RSC(N=N,delay=delay,dur=dur,amp=amp,loc=loc,g2s=g2s,s2g=s2g,g2g=g2g)
	#
	if type == 'SSC':
		net = SSC(N=N,delay=delay,dur=dur,amp=amp,loc=loc,g2s=g2s,s2g=s2g,g2g=g2g)
	#
	if type == 'STC':
		net = STC(N=N,delay=delay,dur=dur,amp=amp,loc=loc,g2s=g2s,s2g=s2g,g2g=g2g)
	#
	cells = [net.stn_cells[0]]+[net.gpe_cells[0]]+[net.stn_cells[1]]+[net.gpe_cells[1]]
	#
	t_vec = h.Vector()
	t_vec.record(h._ref_t)
	v_vec = []
	#
	for j in range(4):
		vec = h.Vector()
		vec.record(cells[j].soma(0.5)._ref_v)
		v_vec.append(vec)
	#
	simulate(tstop)
	#
	fig, ax = pyplot.subplots(4,1,sharex=True,sharey=True)
	#
	for j in range(4):
		plot = ax[j].plot(t_vec, v_vec[j], color='black',label=cells[j].ident)
		x = ax[j].set_ylabel(cells[j].ident)
	#
	axis = pyplot.axis([0,2000,-100,50])
	tics = pyplot.yticks([-100,-50,0,50])
	#
	big_ax = fig.add_subplot(111)
	big_ax.set_axis_bgcolor('none')
	big_ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
	x = big_ax.set_xlabel('time (ms)')
	#y = big_ax.set_ylabel('voltage (mV)')
	#
	pyplot.tight_layout()
	pyplot.show()
#

def traces_run(ntype,ctype,name,tstop=2000,N=8,delay=0,dur=1e9,amp=0,loc=0.5,g2s=0,s2g=0,g2g=0):
	#
	net = None
	traces = []
	if ntype == 'RSC':
		net = RSC(N=N,delay=delay,dur=dur,amp=amp,loc=loc,g2s=g2s,s2g=s2g,g2g=g2g)
	#
	if ntype == 'SSC':
		net = SSC(N=N,delay=delay,dur=dur,amp=amp,loc=loc,g2s=g2s,s2g=s2g,g2g=g2g)
	#
	if ntype == 'STC':
		net = STC(N=N,delay=delay,dur=dur,amp=amp,loc=loc,g2s=g2s,s2g=s2g,g2g=g2g)
	#
	if ctype=='stn':
		cells = net.stn_cells[:]
	#
	elif ctype=='gpe':
		cells = net.gpe_cells[:]
	#
	else:
		raise TypeError("Invalid cell type")
	#
	t_vec = h.Vector()
	t_vec.record(h._ref_t)
	v_vec = []
	#
	for j in range(len(cells)):
		vec = h.Vector()
		vec.record(cells[j].soma(0.5)._ref_v)
		v_vec.append(vec)
	#
	simulate(tstop)
	spike_plot(v_vec,t_vec,name)
#

def spike_plot(v_vec,t_vec,name,vmin=-80,vmax=20,xtic=2,ytic=100):
	'''
	Takes an array of membrane potentials and outputs a spike plot figure.
	'''
	# Initialize image parameters
	vrange = vmax-vmin
	#
	timeS = [x for x in numpy.arange(0,int(t_vec[-1]+1),h.dt)]
	timeD = numpy.arange(0,int(t_vec[-1]+1),1)
	#
	timeID = [timeS.index(t) for t in timeD[:-1]]
	#
	ht = len(v_vec)
	w = len(timeID)
	step = int(len(t_vec)/w)
	ytic = int(max(times)*xtic/(2*ht))
	traces = [[numpy.mean([v_vec[i][x] for x in range(j,j+step,1)]) for j in timeID] for i in range(ht)]
	scaleData = []
	preimage = []
	#
	# Scale data
	for i in range(ht):
		scaleData.append([])
		for j in range(w):
			if traces[i][j]>vmax:
				scaleData[i].append(0)
			elif traces[i][j]<vmin:
				scaleData[i].append(1)
			else:
				scaleData[i].append(-(traces[i][j]-vmax)/vrange)
			#
		#
	# Create image	
	for i in range(ht*ytic):
		preimage.append([])
		for j in range(w*xtic):
			preimage[i].append(scaleData[i/ytic][j/xtic])
		#
	#
	image = numpy.array(preimage)
	fig = pyplot.figure()	
	pyplot.imshow(image,cmap=pyplot.cm.gray)
	pyplot.imsave(name,image,cmap=pyplot.cm.gray)
	fig.show()
#
