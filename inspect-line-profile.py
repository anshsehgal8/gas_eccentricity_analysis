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




def configure_matplotlib(hardcopy=False):
    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=8)
    plt.rc('axes', labelsize=8)
    plt.rc('legend', fontsize=8)
    plt.rc('font', family='Times New Roman' if hardcopy else 'DejaVu Sans', size=8)
    plt.rc('text', usetex=hardcopy)




def plot_line_profile(ax, filename, line_of_sight, bins, radial_cut, noise, label):
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
    np.random.seed(1)
    gaussian_noise = np.random.normal(loc=0,size=vx.shape,scale=noise)
    los_vel = ((np.cos(los_phi) * vx + np.sin(los_phi) * vy) * km_per_sec) + gaussian_noise

    line_amplitude, los_velocity_bins = np.histogram(los_vel.flatten(), bins=bins, density=True, weights= (dA * (rc > r0) * (rc < r1)).flatten())
    ax.step(los_velocity_bins[1:], line_amplitude, color='black')
    

    asymmetry = abs(np.max(line_amplitude[0:100]) - np.max(line_amplitude[100:]))
    print("Asymmetry : ", asymmetry)

    ax.fill_between(los_velocity_bins[1:],line_amplitude,0,alpha=0.3,color='black')
    #ax.legend(loc='upper left')
    ax.text(-50,0.022, label)


    # def double_gaussian(x, x0, x1, y0, y1, s0, s1):
    #     return y0 * np.exp(-(x - x0)**2 / 2 / s0**2) + y1 * np.exp(-(x - x1)**2 / 2 / s1**2)

    # popt, pcov = scipy.optimize.curve_fit(double_gaussian, los_velocity_bins[1:], line_amplitude, (-20.0, 20.0, 0.1, 0.1, 1.0, 1.0))
    # v = np.linspace(los_velocity_bins[0], los_velocity_bins[-1], 10000)

    # ax1.plot(v, double_gaussian(v, *popt))
    ax.axvline(0.0, c='grey', lw=0.5, color='grey')




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("filenames", nargs='+')
    parser.add_argument("--line-of-sight", "-l", type=float, default=0.0, help="Azimuthal line-of-sight angle in degrees")
    parser.add_argument("--radial-cut", "-r", type=str, default="1.5,3.0", help="Pair of floats [AU] indicating the radial annulus to include")
    parser.add_argument("--bins", "-b", type=int, default=200, help="Number of bins to use in the line profile histogram")
    parser.add_argument("--noise", "-n", type=int, default=4, help="Amount of Gaussian noise to be used in line profile")
    args = parser.parse_args()
    filenames = ['data/q_suite_v2_diagnostics/q0050-a02-b64.diagnostics.0273.h5', 'data/q_suite_v2_diagnostics/q0600-a02-b64.diagnostics.0256.h5', 'data/q_suite_v2_diagnostics/q1200-a02-b64.diagnostics.0257.h5' ]

    fig = plt.figure(figsize=[3.32088, 3.32088])
    configure_matplotlib(hardcopy=True)
    ax1 = fig.add_subplot(3, 1, 1)
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax2 = fig.add_subplot(3, 1, 2, sharex=ax1 ) #xticks=([]))
    plt.setp(ax2.get_xticklabels(), visible=False)
    ax3 = fig.add_subplot(3, 1, 3, sharex=ax1 ) #xticks=([]))
    ax2.set_ylabel('Flux [Arb.]')
    ax3.set_xlabel(r'$v \rm{[km/s]}$')
    plot_line_profile(ax1, filenames[0], 15., args.bins, eval(args.radial_cut), args.noise, 'q = 0.005')
    plot_line_profile(ax2, filenames[1], 30., args.bins, eval(args.radial_cut), args.noise, 'q = 0.06')
    plot_line_profile(ax3, filenames[2], 280., args.bins, eval(args.radial_cut), args.noise,'q = 0.12')
    plt.subplots_adjust(left=0.165,bottom=0.13,right=0.96,top=0.98)
    ax1.set_xlim(-60,60)
    plt.show()
