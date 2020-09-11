#!/usr/bin/env python3

import argparse
import numpy as np
import scipy.optimize
import h5py
import matplotlib.pyplot as plt
import loaders



def plot_e_vs_r(filename,ax):
	e_vs_r = np.array(h5py.File(filename, 'r')['mm08_e_vs_r'])
	r = np.linspace(0, 24, len(e_vs_r))
	ax.plot(r, e_vs_r)
	ax.set_xscale('log')
	ax.set_yscale('log')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    plot_e_vs_r(args.filename,ax1)
    plt.show()

