#!/usr/bin/env python3

import argparse
import numpy as np
import h5py
import matplotlib.pyplot as plt
import loaders
import glob
import os


#################################################################
#  This script needs to:
#    1. Open each eccentricity_measures script
#	 2. Extract MM08_vs_r and KD06_vs_r
#    3. Use sigma_vs_r to find radial cut
#    4. Find a global e value from the radial cut
#    5. Time Average after saturation
#################################################################

def get_global_e(filename):
	mm08_e_vs_r   = np.array(h5py.File(filename, 'r')['mm08_e_vs_r'])
	kd06_e_vs_r   = np.array(h5py.File(filename, 'r')['kd06_e_vs_r'])
	sigma_vs_r    = np.array(h5py.File(filename, 'r')['sigma_vs_r'])
	domain_radius = np.array(h5py.File(filename, 'r')['run_config']['domain_radius'])
	r = np.linspace(0, domain_radius, len(sigma_vs_r))
	max_sigma_r =  np.argmax(sigma_vs_r)
	min_sigma_r =  np.argmin(sigma_vs_r[0:50])
	mm08_e_small = np.mean(mm08_e_vs_r[12:18])
	mm08_e_large = np.mean(mm08_e_vs_r[17:54])
	mm08_e_adaptive = np.mean(mm08_e_vs_r[min_sigma_r:max_sigma_r])
	kd06_e_small = np.mean(kd06_e_vs_r[12:18])
	kd06_e_large = np.mean(kd06_e_vs_r[17:54])
	kd06_e_adaptive = np.mean(kd06_e_vs_r[min_sigma_r:max_sigma_r])
	return mm08_e_small,mm08_e_large,mm08_e_adaptive




def configure_matplotlib(hardcopy=False):
	plt.rc('xtick', labelsize=8)
	plt.rc('ytick', labelsize=8)
	plt.rc('axes', labelsize=8)
	plt.rc('legend', fontsize=8)
	plt.rc('font', family='Times New Roman' if hardcopy else 'DejaVu Sans', size=8)
	plt.rc('text', usetex=hardcopy)




if __name__ == "__main__":
	# parser = argparse.ArgumentParser()
	# parser.add_argument("filenames", nargs='+')
	# args = parser.parse_args()

	configure_matplotlib(hardcopy=True)

	alpha_keys = ['a02','a04','a08','a16']
	markers = ['+','^','.','*']
	colors =  ['blue','orange','green','red']
	labels = [r'$\alpha$ = 0.02', r'$\alpha$ = 0.04', r'$\alpha$ = 0.08', r'$\alpha$ = 0.16']
	fig = plt.figure()
	ax1 = fig.add_subplot(1, 1, 1)
	qs = [0.005,0.01,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.07,0.075,0.080,0.085,0.090,0.095,0.10,0.105,0.11,0.115,0.12,0.125,0.13,0.135,0.14,0.145,0.15,0.155,0.16]




	rundirs = [f for f in sorted(glob.glob(f'data/q_suite_v2/q????-a08-b64'))]

	es_small = []
	min_es_small = []
	max_es_small = []
	es_large = []
	min_es_large = []
	max_es_large = []
	es_adaptive = []
	min_es_adaptive = []
	max_es_adaptive = []

	
	for rundir in rundirs:
		filenames = sorted(glob.glob(os.path.join(rundir, 'eccentricity_measures.????.h5')))
		e_per_file_small = []
		e_per_file_large = []
		e_per_file_adaptive = []
		for filename in filenames:
			mm08_e_small,mm08_e_large,mm08_e_adaptive = get_global_e(filename)
			e_per_file_small.append(mm08_e_small)
			e_per_file_large.append(mm08_e_large)
			e_per_file_adaptive.append(mm08_e_adaptive)

		es_small.append(np.mean(e_per_file_small[-50:]))
		min_es_small.append(np.min(e_per_file_small[-50:]))
		max_es_small.append(np.max(e_per_file_small[-50:]))
		es_large.append(np.mean(e_per_file_large[-50:]))
		min_es_large.append(np.min(e_per_file_large[-50:]))
		max_es_large.append(np.max(e_per_file_large[-50:]))
		es_adaptive.append(np.mean(e_per_file_adaptive[-50:]))
		min_es_adaptive.append(np.min(e_per_file_adaptive[-50:]))
		max_es_adaptive.append(np.max(e_per_file_adaptive[-50:]))


	ax1.plot(qs, es_small, marker='+', color='red', label='small', markersize=6, linestyle='None',linewidth=0.5, mfc='None')
	ax1.plot(qs, es_large, marker='*', color='black', label='large', markersize=6, linestyle='None',linewidth=0.5, mfc='None')
	ax1.plot(qs, es_adaptive, marker='.', color='blue', label='adaptive', markersize=6, linestyle='None',linewidth=0.5, mfc='None')
	ax1.fill_between(qs, min_es_small, max_es_small, alpha=0.3)
	ax1.fill_between(qs, min_es_large, max_es_large, alpha=0.3)
	ax1.fill_between(qs, min_es_adaptive, max_es_adaptive, alpha=0.3)
	ax1.set_xscale('log')
	ax1.set_yscale('log')
	ax1.set_xlabel('Mass Ratio')
	ax1.set_ylabel('Eccentricity')


	
	plt.legend()
	plt.show()

