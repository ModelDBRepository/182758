import random

class Network:
	"""
	General cell network as described in:
	Terman D, Rubin JE, Yew AC, Wilson CJ (2002) Activity patterns in a model
	for the subthalamopallidal network of the basal ganglia. J Neurosci 22:2963-76
	#
	A network of *N* STN and *N* GPe cells, where each cell n makes connections 
	as defined below.
	#
	Subtypes of networks include:
	Random, Sparsely-Connected (RSC)
	Structured, Sparsely-Connected (SSC)
	Structured, Tightly-Connected (STC)
	#
	"""
	#
	def __init__(self,N=8,delay=0,dur=1e9,amp=0,loc=0.5,g2s=0,s2g=0,g2g=0):
		"""
		:param N: Number of cells.
		"""
		self._N = N              # Total number of cells in the net
		self.delay = delay
		self.dur = dur
		self.amp = amp
		self.loc = loc
		self.s2g = s2g
		self.g2s = g2s
		self.g2g = g2g
		self.t_vec = h.Vector()   # Spike time of all cells
		self.id_vec = h.Vector()  # Ids of spike times
		#
		self.set_numcells(N)  # Actually build the net.
	#
	def set_numcells(self, N):
		"""Create, layout, and connect N cells."""
		self.create_cells(N)
		self.connect_cells()
		self.connect_stim()
	#
	def create_cells(self, N):
		"""Create and layout N cells in the network."""
		self.stn_cells = []
		self.gpe_cells = []
		for i in range(N):
			# create cell pair
			ident = str(i+1)
			stn = STN()
			gpe = GPe(delay=self.delay,dur=self.dur,amp=self.amp,loc=self.loc,cur=True)
			stn.ident = 'stn%s' % (ident)
			gpe.ident = 'gpe%s' % (ident)
			# reposition cell pair
			stn.set_position(i*25,-10,0)
			gpe.set_position(i*25,10,0)
			# add pair to cell lists
			self.stn_cells.append(stn)
			self.gpe_cells.append(gpe)
	#
	def connect_cells(self):
		"""Create list of which cells will connect as follows:
		syn_list[i] = (postcell,precells_G2S,precells_S2G,precells_G2G)
		"""
		raise NotImplementedError("create_sections() is not implemented.")
		#
	#
	def connect_stim(self):
		for post in range(len(self.syn_list)):
			for pre in self.syn_list[post][1]:
				self.syn_list[post][0].create_synapse(pre,'G2S',self.g2s)
			#
			for pre in self.syn_list[post][2]:
				self.syn_list[post][0].create_synapse(pre,'S2G',self.s2g)
			#
			for pre in self.syn_list[post][3]:
				self.syn_list[post][0].create_synapse(pre,'G2G',self.g2g)
			#
		#
	#
	def get_spikes(self):
		"""Get the spikes as a list of lists."""
		return spiketrain.netconvecs_to_listoflists(self.t_vec, self.id_vec)


class RSC(Network):
	"""
	Random, Sparsely-Connected Network
	#
	A network of *N* STN and *N* GPe cells, where each cell n makes connections 
	as defined below.
	#
	Each STN cell excites 1 randomly selected GPe cell.
	Each GPe cell inhibits 3 randomly selected STN cells.
	Each GPe cell inhibits all GPe cells.
	#
	"""
	def connect_cells(self,s2g=1,g2s=3):
		"""Create list of which cells will connect as follows:
		syn_list[i] = (postcell,precells_G2S,precells_S2G,precells_G2G)
		"""
		self.syn_list = []
		N = self._N
		for i in range(N):
			# Create STN to GPe excitatory connections
			syns = random.sample(self.gpe_cells,s2g)
			self.syn_list.append((self.stn_cells[i],syns,[],[]))
			#
			# Create GPe to STN excitatory connections
			syns_s = random.sample(self.stn_cells,g2s)
			#
			# Create GPe to GPe excitatory connections
			syns_g = self.gpe_cells
			self.syn_list.append((self.gpe_cells[i],[],syns_s,syns_g))
		#
	#
#

class SSC(Network):
	"""
	Structured, Sparsely-Connected Network
	#
	A network of *N* STN and *N* GPe cells, where each cell n makes connections 
	as defined below.
	#
	Each STN cell excites the 1 closest GPe cell.
	Each GPe cell inhibits 2 STN cells skipping the 3 closest.
	Each GPe cell inhibits the 2 closest GPe cells.
	Periodic boundary conditions are used.
	#
	"""
	def connect_cells(self):
		"""Create list of which cells will connect as follows:
		syn_list[i] = (postcell,precells_G2S,precells_S2G,precells_G2G)
		"""
		self.syn_list = []
		N = self._N
		for i in range(N):
			# Create STN to GPe excitatory connections
			syns = [self.gpe_cells[i]]
			self.syn_list.append((self.stn_cells[i],syns,[],[]))
			#
			# Create GPe to STN excitatory connections
			syns_s = [self.stn_cells[(i-2)%N],self.stn_cells[(i+2)%N]]
			#
			# Create GPe to GPe excitatory connections
			syns_g = [self.gpe_cells[(i-1)%N],self.gpe_cells[(i+1)%N]]
			self.syn_list.append((self.gpe_cells[i],[],syns_s,syns_g))
		#
	#
#

class STC(Network):
	"""
	Structured, Tightly-Connected Network
	#
	A network of *N* STN and *N* GPe cells, where each cell n makes connections 
	as defined below.
	#
	Each STN cell excites the 3 closest GPe cells (i=i-1,i=i,i=i+1).
	Each GPe cell inhibits the 5 closest STN cells (i=i-2:i=i+2.
	Each GPe cell inhibits all GPe cells, excluding itself.
	#
	"""
	def connect_cells(self):
		"""Create list of which cells will connect as follows:
		syn_list[i] = (postcell,precells_G2S,precells_S2G,precells_G2G)
		"""
		self.syn_list = []
		N = self._N
		for i in range(N):
			# Create STN to GPe excitatory connections
			syns = []
			for j in range(-1,2):
				syns.append(self.gpe_cells[(i+j)%N])
			#
			self.syn_list.append((self.stn_cells[i],syns,[],[]))
			#
			# Create GPe to STN excitatory connections
			syns_s = []
			for j in range(-2,3):
				syns_s.append(self.stn_cells[(i+j)%N])
			#
			# Create GPe to GPe excitatory connections
			syns_g = self.gpe_cells
			self.syn_list.append((self.gpe_cells[i],[],syns_s,syns_g))
		#
	#
#