#!/usr/bin/env python3

import os
import glob
import numpy as np
import h5py
import matplotlib.pyplot as plt




def get_eccentricity_time_series_mm08(rundir, include_factor_of_two=True):
    """
    Gets the time series of: time, eccentricity magnitude, and the eccentricity
    phase angle from a directory of HDF5 results
    
    :param      rundir:  The runid as a string
    :type       rundir:  str
    
    :returns:   Three time series: the time, e's, and w's (the phases)
    :rtype:     A tuple
    """
    filenames = sorted(glob.glob(os.path.join(rundir, 'eccentricity_measures.????.h5')))
    t = np.array([h5py.File(f, 'r')['time']             [...] for f in filenames])
    e = np.array([h5py.File(f, 'r')['mm08_e_global']    [...] for f in filenames]) * (2.0 if include_factor_of_two else 1.0)
    w = np.array([h5py.File(f, 'r')['mm08_phase_global'][...] for f in filenames])
    return t, e, w




def get_eccentricity_time_series_kd06(rundir):
    """
    Gets the time series of: time, eccentricity magnitude from a directory of
    HDF5 results
    
    :param      rundir:  The runid as a string
    :type       rundir:  str
    
    :returns:   Three time series: the time, e's, and w's (the phases)
    :rtype:     A tuple
    """
    filenames = sorted(glob.glob(os.path.join(rundir, 'eccentricity_measures.????.h5')))
    t = np.array([h5py.File(f, 'r')['time']             [...] for f in filenames])
    e = np.array([h5py.File(f, 'r')['kd06_e_global']    [...] for f in filenames])
    return t, e




def make_figure_eccentricity_time_series():
    rundirs = [f for f in sorted(glob.glob('data/q_suite_v1_reduced/q????-sc-b64'))]
    colors = [plt.cm.viridis(n / len(rundirs)) for n in range(len(rundirs))]

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    for rundir, color in zip(rundirs, colors):
        runid = rundir.split('/')[-1]

        t, e, w = get_eccentricity_time_series_mm08(rundir)
        ax1.plot(t / 2 / np.pi, e, label=runid, c=color)
        ax1.text(t[-1] / 2 / np.pi, e[-1], runid)

        t, e = get_eccentricity_time_series_kd06(rundir)
        ax2.plot(t / 2 / np.pi, e, label=runid, c=color)
        ax2.text(t[-1] / 2 / np.pi, e[-1], runid)

    ax1.set_yscale('log')
    ax2.set_yscale('log')
    ax1.set_ylim(1e-5, 1.0)
    ax2.set_ylim(1e-5, 1.0)
    ax1.set_xlabel('Orbits')
    ax2.set_xlabel('Orbits')
    ax1.set_title('MM08')
    ax2.set_title('KD06')
    ax1.set_ylabel('Eccentricity measure')
    return fig




def make_figure_eccentricity_versus_q():
    def get_mean_es(rundir):
        runid = rundir.split('/')[-1]
        q = int(runid[1:5]) / 10
        t1, e1, w1 = get_eccentricity_time_series_mm08(rundir)
        t2, e2     = get_eccentricity_time_series_kd06(rundir)
        i1 = np.where(t1 / 2 / np.pi > 500)
        i2 = np.where(t2 / 2 / np.pi > 500)
        if len(i1[0]) > 30:
            e1_mean = e1[i1].mean()
            e2_mean = e2[i2].mean()
            return q, e1_mean, e2_mean
        else:
            print(f'warning: {rundir} was not fully evolved')
            return None

    rundirs = [f for f in sorted(glob.glob('data/q_suite_v1_reduced/q????-sc-b64'))]
    es  = [x for x in [get_mean_es(rundir) for rundir in rundirs] if x]
    qs  = [e[0] for e in es]
    e1s = [e[1] for e in es]
    e2s = [e[2] for e in es]
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    ax1.plot(qs, e1s, '-o', mfc='none')
    ax2.plot(qs, e2s, '-o', mfc='none')
    ax1.set_xlabel(r'Mass ratio $[M_J]$')
    ax2.set_xlabel(r'Mass ratio $[M_J]$')
    ax1.set_ylabel('Eccentricity measure')
    ax1.set_title('MM08')
    ax2.set_title('KD06')
    ax1.set_ylim(1e-5, 1.0)
    ax2.set_ylim(1e-5, 1.0)
    ax1.set_xscale('log')
    ax2.set_xscale('log')
    ax1.set_yscale('log')
    ax2.set_yscale('log')
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
