#!/usr/bin/env python3

import os
import glob
import numpy as np
import h5py
import matplotlib.pyplot as plt
import itertools




def plot_phase_time_series(ax,filename):	
	t   = np.array(h5py.File(filename, 'r')['t_mm08'])
	cumphase = h5py.File(filename, 'r')['cumphase']
	orbits = t[0:-1] / 2 / np.pi
	ax.plot(orbits,cumphase)



def make_figure_phase_time_series():
	fig = plt.figure()
	ax1 = fig.add_subplot(1,1,1)
	filenames = [f for f in sorted(glob.glob(f'data/q_suite_v2/q????-a08-b64/time_series.h5'))]
	for filename in filenames:
		plot_phase_time_series(ax1,filename)
	plt.xlabel('Orbits')
	plt.ylabel('Precession Rate')
	return fig



def plot_eccentricity_time_series(ax1,ax2,filename):
	orbits_1 = np.array(h5py.File(filename, 'r')['t_mm08'])
	orbits_1 = orbits_1 / 2. / np.pi
	e1       = h5py.File(filename, 'r')['e_mm08']
	orbits_2 = np.array(h5py.File(filename, 'r')['t_kd06'])
	orbits_2 = orbits_2 / 2. / np.pi
	e2       = h5py.File(filename, 'r')['e_kd06']
	ax1.plot(orbits_1, e1)
	ax2.plot(orbits_2, e2)



def make_figure_eccentricity_time_series():
	fig = plt.figure()
	ax1 = fig.add_subplot(1, 2, 1)
	ax2 = fig.add_subplot(1, 2, 2)

	filenames = [f for f in sorted(glob.glob(f'data/q_suite_v2/q????-a08-b64/time_series.h5'))]

	for filename in filenames:
		plot_eccentricity_time_series(ax1, ax2, filename)

	ax1.set_yscale('log')
	ax2.set_yscale('log')
	ax1.set_ylim(1e-3, 1.0)
	ax2.set_ylim(1e-3, 1.0)
	ax1.set_xlabel('Orbits')
	ax2.set_xlabel('Orbits')
	ax1.set_title('MM08')
	ax2.set_title('KD06')
	ax1.set_ylabel('Eccentricity measure')
	return fig



def plot_precession_versus_q(ax, filename, marker):
	qs = h5py.File(filename, 'r')['qs_prec']
	precessions = h5py.File(filename, 'r')['precessions']
	ax.plot(qs, precessions, marker=marker)



def make_figure_precession_versus_q():
	fig = plt.figure()
	ax1 = fig.add_subplot(1,1,1)
	filenames = ['data_to_plot_a02.h5', 'data_to_plot_a04.h5', 'data_to_plot_a08.h5', 'data_to_plot_a16.h5']
	markers = ['+','^','.','*']
	for filename, marker in zip(filenames, markers):
		plot_precession_versus_q(ax1,filename, marker)
	ax1.set_xlabel('Planet Mass (M_J)')
	ax1.set_ylabel('Precession Rate (Orbits/Rev)')
	#plt.axvline(x=50,color='r')
	return fig



def plot_eccentricity_versus_q(ax1, ax2, filename, marker):
	qs      = h5py.File(filename, 'r')['qs']
	e1s     = h5py.File(filename, 'r')['e1s']
	e2s     = h5py.File(filename, 'r')['e2s']
	e1mins  = h5py.File(filename, 'r')['e1mins']
	e2mins  = h5py.File(filename, 'r')['e2mins']
	e1maxs  = h5py.File(filename, 'r')['e1maxs']
	e2maxs  = h5py.File(filename, 'r')['e2maxs'] 
	ax1.plot(qs, e1s, marker = marker, markersize=8, color= 'black', linestyle='None',linewidth=0.5, mfc='None', label=filename[-6:-3])
	ax2.plot(qs, e2s, marker = marker, markersize=8, color= 'black', linestyle='None',linewidth=0.5, mfc='None', label=filename[-6:-3])
	ax1.fill_between(qs, e1mins, e1maxs, alpha=0.4)
	ax2.fill_between(qs, e2mins, e2maxs, alpha=0.4)



# def plot_max_eccentricity_versus_q(ax1, ax2, filename, marker):
# 	qs      = h5py.File(filename, 'r')['qs']
# 	max_e_kd06 = h5py.File(filename, 'r')['max_e_kd06']
# 	max_e_mm08 = h5py.File(filename, 'r')['max_e_mm08']
# 	max_e_mm08_mins = h5py.File(filename, 'r')['max_e_mm08_mins']
# 	max_e_kd06_mins = h5py.File(filename, 'r')['max_e_kd06_mins']
# 	max_e_kd06_maxs = h5py.File(filename, 'r')['max_e_kd06_maxs']
# 	max_e_mm08_maxs = h5py.File(filename, 'r')['max_e_mm08_maxs']
# 	ax1.plot(qs, max_e_mm08, marker = marker, markersize=8, color= 'black', linestyle='None',linewidth=0.5, mfc='None', label=filename[-6:-3])
# 	ax2.plot(qs, max_e_kd06, marker = marker, markersize=8, color= 'black', linestyle='None',linewidth=0.5, mfc='None', label=filename[-6:-3])
# 	ax1.fill_between(qs, max_e_mm08_mins, max_e_mm08_maxs, alpha=0.4)
# 	ax2.fill_between(qs, max_e_kd06_mins, max_e_kd06_maxs, alpha=0.4)


# def make_figure_max_eccentricity_versus_q():
# 	fig = plt.figure(figsize=[6.97,5.0])
# 	ax1 = fig.add_subplot(1, 2, 1)
# 	ax2 = fig.add_subplot(1, 2, 2)
# 	filenames = ['data_to_plot_a02.h5', 'data_to_plot_a04.h5', 'data_to_plot_a08.h5', 'data_to_plot_a16.h5']
# 	markers = ['+','^','.','*']
# 	for filename, marker in zip(filenames,markers):
# 		plot_max_eccentricity_versus_q(ax1, ax2, filename, marker)
	
# 	ax1.set_xlabel(r'Planet Mass $[M_J]$')
# 	ax2.set_xlabel(r'Planet Mass $[M_J]$')
# 	ax1.set_ylabel('Eccentricity measure')
# 	ax1.set_title('MM08')
# 	ax2.set_title('KD06')
# 	ax1.set_ylim(1e-3, 1.0)
# 	ax2.set_ylim(1e-3, 1.0)
# 	ax1.set_xscale('log')
# 	ax2.set_xscale('log')
# 	ax1.set_yscale('log')
# 	ax2.set_yscale('log')
# 	ax1.legend()
# 	ax2.legend()
# 	return fig


def make_figure_eccentricity_versus_q():
	fig = plt.figure(figsize=[6.97,5.0])
	ax1 = fig.add_subplot(1, 2, 1)
	ax2 = fig.add_subplot(1, 2, 2)
	#filenames = ['data_to_plot_sc.h5']
	filenames = ['data_to_plot_a02.h5', 'data_to_plot_a04.h5', 'data_to_plot_a08.h5', 'data_to_plot_a16.h5']
	markers = ['+','^','.','*']
	#markers = ['.']

	
	for filename, marker in zip(filenames,markers):
		plot_eccentricity_versus_q(ax1, ax2, filename, marker)
	

	ax1.set_xlabel(r'Planet Mass $[M_J]$')
	ax2.set_xlabel(r'Planet Mass $[M_J]$')
	ax1.set_ylabel('Eccentricity measure')
	ax1.set_title('MM08')
	ax2.set_title('KD06')
	ax1.set_ylim(1e-3, 1.0)
	ax2.set_ylim(1e-3, 1.0)
	ax1.set_xscale('log')
	ax2.set_xscale('log')
	ax1.set_yscale('log')
	ax2.set_yscale('log')
	ax1.legend()
	ax2.legend()
	return fig




def configure_matplotlib(hardcopy=False):
	plt.rc('xtick', labelsize=8)
	plt.rc('ytick', labelsize=8)
	plt.rc('axes', labelsize=8)
	plt.rc('legend', fontsize=8)
	plt.rc('font', family='Times New Roman' if hardcopy else 'DejaVu Sans', size=8)
	plt.rc('text', usetex=hardcopy)




if __name__ == "__main__":
	from argparse import ArgumentParser, RawTextHelpFormatter
	figure_funcs = dict([(k[12:], v)  for k, v in locals().items() if k.startswith('make_figure')])
	parser = ArgumentParser(formatter_class=RawTextHelpFormatter, epilog='\n'.join(['all'] + list(figure_funcs.keys())))
	parser.add_argument('figures', nargs='+', metavar='figure', choices=['all'] + list(figure_funcs.keys()))
	parser.add_argument('--hardcopy', action='store_true')
	parser.add_argument('--open', action='store_true')
	args = parser.parse_args()
	configure_matplotlib(args.hardcopy)
	figure_list = figure_funcs.keys() if args.figures == ['all'] else args.figures
	for figure in figure_list:
		fig = figure_funcs[figure]()
		if args.hardcopy:
			pdf_name = f'figures/{figure}.pdf'
			print(f'saving {pdf_name}')
			fig.savefig(f'{pdf_name}')
			if args.open:
				os.system(f'open {pdf_name}')
	if not args.hardcopy:
		plt.show()
