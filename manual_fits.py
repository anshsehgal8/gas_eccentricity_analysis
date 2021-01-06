#!/usr/bin/env python3
import argparse
import numpy as np
import h5py
import matplotlib.pyplot as plt
import loaders
import glob
import os


def configure_matplotlib(hardcopy=False):
	plt.rc('xtick', labelsize=8)
	plt.rc('ytick', labelsize=8)
	plt.rc('axes', labelsize=8)
	plt.rc('legend', fontsize=8)
	plt.rc('font', family='Times New Roman' if hardcopy else 'DejaVu Sans', size=8)
	plt.rc('text', usetex=hardcopy)




configure_matplotlib(hardcopy=True)

fig = plt.figure(figsize=[3.32088,5])
ax1 = fig.add_subplot(2, 1, 1)
alpha_keys = ['a02', 'a04', 'a08', 'a16']
markers = ['+', '*', '^', 'o']
colors = ['blue', 'green', 'orange', 'red']
labels = [r'$\alpha$ = 0.02', r'$\alpha$ = 0.04', r'$\alpha$ = 0.08', r'$\alpha$ = 0.16']

for alpha_key,marker,color,label in zip(alpha_keys,markers,colors,labels):
	h5f = h5py.File(f'final_fits_{alpha_key}.h5', 'r')
	qs = h5f['qs']
	es_adaptive_mm08 = h5f['es_mm08']
	es_adaptive_kd06 = h5f['es_kd06']
	min_es_adaptive_mm08 = h5f['min_es_mm08'] 
	min_es_adaptive_kd06 = h5f['min_es_kd06']
	max_es_adaptive_mm08 = h5f['max_es_mm08']
	max_es_adaptive_kd06 = h5f['max_es_kd06']

	ax1.plot(qs, es_adaptive_kd06, marker=marker, color=color, label=label, markersize=6, linestyle='None',linewidth=0.5, mfc='None')
	ax1.fill_between(qs, min_es_adaptive_kd06, max_es_adaptive_kd06, alpha=0.3,color=color)

ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel('Mass Ratio')
ax1.set_ylabel('Eccentricity')
ax1.legend()

ax2 = fig.add_subplot(2, 1, 2)

q   = [0.005,0.015,0.025,0.035,0.05,0.06,0.07,0.08,0.09,0.1,0.115,0.125,0.14,0.15,0.16]
a02 = [0.097391304, 0.126315789, 0.374347826, 0.453555556, 0.691276596, 0.706981132, 1.091020408, 1.214042553, 1.439347826, 1.616888889, 1.864888889, 1.965052632, 2.400212766, 2.313052632, 2.293488372]
a04 = [0.054347826, 0.086021505, 0.119148936, 0.432444444, 0.701041667, 0.697045455, 0.87, 0.949247312, 1.123225806, 1.189787234, 1.569791667, 1.866595745, 2.337173913, 2.434623656, 2.598064516]
a08 = [0.053978495, 0.117659574, 0.094893617, 0.063829787, 0.096304348, 0.686956522, 0.941086957, 0.856404494, 1.029777778, 1.407826087, 1.364347826, 1.307608696, 1.682978723, 2.070652174, 2.234347826]
a16 = [0.172043011, 0.162391304, 0.216842105, 0.12382821, 0.145227273, 0.108695652, 0.126315789, 0.123913043, 0.133695652, 0.147916667, 1.162391304, 1.155555556, 1.218, 1.302444444, 1.34172043]

ax2.plot(q, a02, marker='+', color='blue', mfc='None',  label=r'$\alpha$ = 0.02')
ax2.plot(q, a04, marker='*', color='green', mfc='None', label=r'$\alpha$ = 0.04')
ax2.plot(q, a08, marker='^', color='orange', mfc='None', label=r'$\alpha$ = 0.08')
ax2.plot(q, a16, marker='o', color='red', mfc='None', label=r'$\alpha$ = 0.16')
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_xlabel('Mass Ratio')
ax2.set_ylabel(r'$r_c / a$')
ax2.legend()
plt.subplots_adjust(left=0.165,bottom=0.09,right=0.98,top=0.98)
plt.show()
