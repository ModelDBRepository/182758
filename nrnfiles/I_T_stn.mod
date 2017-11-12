COMMENT

I_T_stn.mod as Tstn

Hodgkin-Huxley like T current for STN cells 0as decribed in:
Terman D, Rubin JE, Yew AC, Wilson CJ (2002) Activity patterns in a model
for the subthalamopallidal network of the basal ganglia. J Neurosci 22:2963-76

ENDCOMMENT

NEURON {
	SUFFIX Tstn
	NONSPECIFIC_CURRENT I
	RANGE g0, v0, tau_0r, tau_1r, phi_r, theta_tr, theta_r, sigma_tr, sigma_r, theta_a, sigma_a, theta_b, sigma_b, b_inf, a_inf, r, tau_r
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

	phi_r
	theta_tr
	theta_r
	sigma_tr
	sigma_r
	tau_0r	(ms)
	tau_1r 	(ms)

	theta_a
	sigma_a

	theta_b
	sigma_b
}

ASSIGNED {
	I 		(mA/cm2)
	r_inf
	tau_r	(ms)
	a_inf
	b_inf
}

STATE {
	r
}

INITIAL {
	rates(v)
	r = r_inf
}

BREAKPOINT {
 	SOLVE states METHOD cnexp

	b_inf = 1/(1+exp((r-theta_b)/sigma_b))-1/(1+exp(-theta_b/sigma_b))

 	I=g0*(a_inf*a_inf*a_inf)*(b_inf*b_inf)*(v-v0)
}

DERIVATIVE states {
	rates(v)
	r' = phi_r*((r_inf-r)/tau_r)
}

PROCEDURE rates(v(mV)) {  :Computes rate and other constants at current v.
	:Call once from HOC to initialize inf at resting v.

UNITSOFF
	tau_r = tau_0r + tau_1r/(1+exp(-(v-theta_tr)/sigma_tr))
	r_inf = 1/(1+exp(-(v-theta_r)/sigma_r))

	a_inf = 1/(1+exp(-(v-theta_a)/sigma_a))
}

UNITSON