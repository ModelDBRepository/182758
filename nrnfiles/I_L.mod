COMMENT

I_L.mod as l

Hodgkin-Huxley like leak current as decribed in:
Terman D, Rubin JE, Yew AC, Wilson CJ (2002) Activity patterns in a model
for the subthalamopallidal network of the basal ganglia. J Neurosci 22:2963-76

ENDCOMMENT

NEURON {
	SUFFIX l
	NONSPECIFIC_CURRENT I
	RANGE g0, v0
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	(S) = (siemens)
}

PARAMETER {
	v 	(mV)
	g0 	(S/cm2)
	v0 	(mV)
}

ASSIGNED {
	I 	(mA/cm2)
}

BREAKPOINT {
 	I=g0*(v-v0)
}