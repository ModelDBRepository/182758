COMMENT

I_Na.mod as Na

Hodgkin-Huxley like sodium current as decribed in:
Terman D, Rubin JE, Yew AC, Wilson CJ (2002) Activity patterns in a model
for the subthalamopallidal network of the basal ganglia. J Neurosci 22:2963-76

ENDCOMMENT

NEURON {
	SUFFIX Na
	NONSPECIFIC_CURRENT I
	RANGE g0, v0, tau_0h, tau_1h, phi_h, theta_th, theta_h, sigma_th, sigma_h, theta_m, sigma_m
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

	phi_h
	theta_th
	theta_h
	sigma_th
	sigma_h
	tau_0h	(ms)
	tau_1h 	(ms)

	theta_m
	sigma_m
}

ASSIGNED {
	I 		(mA/cm2)
	h_inf
	tau_h	(ms)
	m_inf
}

STATE {
	h
}

INITIAL {
	rates(v)
	h = h_inf
}

BREAKPOINT {
 	SOLVE states METHOD cnexp

 	I=g0*(m_inf*m_inf*m_inf)*h*(v-v0)
}

DERIVATIVE states {
	rates(v)
	h' = phi_h*((h_inf-h)/tau_h)
}

PROCEDURE rates(v(mV)) {  :Computes rate and other constants at current v.
	:Call once from HOC to initialize inf at resting v.

UNITSOFF
	tau_h = tau_0h + tau_1h/(1+exp(-(v-theta_th)/sigma_th))
	h_inf = 1/(1+exp(-(v-theta_h)/sigma_h))

	m_inf = 1/(1+exp(-(v-theta_m)/sigma_m))
}

UNITSON