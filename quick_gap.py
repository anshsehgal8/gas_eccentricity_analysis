#!/usr/bin/env python3

import argparse
import numpy as np
import scipy.optimize
import h5py
import matplotlib.pyplot as plt
import loaders


def get_gap_depth_vs_q(filename,bins,radial_cut):
    r       = loaders.get_dataset(filename, 'radius')
    dA      = loaders.get_dataset(filename, 'cell_area')
    sigma   = loaders.get_dataset(filename, 'sigma')
    phi     = loaders.get_dataset(filename, 'phi')
    vr      = loaders.get_dataset(filename, 'radial_velocity')
    vp      = loaders.get_dataset(filename, 'phi_velocity')
    r0, r1  = radial_cut
    dM      = dA * sigma
    domain_radius   = h5py.File(filename, 'r')['run_config']['domain_radius'][()]
    mass_ratio      = h5py.File(filename, 'r')['run_config']['mass_ratio'][()]
    planet_position = h5py.File(filename, 'r')['position_of_mass2'][()]
    x_planet = planet_position[0]
    y_planet = planet_position[1]
    rbins = np.linspace(0.0, domain_radius, bins)

    if x_planet > 0:
        phi_cut = (phi > (np.pi / 2.0)) * (phi < (-0.5 * np.pi))
    elif x_planet < 0: 
        phi_cut = (phi < (np.pi / 2.0)) * (phi > (-0.5 * np.pi))


    dM_binned,   _  = np.histogram(r, weights=dM * phi_cut , bins=rbins)
    dA_binned,   _  = np.histogram(r, weights=dA * phi_cut , bins=rbins)
    sigma_vs_r      = dM_binned / dA_binned
    gap_measurement = sigma_vs_r[0:22].min()  #sigma_vs_r[0:22].max() 
    return gap_measurement,mass_ratio



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs='+')
    parser.add_argument("--radial-cut", "-r", type=str, default="1.5,5.0", help="Pair of floats [AU] indicating the radial annulus to include")
    parser.add_argument("--bins", "-b", type=int, default=256, help="Number of bins to use in the line profile histogram")
    args = parser.parse_args()

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    qs = []
    gap_depth = []
    for filename in args.filenames:
        gap_measurement, mass_ratio = get_gap_depth_vs_q(filename, args.bins, eval(args.radial_cut))
        qs.append(mass_ratio)
        gap_depth.append(gap_measurement)

    ax1.plot(qs,gap_depth, marker = '.')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_ylabel(r'$\Delta\Sigma$')
    ax1.set_xlabel('Mass Ratio')
    plt.show()




