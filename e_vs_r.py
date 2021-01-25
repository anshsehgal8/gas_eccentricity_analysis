#!/usr/bin/env python3

import argparse
import numpy as np
import h5py
import matplotlib.pyplot as plt
import loaders
from matplotlib import cm


filepath = 'data/q_suite_v2/q0050-a02-b64/eccentricity_measures.'
filenames_kd06 = ['data/q_suite_v2/q0050-a02-b64/eccentricity_measures.0000.h5' , 'data/q_suite_v2/q0050-a02-b64/eccentricity_measures.0250.h5']
filenames_mm08 = ['data/q_suite_v2/q0050-a02-b64/eccentricity_measures.0250.h5']
  

def configure_matplotlib(hardcopy=False):
    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=8)
    plt.rc('axes', labelsize=8)
    plt.rc('legend', fontsize=8)
    plt.rc('font', family='Times New Roman' if hardcopy else 'DejaVu Sans', size=8)
    plt.rc('text', usetex=hardcopy)



def plot_e_vs_r_kd06(filename,ax,color):
    e_vs_r = np.array(h5py.File(filename, 'r')['kd06_e_vs_r'])
    domain_radius = np.array(h5py.File(filename, 'r')['run_config']['domain_radius'])
    r = np.linspace(0, domain_radius, len(e_vs_r))
    e_per_file  = np.mean(e_vs_r[15:30])
    ax.plot(r, e_vs_r, color=color)
    ax.set_xscale('log')
    ax.set_yscale('log')
    #ax.axvline(1.5)
    #ax.axvline(3)
    return e_per_file


def plot_e_vs_r_mm08(filename,ax,color):
    e_vs_r = np.array(h5py.File(filename, 'r')['mm08_e_vs_r'])
    domain_radius = np.array(h5py.File(filename, 'r')['run_config']['domain_radius'])
    r = np.linspace(0, domain_radius, len(e_vs_r))
    e_per_file  = np.mean(e_vs_r[15:30])
    ax.plot(r, e_vs_r, color=color)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.axvline(1.5, linestyle='--', color='black')
    ax.axvline(3, linestyle='--', color='black')
    return e_per_file


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("filenames", nargs='+')
    # args = parser.parse_args()
    configure_matplotlib(hardcopy=True)
    fig = plt.figure(figsize=[3.32088, 3.32088])
    ax1 = fig.add_subplot(1,1,1)

    #ax1.plot(r,y, label=r'$r^{-3}$ fit', color='r')
    numFiles = len(filenames_kd06)
    cm_subsection = np.linspace(0.0,1.0,numFiles)
    #colors = [ cm.cool(x) for x in cm_subsection ]
    colors_kd06 = ['blue', 'green']
    colors_mm08 = ['red']
    labels = ['AMD (0 orbits)', 'AMD (2500 orbits)', 'RVM (2500 orbits)',]
    es_kd06 = []
    es_mm08 = []

    for filename, color in zip(filenames_kd06, colors_kd06):

       es_kd06.append(plot_e_vs_r_kd06(filename,ax1, color))
    

    for filename, color in zip(filenames_mm08, colors_mm08):
        es_mm08.append(plot_e_vs_r_mm08(filename,ax1, color))
    
    e_global_kd06 = np.mean(es_kd06[-30:])
    print(e_global_kd06)
    ax1.set_xlabel('Radius(AU)')
    ax1.set_ylabel('Eccentricity')
    ax1.set_ylim(1E-5,0.3)
    plt.subplots_adjust(left=0.167,bottom=0.11,right=0.965,top=0.977)
    plt.legend(labels, fontsize=5)
    plt.show()

