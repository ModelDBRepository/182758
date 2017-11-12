COMMENT

I_Ca.mod as Ca

Hodgkin-Huxley like calcium current as decribed in:
Terman D, Rubin JE, Yew AC, Wilson CJ (2002) Activity patterns in a model
for the subthalamopallidal network of the basal ganglia. J Neurosci 22:2963-76

ENDCOMMENT

NEURON {
	SUFFIX Ca
	NONSPECIFIC_CURRENT I
	RANGE g0, v0, theta_s, sigma_s
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

	theta_s
	sigma_s
}

ASSIGNED {
	I 		(mA/cm2)
	s_inf
}

INITIAL {
	rates(v)
}

BREAKPOINT {
	rates(v)

 	I=g0*s_inf*s_inf*(v-v0)
}

PROCEDURE rates(v(mV)) {  :Computes rate and other constants at current v.
	:Call once from HOC to initialize inf at resting v.

UNITSOFF
	s_inf = 1/(1+exp(-(v-theta_s)/sigma_s))
}

UNITSON