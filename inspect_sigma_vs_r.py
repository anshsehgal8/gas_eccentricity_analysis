#!/usr/bin/env python3


###########################################################
#
# This script generates Sigma vs. R plots at a glance, 
# given a diagnostic file as input.
#
###########################################################



import argparse
import numpy as np
import scipy.optimize
import h5py
import matplotlib.pyplot as plt
import loaders
from matplotlib import cm



def plot_sigma_profile(ax, filename, bins, radial_cut, color):
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
    r       = loaders.get_dataset(filename, 'radius')
    dA      = loaders.get_dataset(filename, 'cell_area')
    sigma   = loaders.get_dataset(filename, 'sigma')
    phi     = loaders.get_dataset(filename, 'phi')
    r0, r1  = radial_cut
    dM      = dA * sigma
    domain_radius   = h5py.File(filename, 'r')['run_config']['domain_radius'][()]
    planet_position = h5py.File(filename, 'r')['position_of_mass2'][()]
    rbins = np.linspace(0.0, domain_radius, bins)
    x_planet = planet_position[0]
    y_planet = planet_position[1]


    if x_planet > 0:
        phi_cut = (phi > (np.pi / 2.0)) * (phi < (-0.5 * np.pi))
    elif x_planet < 0: 
        phi_cut = (phi < (np.pi / 2.0)) * (phi > (-0.5 * np.pi))


    dM_binned,   _  = np.histogram(r, weights=dM * phi_cut, bins=rbins)
    dA_binned,   _  = np.histogram(r, weights=dA * phi_cut, bins=rbins)
    sigma_vs_r      = dM_binned / dA_binned
    gap_measurement = sigma_vs_r[0:150].min()


    ax1.plot(rbins[1:], sigma_vs_r, label=filename[22:25],color=color)
    ax1.set_xlabel(r'$v \rm{[km/s]}$')
    ax1.set_ylabel('Flux [Arb.]')
    ax1.set_yscale('log')
    ax1.set_xscale('log')






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs='+')
    parser.add_argument("--radial-cut", "-r", type=str, default="1.5,5.0", help="Pair of floats [AU] indicating the radial annulus to include")
    parser.add_argument("--bins", "-b", type=int, default=256, help="Number of bins to use in the line profile histogram")
    args = parser.parse_args()

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    numFiles = len(args.filenames)
    cm_subsection = np.linspace(0.0,1.0,numFiles)
    colors = [ cm.cool(x) for x in cm_subsection ]
    for filename, color in zip(args.filenames,colors):
        plot_sigma_profile(ax1, filename, args.bins, eval(args.radial_cut), color)
    #plt.legend()
    plt.show()





