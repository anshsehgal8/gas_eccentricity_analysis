#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


def configure_matplotlib(hardcopy=False):
	plt.rc('xtick', labelsize=8)
	plt.rc('ytick', labelsize=8)
	plt.rc('axes', labelsize=8)
	plt.rc('legend', fontsize=8)
	plt.rc('font', family='Times New Roman' if hardcopy else 'DejaVu Sans', size=8)
	plt.rc('text', usetex=hardcopy)

configure_matplotlib(hardcopy=True)

q = [0.005,0.015,0.025,0.035,0.05,0.06,0.07,0.08,0.09,0.1,0.115,0.125,0.14,0.15,0.16]

a02 = [0.097391304, 0.126315789, 0.374347826, 0.453555556, 0.691276596, 0.706981132, 1.091020408, 1.214042553, 1.439347826, 1.616888889, 1.864888889, 1.965052632, 2.400212766, 2.313052632, 2.293488372]
a04 = [0.054347826, 0.086021505, 0.119148936, 0.432444444, 0.701041667, 0.697045455, 0.87, 0.949247312, 1.123225806, 1.189787234, 1.569791667, 1.866595745, 2.337173913, 2.434623656, 2.598064516]
a08 = [0.053978495, 0.117659574, 0.094893617, 0.063829787, 0.096304348, 0.686956522, 0.941086957, 0.856404494, 1.029777778, 1.407826087, 1.364347826, 1.307608696, 1.682978723, 2.070652174, 2.234347826]
a16 = [0.172043011, 0.162391304, 0.216842105, 0.12382821, 0.145227273, 0.108695652, 0.126315789, 0.123913043, 0.133695652, 0.147916667, 1.162391304, 1.155555556, 1.218, 1.302444444, 1.34172043]

plt.figure()
plt.plot(q, a02, marker='+', color='blue',  label='a02')
plt.plot(q, a04, marker='^', color='orange',   label='a04')
plt.plot(q, a08, marker='o', color='green',    label='a08')
plt.plot(q, a16, marker='*', color='red', label='a16')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Mass Ratio')
plt.ylabel(r'$r_c / a$')
plt.legend()
plt.show()
