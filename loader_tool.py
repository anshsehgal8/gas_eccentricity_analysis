#!/usr/bin/env python3

import os
import glob
import numpy as np
import h5py
import matplotlib.pyplot as plt


saturation_orbits = [2200, 1800, 1500, 1200]
alpha_keys  = ['a02', 'a04', 'a08', 'a16']


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
    t = np.array([h5py.File(f, 'r')['time']               [...] for f in filenames])
    e = np.array([h5py.File(f, 'r')['mm08_e_global']      [...] for f in filenames]) * (2.0 if include_factor_of_two else 1.0)
    w = np.array([h5py.File(f, 'r')['mm08_phase_global']  [...] for f in filenames])

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




# def get_max_eccentricity_time_series_mm08(rundir):
#     filenames   = sorted(glob.glob(os.path.join(rundir, 'eccentricity_measures.????.h5')))
#     t           = np.array([h5py.File(f, 'r')['time']             [...] for f in filenames])
#     max_e       = np.array([h5py.File(f, 'r')['mm08_e_vs_r']      [...] for f in filenames])
#     #print(max_e.shape)
#     return t[5:], max_e[5:]


# def get_max_eccentricity_time_series_kd06(rundir):
#     filenames   = sorted(glob.glob(os.path.join(rundir, 'eccentricity_measures.????.h5')))
#     t           = np.array([h5py.File(f, 'r')['time']             [...] for f in filenames])
#     max_e       = np.array([h5py.File(f, 'r')['kd06_e_vs_r']      [...] for f in filenames])
#     #print(max_e.shape)
#     return t[5:], max_e[5:]




def get_disk_phase_time_series(rundir):
    t, e, w = get_eccentricity_time_series_mm08(rundir)
    dphi = np.diff(w)
    dphi[dphi < -0.9 * 2 * np.pi] += 2 * np.pi
    dphi[dphi > +0.9 * 2 * np.pi] -= 2 * np.pi
    cumphase = np.cumsum(dphi)
    return cumphase




def calc_precession_versus_q(alpha_key, saturation_orbit):
    def get_mean_phase(rundir):
        runid = rundir.split('/')[-1]
        q = int(runid[1:5])/10
        cumphase = get_disk_phase_time_series(rundir)
        t, e , w = get_eccentricity_time_series_mm08(rundir)
        t = t[0:-1]
        i = np.where(t / 2 / np.pi > saturation_orbit)
        isat = int(saturation_orbit / 15)

        if len(i[0]) > 10:
            cumphase_mean = (cumphase[-1] - cumphase[isat]) / (t[-1] - t[isat])
            cumphase_mean = (cumphase_mean)**(-1.)
            return q, cumphase_mean
        else:
            print(f'warning: {runid} was not fully evolved')

    rundirs = [f for f in sorted(glob.glob(f'data/q_suite_v2/q????-{alpha_key}-b64'))]
    phases  = [x for x in [get_mean_phase(rundir) for rundir in rundirs] if x]
    qs  = [e[0] for e in phases]
    precessions = [e[1] for e in phases]
    return qs, precessions




def calc_eccentricity_versus_q(alpha_key, saturation_orbit):
    def get_mean_es(rundir):
        runid = rundir.split('/')[-1]
        q = int(runid[1:5]) / 10
        t1, e1, w  = get_eccentricity_time_series_mm08(rundir)
        t2, e2     = get_eccentricity_time_series_kd06(rundir)
        i1 = np.where(t1 / 2 / np.pi > saturation_orbit)
        i2 = np.where(t2 / 2 / np.pi > saturation_orbit)
        if len(i1[0]) > 10:
            e1_mean = e1[i1].mean()
            e2_mean = e2[i2].mean()
            e1_min  = e1[i1].min()
            e2_min  = e2[i2].min()
            e1_max  = e1[i1].max()
            e2_max  = e2[i2].max()
            return q, e1_mean, e2_mean, e1_min, e2_min, e1_max, e2_max
        else:
            print(f'warning: {runid} was not fully evolved')
            return None

    rundirs = [f for f in sorted(glob.glob(f'data/q_suite_v2/q????-{alpha_key}-b64'))]
    es      = [x for x in [get_mean_es(rundir) for rundir in rundirs] if x]
    qs      = [e[0] for e in es]
    e1s     = [e[1] for e in es]
    e2s     = [e[2] for e in es]
    e1mins  = [e[3] for e in es]
    e2mins  = [e[4] for e in es]
    e1maxs  = [e[5] for e in es]
    e2maxs  = [e[6] for e in es]

    return qs, e1s, e2s, e1mins, e2mins, e1maxs, e2maxs




def write_totals_versus_q():

    for alpha_key, saturation_orbit in zip(alpha_keys, saturation_orbits):
        qs, e1s, e2s, e1mins, e2mins, e1maxs, e2maxs = calc_eccentricity_versus_q(alpha_key, saturation_orbit)
        qs_prec, precessions = calc_precession_versus_q(alpha_key, saturation_orbit)

        h5f = h5py.File(f'data_to_plot_{alpha_key}.h5', 'w')
        h5f['qs']           = qs 
        h5f['e1s']          = e1s
        h5f['e2s']          = e2s
        h5f['e1mins']       = e1mins
        h5f['e2mins']       = e2mins
        h5f['e1maxs']       = e1maxs
        h5f['e2maxs']       = e2maxs
        h5f['qs_prec']      = qs_prec
        h5f['precessions']  = precessions





def write_time_series_data():

    rundirs = [f for f in sorted(glob.glob(f'data/q_suite_v2/q????-a??-b64'))]

    for rundir in rundirs:
        t_mm08, e_mm08, w = get_eccentricity_time_series_mm08(rundir)
        t_kd06, e_kd06    = get_eccentricity_time_series_kd06(rundir)
        cumphase          = get_disk_phase_time_series(rundir)
        h5f = h5py.File(f"{rundir}/time_series.h5", 'w')
        h5f['t_mm08']        = t_mm08
        h5f['t_kd06']        = t_kd06
        h5f['e_mm08']        = e_mm08
        h5f['e_kd06']        = e_kd06
        h5f['cumphase']      = cumphase


    

if __name__ == "__main__":

    write_totals_versus_q()
    write_time_series_data()

 




