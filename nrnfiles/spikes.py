import numpy

def detect_spikes(t_vec,v_vec,thresh=0,start=100):
	spikes = []
	for i in range(start,len(t_vec)):
		if v_vec[i-1]<thresh and v_vec[i]>thresh:
			spikes.append(t_vec[i])
		#
	#
	spike_num = len(spikes)
	duration = (t_vec[-1]-t_vec[0])/1000
	spike_freq = spike_num/duration

	return spike_freq
#
	

def AHP_dur(t_vec,v_vec,cur,thresh=0,delay=500):
	sptime = None
	pretime = None

	times = [x for x in numpy.arange(0,int(t_vec[-1]+1),h.dt)]
	for i in reversed(range(1,times.index(delay))):
		if v_vec[i-1]<thresh and v_vec[i]>thresh:
			pretime = t_vec[i]
			break
		#
	#
	for i in range(times.index(delay),len(t_vec)):
		if v_vec[i-1]<thresh and v_vec[i]>thresh:
			sptime = t_vec[i]
			break
		#
	#
	if pretime==None:
		pretime = delay
	if cur>50:
		pretime = delay
	if sptime==None:
		sptime = t_vec[-1]
	#

	AHP_dur = (sptime-pretime)/1000

	return AHP_dur
#