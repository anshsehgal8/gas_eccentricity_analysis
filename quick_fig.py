#!/usr/bin/env python3

###############################################################
# This script generates line profiles at a glance from a given 
# diagnostic files
#
#
#
###############################################################


import argparse
import numpy as np
import scipy.optimize
import h5py
import matplotlib.pyplot as plt
import loaders

km_per_sec = 4.74 * 2 * np.pi # For a planet orbiting at 1 AU



def plot_line_profile(ax, filename, line_of_sight, bins, radial_cut, noise, label,linestyle,linewidth):
    """
    Doc string to come soon...

    :param      ax:             { parameter_description }
    :type       ax:             { type_description }
    :param      filename:       The filename
    :type       filename:       { type_description }
    :param      line_of_sight:  The line of sight
    :type       line_of_sight:  { type_description }
    :param      bins:           The bins
    :type       bins:           { type_description }
    :param      radial_cut:     The radial cut
    :type       radial_cut:     { type_description }
    """
    rc   = loaders.get_dataset(filename, 'radius')
    vx   = loaders.get_dataset(filename, 'x_velocity')
    vy   = loaders.get_dataset(filename, 'y_velocity')
    dA   = loaders.get_dataset(filename, 'cell_area')
    r0, r1  = radial_cut
    los_phi = line_of_sight * np.pi / 180.0
    los_vel = ((np.cos(los_phi) * vx + np.sin(los_phi) * vy) * km_per_sec) + np.random.normal(loc=0,size=vx.shape,scale=noise)

    line_amplitude, los_velocity_bins = np.histogram(los_vel.flatten(), bins=bins, density=True, weights= (dA  * (rc > r0) * (rc < r1)).flatten())
    ax.step(los_velocity_bins[1:], line_amplitude * 31.7, label=label, linestyle=linestyle, linewidth=linewidth)
    ax.set_xlim(-50,50)
    ax.set_ylim(0,1.4)
    ax.set_ylabel('Flux [Arb.]')
    ax.legend(loc='upper left', prop={'size':5})

    # def double_gaussian(x, x0, x1, y0, y1, s0, s1):
    #     return y0 * np.exp(-(x - x0)**2 / 2 / s0**2) + y1 * np.exp(-(x - x1)**2 / 2 / s1**2)

    # popt, pcov = scipy.optimize.curve_fit(double_gaussian, los_velocity_bins[1:], line_amplitude, (-20.0, 20.0, 0.1, 0.1, 1.0, 1.0))
    # v = np.linspace(los_velocity_bins[0], los_velocity_bins[-1], 10000)

    # ax1.plot(v, double_gaussian(v, *popt))
    # ax1.axvline(0.0, c='grey', lw=0.5, color='grey')





def configure_matplotlib(hardcopy=False):
    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=8)
    plt.rc('axes', labelsize=8)
    plt.rc('legend', fontsize=8)
    plt.rc('font', family='Times New Roman' if hardcopy else 'DejaVu Sans', size=8)
    plt.rc('text', usetex=hardcopy)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("filename")
    parser.add_argument("--line-of-sight", "-l", type=float, default=0.0, help="Azimuthal line-of-sight angle in degrees")
    parser.add_argument("--radial-cut", "-r", type=str, default="1.5,5", help="Pair of floats [AU] indicating the radial annulus to include")
    parser.add_argument("--bins", "-b", type=int, default=100, help="Number of bins to use in the line profile histogram")
    parser.add_argument("--noise", "-n", type=int, default=4, help="Amount of Gaussian noise to be used in line profile")
    args = parser.parse_args()
    configure_matplotlib(hardcopy=True)

    filenames = ['data/q_suite_v2_diagnostics/q0050-a08-b64.diagnostics.0177.h5', 'data/q_suite_v2_diagnostics/q1600-a08-b64.diagnostics.0181.h5']


    fig = plt.figure(figsize=[3.5, 2])

    
    ax1 = fig.add_subplot(111)
    plot_line_profile(ax1, filenames[0], args.line_of_sight, args.bins, eval(args.radial_cut), args.noise,'Mass Ratio: 0.005 (circular disk)','--', 0.4)
    #plt.setp(ax1.get_xticklabels(), visible=False)
    #ax2 = fig.add_subplot(212)
    plot_line_profile(ax1, filenames[1], args.line_of_sight, args.bins, eval(args.radial_cut), args.noise,'Mass Ratio: 0.16 (eccentric disk)','-', 1.0)
    ax1.set_xlabel(r'$v \rm{[km/s]}$')
    plt.subplots_adjust(bottom=0.17, right=0.97, top=0.98, left=0.13)
    plt.show()
