COMMENT

add CA dependence?

I_K.mod as K

Hodgkin-Huxley like potassium current as decribed in:
Terman D, Rubin JE, Yew AC, Wilson CJ (2002) Activity patterns in a model
for the subthalamopallidal network of the basal ganglia. J Neurosci 22:2963-76

ENDCOMMENT

NEURON {
	SUFFIX K
	NONSPECIFIC_CURRENT I
	RANGE g0, v0, tau_0n, tau_1n, phi_n, theta_tn, theta_n, sigma_tn, sigma_n
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

	phi_n
	theta_tn
	theta_n
	sigma_tn
	sigma_n
	tau_0n	(ms)
	tau_1n 	(ms)
}

ASSIGNED {	
	I 		(mA/cm2)
	n_inf
	tau_n	(ms)
}

STATE {
	n
}

INITIAL {
	rates(v)
	n = n_inf
}

BREAKPOINT {
 	SOLVE states METHOD cnexp

 	I=g0*(n*n*n*n)*(v-v0)
}

DERIVATIVE states {
	rates(v)
	n' = phi_n*((n_inf-n)/tau_n)
}

PROCEDURE rates(v(mV)) {  :Computes rate and other constants at current v.
	:Call once from HOC to initialize inf at resting v.

UNITSOFF
	tau_n = tau_0n + tau_1n/(1+exp(-(v-theta_tn)/sigma_tn))
	n_inf = 1/(1+exp(-(v-theta_n)/sigma_n))
}

UNITSON