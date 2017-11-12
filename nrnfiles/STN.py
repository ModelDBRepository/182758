class STN(Cell):  #### Inherits from Cell
	"""Creates basic STN cell with soma only, inserts
	currents, and sets parameters."""
	#
	def __init__(self, delay=0, dur=1e9, amp=0, loc=0.5):
		super(STN,self).__init__()
		self.ident = 'stn'
		self.delay = delay
		self.dur = dur
		self.amp = amp
		self.loc = loc
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
			sec.cm = 100    # Membrane capacitance in micro Farads / cm^2
		#
		# Insert appropiate currents
		self.soma.insert('l')
		self.soma.insert('K')
		self.soma.insert('Na')
		self.soma.insert('Tstn')
		self.soma.insert('Ca')
		self.soma.insert('AHP')
		# Set intercurrent pointers
		h.setpointer(self.soma(0.5)._ref_I_Ca, 'I_Ca', self.soma(0.5).AHP)
		h.setpointer(self.soma(0.5)._ref_I_Tstn, 'I_T', self.soma(0.5).AHP)
		self.soma.Ca0_AHP = 0.3
		#
		# Set current parameters
		self.soma.g0_l = 2.25*self.Iscale
		self.soma.g0_K = 45.0*self.Iscale
		self.soma.g0_Na = 37.5*self.Iscale
		self.soma.g0_Tstn = 0.5*self.Iscale
		self.soma.g0_Ca = 0.5*self.Iscale
		self.soma.g0_AHP = 9.0*self.Iscale
		#
		self.soma.v0_l = -60.0
		self.soma.v0_K = self.soma.v0_AHP = -80.0
		self.soma.v0_Na = 55.0
		self.soma.v0_Ca = self.soma.v0_Tstn = 140.0
		#
		self.soma.tau_1h_Na = 500.0
		self.soma.tau_1n_K = 100.0
		self.soma.tau_1r_Tstn = 17.5
		self.soma.tau_0h_Na = 1.0
		self.soma.tau_0n_K = 1.0
		self.soma.tau_0r_Tstn = 40.0
		#
		self.soma.phi_h_Na = 0.75
		self.soma.phi_n_K = 0.75
		self.soma.phi_r_Tstn = 0.2
		#
		self.soma.k1_AHP = 15.0
		self.soma.kca_AHP = 22.5
		self.soma.epsilon_AHP = 5e-5
		#
		self.soma.theta_m_Na = -30.0
		self.soma.theta_h_Na = -39.0
		self.soma.theta_n_K = -32.0
		self.soma.theta_r_Tstn = -67.0
		self.soma.theta_a_Tstn = -63.0
		self.soma.theta_b_Tstn = 0.4
		self.soma.theta_s_Ca = -39.0
		#
		self.soma.theta_th_Na = -57.0
		self.soma.theta_tn_K = -80.0
		self.soma.theta_tr_Tstn = 68.0
		#
		self.soma.sigma_m_Na = 15.0
		self.soma.sigma_h_Na = -3.1
		self.soma.sigma_n_K = 8.0
		self.soma.sigma_r_Tstn = -2.0
		self.soma.sigma_a_Tstn = 7.8
		self.soma.sigma_b_Tstn = -0.1
		self.soma.sigma_s_Ca = 8.0
		#
		self.soma.sigma_th_Na = -3.0
		self.soma.sigma_tn_K = -26.0
		self.soma.sigma_tr_Tstn = -2.2