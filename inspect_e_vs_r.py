#!/usr/bin/env python3

import argparse
import numpy as np
import scipy.optimize
import h5py
import matplotlib.pyplot as plt
import loaders
from matplotlib import cm



def plot_e_vs_r(filename,ax,color):
    e_vs_r = np.array(h5py.File(filename, 'r')['mm08_e_vs_r'])
    domain_radius = np.array(h5py.File(filename, 'r')['run_config']['domain_radius'])
    r = np.linspace(0, domain_radius, len(e_vs_r)) #Domain Radius of 24
    ax.plot(r, e_vs_r, label=filename[-37:-34], color=color)
    ax.set_xscale('log')
    ax.set_yscale('log')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames",nargs='+')
    args = parser.parse_args()
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    r = np.linspace(0, 24, 255)
    y = r**(-3.0)
    ax1.plot(r,y, label=r'$r^{-3}$ fit', color='r')
    numFiles = len(args.filenames)
    cm_subsection = np.linspace(0.0,1.0,numFiles)
    colors = [ cm.cool(x) for x in cm_subsection ]

    for filename,color in zip(args.filenames,colors):
        plot_e_vs_r(filename,ax1,color)
    
    ax1.legend()
    ax1.set_xlabel('Radius(AU)')
    ax1.set_ylabel('Eccentricity')
    plt.show()

