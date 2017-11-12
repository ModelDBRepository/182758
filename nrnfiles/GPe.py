class GPe(Cell):  #### Inherits from Cell
	"""Creates basic STN cell with soma only, inserts
	currents, and sets parameters."""
	#
	def __init__(self, delay=0, dur=1e9, amp=0, loc=0.5, cur=False):
		super(GPe,self).__init__()
		self.ident = 'gpe'
		self.delay = delay
		self.dur = dur
		self.amp = amp
		self.loc = loc
		if cur==True:
			self.stim = self.attach_current_clamp()
		#
	#
	def create_sections(self):
		"""Create the sections of the cell."""
		self.soma = h.Section(name='soma', cell=self)
	#
	def define_geometry(self):
		"""Set the 3D geometry of the cell."""
		self.soma.L = self.soma.diam = 12.6157 # microns
		self.shape_3D()
	#
	def define_biophysics(self):
		"""Assign the membrane properties across the cell."""
		for sec in self.all: # 'all' exists in parent object.
			sec.Ra = 100    # Axial resistance in Ohm * cm
			sec.cm = 100      # Membrane capacitance in micro Farads / cm^2
		#
		# Insert appropiate currents
		self.soma.insert('l')
		self.soma.insert('K')
		self.soma.insert('Na')
		self.soma.insert('Tgpe')
		self.soma.insert('Ca')
		self.soma.insert('AHP')
		#
		# Set intercurrent pointers
		h.setpointer(self.soma(0.5)._ref_I_Ca, 'I_Ca', self.soma(0.5).AHP)
		h.setpointer(self.soma(0.5)._ref_I_Tgpe, 'I_T', self.soma(0.5).AHP)
		self.soma.Ca0_AHP = 0.02
		#
		# Set current parameters
		#
		self.soma.g0_l = 0.1*self.Iscale
		self.soma.g0_K = 30.0*self.Iscale
		self.soma.g0_Na = 120.0*self.Iscale
		self.soma.g0_Tgpe = 0.5*self.Iscale
		self.soma.g0_Ca = 0.15*self.Iscale
		self.soma.g0_AHP = 30.0*self.Iscale
		#
		self.soma.v0_l = -55.0
		self.soma.v0_K = self.soma.v0_AHP = -80.0
		self.soma.v0_Na = 55.0
		self.soma.v0_Ca = self.soma.v0_Tgpe = 120.0
		#
		self.soma.tau_1h_Na = 0.27
		self.soma.tau_1n_K = 0.27
		self.soma.tau_0h_Na = 0.05
		self.soma.tau_0n_K = 0.05
		self.soma.tau_r_Tgpe = 30.0
		#
		self.soma.phi_h_Na = 0.05
		self.soma.phi_n_K = 0.05
		self.soma.phi_r_Tgpe = 1.0
		#
		self.soma.k1_AHP = 30.0
		self.soma.kca_AHP = 20.0
		self.soma.epsilon_AHP = 1e-4
		#
		self.soma.theta_m_Na = -37.0
		self.soma.theta_h_Na = -58.0
		self.soma.theta_n_K = -50.0
		self.soma.theta_r_Tgpe = -70.0
		self.soma.theta_a_Tgpe = -57.0
		self.soma.theta_s_Ca = -35.0
		#
		self.soma.theta_th_Na = -40.0
		self.soma.theta_tn_K = -40.0
		#
		self.soma.sigma_m_Na = 10.0
		self.soma.sigma_h_Na = -12.0
		self.soma.sigma_n_K = 14.0
		self.soma.sigma_r_Tgpe = -2.0 
		self.soma.sigma_a_Tgpe = 2.0
		self.soma.sigma_s_Ca = 2.0
		#
		self.soma.sigma_th_Na = -12.0
		self.soma.sigma_tn_K = -12.0
		#
	#