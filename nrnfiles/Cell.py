class Cell(object):
	"""Generic cell template."""
	#
	def __init__(self):
		self.x = 0; self.y = 0; self.z = 0
		self.soma = None
		self.Syn_list = []
		self.Iscale = 0.1
		self.create_sections()
		self.build_subsets()
		self.define_geometry()
		self.define_biophysics()
	#   
	def create_sections(self):
		"""Create the sections of the cell. Remember to do this
		in the form::
		
		h.Section(name='soma', cell=self)
		   
		"""
		raise NotImplementedError("create_sections() is not implemented.")
	#
	def define_geometry(self):
		"""Set the 3D geometry of the cell."""
		raise NotImplementedError("define_geometry() is not implemented.")
	#
	def define_biophysics(self):
		"""Assign the membrane properties across the cell."""
		raise NotImplementedError("define_biophysics() is not implemented.")
	#
	def connect2self(self, thresh=10):
		"""Make a new NetCon with this cell's membrane
		potential at the soma as the source (i.e. the spike detector)
		onto the target passed in (i.e. a synapse on a cell).
		Subclasses may override with other spike detectors."""
		nc = h.NetCon(self.soma(0.5)._ref_v, self.soma)
		nc.threshold = thresh
		return nc
	#
	def get_spikes(self):
		"""Get the spikes as a list of lists."""
		return spiketrain.netconvecs_to_listoflists(self.t_vec, self.id_vec)
	#

	def create_synapse(self,pre,type,g0):
		"""Subclasses should create synapses (such as ExpSyn) at various
		segments and add them to self.Syn_list."""
		#
		syn = h.syn(0.5, sec=self.soma)
		h.setpointer(pre.soma(0.5)._ref_v, 'vg', syn)
		#
		if type=='G2S':
			syn.g0 = g0*self.Iscale
			syn.theta_Hg = -39.0
			syn.theta_g = 30.0
			syn.sigma_Hg = 8.0
			syn.alpha = 5.0
			syn.beta = 1.0
			syn.v0 = -85.0
		#
		if type=='G2G' or type=='S2G':
			syn.theta_Hg = -57.0
			syn.theta_g = 20.0
			syn.sigma_Hg = 2.0
			syn.alpha = 2.0
			syn.beta = 0.08
		#
		if type=='S2G':
			syn.g0 = g0*self.Iscale
			syn.v0 = 0.0
		#
		if type=='G2G':
			syn.g0 = g0*self.Iscale
			syn.v0 = -100.0
		#
		self.Syn_list.append(syn)
	#
	def build_subsets(self):
		"""Build subset lists. This defines 'all', but subclasses may
		want to define others. If overridden, call super() to include 'all'."""
		self.all = h.SectionList()
		self.all.wholetree(sec=self.soma)
	#
	def attach_current_clamp(self):
		"""Attach a current Clamp to a cell.
		#
		:param cell: Cell object to attach the current clamp.
		:param delay: Onset of the injected current.
		:param dur: Duration of the stimulus.
		:param amp: Magnitude of the current.
		:param loc: Location on the dendrite where the stimulus is placed.
		"""
		stim = h.IClamp(self.soma(self.loc))
		stim.delay = self.delay
		stim.dur = self.dur
		stim.amp = self.amp
		#
		return stim
	#
	def set_position(self, x, y, z):
		"""
		Set the base location in 3D and move all other
		parts of the cell relative to that location.
		"""
		for sec in self.all:
			for i in range(int(h.n3d())):
				h.pt3dchange(i, \
					x-self.x+h.x3d(i), \
					y-self.y+h.y3d(i), \
					z-self.z+h.z3d(i), \
					h.diam3d(i))
		self.x = x; self.y = y; self.z = z
	#
	def shape_3D(self):
		"""
		Set the default shape of the cell in 3D coordinates.
		Set soma(0) to the origin (0,0,0)
		"""
		len1 = self.soma.L
		self.soma.push()
		h.pt3dclear()
		h.pt3dadd(0, 0, 0, self.soma.diam)
		h.pt3dadd(len1, 0, 0, self.soma.diam)
		h.pop_section()