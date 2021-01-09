#!/usr/bin/env python3
import argparse
import numpy as np
import h5py
import matplotlib.pyplot as plt

text_width = 6.97385


def configure_matplotlib(hardcopy=False):
    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=8)
    plt.rc('axes', labelsize=8)
    plt.rc('legend', fontsize=8)
    plt.rc('font', family='Times New Roman' if hardcopy else 'DejaVu Sans', size=8)
    plt.rc('text', usetex=hardcopy)



def plot_sigma(ax, filename):
    h5f = h5py.File(filename, 'r')

    for block_index in h5f['vertices']:
        X = h5f['vertices'][block_index][...][:,:,0]
        Y = h5f['vertices'][block_index][...][:,:,1]
        S = h5f['sigma'][block_index]
        cm = ax.pcolormesh(X, Y, np.log10(S), vmin=-7.9, vmax=-4.1, cmap='inferno')
        cm.set_rasterized(True)
    return cm


def main():
    fig = plt.figure(figsize=[text_width, text_width * 0.4])
    gs  = fig.add_gridspec(nrows=2, ncols=4, height_ratios=[28, 2])
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    ax4 = fig.add_subplot(gs[0, 3])
    cax = fig.add_subplot(gs[1, :])
    axes = [ax1, ax2, ax3, ax4]

    filenames = [
        'data/q_suite_v2_diagnostics/q0050-a02-b64.diagnostics.0273.h5',
        'data/q_suite_v2_diagnostics/q0300-a02-b64.diagnostics.0254.h5',
        'data/q_suite_v2_diagnostics/q0700-a02-b64.diagnostics.0256.h5',
        'data/q_suite_v2_diagnostics/q1200-a02-b64.diagnostics.0257.h5']

    for ax, filename in zip(axes, filenames):
        print(filename)
        cm = plot_sigma(ax, filename)
        ax.set_aspect('equal')
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.colorbar(cm, cax, orientation='horizontal')

    for ax in axes:
        ax.set_xlabel(r'$x$')

    ax1.set_title(r'$5 M_J$')
    ax2.set_title(r'$30 M_J$')
    ax3.set_title(r'$70 M_J$')
    ax4.set_title(r'$120 M_J$')
    ax1.set_ylabel(r'$y$')

    fig.subplots_adjust(left=0.03, right=0.998, top=0.93, wspace=0.01)
    plt.show()


if __name__ == "__main__":
    configure_matplotlib(hardcopy=True)
    main()

