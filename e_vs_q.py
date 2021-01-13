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

fig = plt.figure(figsize=[3.32088,7])
ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2)
ax3 = fig.add_subplot(3, 1, 3)
alpha_keys = ['a02', 'a04', 'a08', 'a16']
markers = ['+', '*', '^', 'o']
colors = ['blue', 'green', 'orange', 'red']
labels = [r'$\alpha$ = 0.02', r'$\alpha$ = 0.04', r'$\alpha$ = 0.08', r'$\alpha$ = 0.16']

for alpha_key,marker,color,label in zip(alpha_keys,markers,colors,labels):
	h5f = h5py.File(f'final_fits_{alpha_key}.h5', 'r')
	qs = np.array(h5f['qs'])
	companion_masses = qs * 1000
	es_adaptive_mm08 = h5f['es_mm08']
	es_adaptive_kd06 = h5f['es_kd06']
	min_es_adaptive_mm08 = h5f['min_es_mm08'] 
	min_es_adaptive_kd06 = h5f['min_es_kd06']
	max_es_adaptive_mm08 = h5f['max_es_mm08']
	max_es_adaptive_kd06 = h5f['max_es_kd06']

	ax1.plot(companion_masses, es_adaptive_mm08, marker=marker, color=color, label=label, markersize=6, linestyle='None',linewidth=0.5, mfc='None')
	ax1.fill_between(companion_masses, min_es_adaptive_mm08, max_es_adaptive_mm08, alpha=0.3,color=color)
	ax2.plot(companion_masses, es_adaptive_kd06, marker=marker, color=color, label=label, markersize=6, linestyle='None',linewidth=0.5, mfc='None')
	ax2.fill_between(companion_masses, min_es_adaptive_kd06, max_es_adaptive_kd06, alpha=0.3,color=color)

ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_ylim(0.003,0.6)
plt.setp(ax1.get_xticklabels(), visible=False)
#ax1.set_xlabel('Mass Ratio')
ax1.set_ylabel('Eccentricity')
ax1.legend(loc='upper left', fontsize=7)
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_ylim(0.003,0.6)
#ax2.set_xlabel('Mass Ratio')
ax2.set_ylabel('Eccentricity')
plt.setp(ax2.get_xticklabels(), visible=False)
ax2.legend(loc='upper left', fontsize=7)

# ax2 = fig.add_subplot(2, 1, 2)

companion_mass   = [5,15,25,35,50,60,70,80,90,100,115,125,140,150,160]
a02 = [0.097391304, 0.126315789, 0.374347826, 0.453555556, 0.691276596, 0.706981132, 1.091020408, 1.214042553, 1.439347826, 1.616888889, 1.864888889, 1.965052632, 2.400212766, 2.313052632, 2.293488372]
a04 = [0.054347826, 0.086021505, 0.119148936, 0.432444444, 0.701041667, 0.697045455, 0.87, 0.949247312, 1.123225806, 1.189787234, 1.569791667, 1.866595745, 2.337173913, 2.434623656, 2.598064516]
a08 = [0.053978495, 0.117659574, 0.094893617, 0.063829787, 0.096304348, 0.686956522, 0.941086957, 0.856404494, 1.029777778, 1.407826087, 1.364347826, 1.307608696, 1.682978723, 2.070652174, 2.234347826]
a16 = [0.172043011, 0.162391304, 0.216842105, 0.12382821, 0.145227273, 0.108695652, 0.126315789, 0.123913043, 0.133695652, 0.147916667, 1.162391304, 1.155555556, 1.218, 1.302444444, 1.34172043]

ax3.plot(companion_mass, a02, marker='+', color='blue',  mfc='None',  label=r'$\alpha$ = 0.02')
ax3.plot(companion_mass, a04, marker='*', color='green',  mfc='None', label=r'$\alpha$ = 0.04')
ax3.plot(companion_mass, a08, marker='^', color='orange', mfc='None', label=r'$\alpha$ = 0.08')
ax3.plot(companion_mass, a16, marker='o', color='red',    mfc='None', label=r'$\alpha$ = 0.16')
ax3.set_xscale('log')
ax3.set_yscale('log')
ax3.set_xlabel(r'Companion Mass $(M_J)$')
ax3.set_ylabel(r'$r_c / a$')
ax3.legend(loc='upper left', fontsize=7)
plt.subplots_adjust(left=0.165,bottom=0.06,right=0.98,top=0.98, hspace=0.096)
plt.show()
