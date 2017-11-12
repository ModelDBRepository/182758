COMMENT

I_syn.mod as syn

Point process to create synapse between GPe cells and/or STN cells using Hodgkin-Huxley like currents as decribed in:
Terman D, Rubin JE, Yew AC, Wilson CJ (2002) Activity patterns in a model
for the subthalamopallidal network of the basal ganglia. J Neurosci 22:2963-76

To differentiate between GPe to STN, GPe to GPe, or STN to GPe range parameters are set accordingly.

ENDCOMMENT

NEURON {
	POINT_PROCESS syn
	POINTER vg
	NONSPECIFIC_CURRENT I
	RANGE g0, v0, theta_g, theta_Hg, sigma_Hg, alpha, beta, s, H_inf,vh
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	(S) = (siemens)
}

PARAMETER {
	v 		(mV)
	g0 		(S/cm2)
	v0 		(mV)
	vg		(mV)

	theta_g
	theta_Hg
	sigma_Hg
	alpha 	(ms-1)
	beta 	(ms-1)
}

ASSIGNED {
	I 		(mA/cm2)
	vh 		(mV)
	H_inf
}

STATE {
	s
}

INITIAL {
	rates(v)
	s = 0
}

BREAKPOINT {
 	SOLVE states METHOD cnexp

 	I=g0*(v-v0)*s
}

DERIVATIVE states {
	rates(v)
	s' = alpha*H_inf*(1-s)-beta*s
}

PROCEDURE rates(v(mV)) {  :Computes rate and other constants at current v.
	:Call once from HOC to initialize inf at resting v.

UNITSOFF
	vh = vg-theta_g
	H_inf = 1/(1+exp(-(vh-theta_Hg)/sigma_Hg))
}

UNITSON