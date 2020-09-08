#!/usr/bin/env python3

import argparse
import numpy as np
import scipy.optimize
import h5py
import matplotlib.pyplot as plt
import loaders

km_per_sec = 4.74 * 2 * np.pi # For a planet orbiting at 1 AU




def plot_line_profile(ax, filename, line_of_sight, bins, radial_cut):
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
    rc = loaders.get_dataset(filename, 'radius')
    rc = loaders.get_dataset(filename, 'radius')
    vx = loaders.get_dataset(filename, 'x_velocity')
    vy = loaders.get_dataset(filename, 'y_velocity')
    r0, r1 = radial_cut
    los_phi = line_of_sight * np.pi / 180.0
    los_vel = (np.cos(los_phi) * vx + np.sin(los_phi) * vy) * km_per_sec

    line_amplitude, los_velocity_bins = np.histogram(los_vel[(rc > r0) * (rc < r1)].flatten(), bins=bins, density=True)
    ax1.step(los_velocity_bins[1:], line_amplitude)
    ax1.set_xlabel(r'$v \rm{[km/s]}$')
    ax1.set_ylabel('Flux [Arb.]')

    def double_gaussian(x, x0, x1, y0, y1, s0, s1):
        return y0 * np.exp(-(x - x0)**2 / 2 / s0**2) + y1 * np.exp(-(x - x1)**2 / 2 / s1**2)

    popt, pcov = scipy.optimize.curve_fit(double_gaussian, los_velocity_bins[1:], line_amplitude, (-20.0, 20.0, 0.1, 0.1, 1.0, 1.0))
    v = np.linspace(los_velocity_bins[0], los_velocity_bins[-1], 10000)

    ax1.plot(v, double_gaussian(v, *popt))
    ax1.axvline(0.0, c='grey', lw=0.5, color='grey')




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--line-of-sight", "-l", type=float, default=0.0, help="Azimuthal line-of-sight angle in degrees")
    parser.add_argument("--radial-cut", "-r", type=str, default="1.5,5.0", help="Pair of floats [AU] indicating the radial annulus to include")
    parser.add_argument("--bins", "-b", type=int, default=200, help="Number ofbins to use in the line profile histogram")
    args = parser.parse_args()

    fig = plt.figure(figsize=[10, 10])
    ax1 = fig.add_subplot(1, 1, 1)
    plot_line_profile(ax1, args.filename, args.line_of_sight, args.bins, eval(args.radial_cut))
    plt.show()
