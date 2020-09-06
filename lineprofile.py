#!/usr/bin/env python3




import argparse
import numpy as np
import h5py
import matplotlib.pyplot as plt
import loaders


def configure_matplotlib(hardcopy=False):
    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=8)
    plt.rc('axes', labelsize=8)
    plt.rc('legend', fontsize=8)
    plt.rc('font', family='Times New Roman' if hardcopy else 'DejaVu Sans', size=8)
    plt.rc('text', usetex=hardcopy)




if __name__ == "__main__":


    configure_matplotlib(hardcopy=True)

    plt.figure(figsize=[3.0,5.0])
    file1 = '/Users/anshsehgal/Mara3/128_5J/diagnostics.0100.h5'
    file2 = '/Users/anshsehgal/Mara3/128_10J/diagnostics.0100.h5'
    file3 = '/Users/anshsehgal/Mara3/128_50J/diagnostics.0100.h5'
    file4 = '/Users/anshsehgal/Mara3/128_100J/diagnostics.0100.h5'




    domain_radius_1 = h5py.File(file1, 'r')['run_config']['domain_radius'][()]
    domain_radius_2 = h5py.File(file2, 'r')['run_config']['domain_radius'][()]
    domain_radius_3 = h5py.File(file3, 'r')['run_config']['domain_radius'][()]
    domain_radius_4 = h5py.File(file4, 'r')['run_config']['domain_radius'][()]
    time_1          = h5py.File(file1, 'r')['time'][()]
    time_2          = h5py.File(file2, 'r')['time'][()]
    time_3          = h5py.File(file3, 'r')['time'][()]
    time_4          = h5py.File(file4, 'r')['time'][()]
    mass_ratio_1    = h5py.File(file1, 'r')['run_config']['mass_ratio'][()]
    mass_ratio_2    = h5py.File(file2, 'r')['run_config']['mass_ratio'][()]
    mass_ratio_3    = h5py.File(file3, 'r')['run_config']['mass_ratio'][()]
    mass_ratio_4    = h5py.File(file4, 'r')['run_config']['mass_ratio'][()]
    run_1           = mass_ratio_1 * 1000
    run_2           = mass_ratio_2 * 1000
    run_3           = mass_ratio_3 * 1000
    run_4           = mass_ratio_4 * 1000

    r_1     = loaders.get_dataset(file1, 'radius')
    r_2     = loaders.get_dataset(file2, 'radius')
    r_3     = loaders.get_dataset(file3, 'radius')
    r_4     = loaders.get_dataset(file4, 'radius')
    phi_1   = loaders.get_dataset(file1, 'phi')
    phi_2   = loaders.get_dataset(file2, 'phi')
    phi_3   = loaders.get_dataset(file3, 'phi')
    phi_4   = loaders.get_dataset(file4, 'phi')
    dA_1    = loaders.get_dataset(file1, 'cell_area')
    dA_2    = loaders.get_dataset(file2, 'cell_area')
    dA_3    = loaders.get_dataset(file3, 'cell_area')
    dA_4    = loaders.get_dataset(file4, 'cell_area')
    vr_1    = loaders.get_dataset(file1, 'radial_velocity')
    vr_2    = loaders.get_dataset(file2, 'radial_velocity')
    vr_3    = loaders.get_dataset(file3, 'radial_velocity')
    vr_4    = loaders.get_dataset(file4, 'radial_velocity')
    vp_1    = loaders.get_dataset(file1, 'phi_velocity')
    vp_2    = loaders.get_dataset(file2, 'phi_velocity')
    vp_3    = loaders.get_dataset(file3, 'phi_velocity')
    vp_4    = loaders.get_dataset(file4, 'phi_velocity')
    vx_1    = loaders.get_dataset(file1, 'x_velocity') * 4.74 * (2*np.pi) #km/s conversion
    vx_2    = loaders.get_dataset(file2, 'x_velocity') * 4.74 * (2*np.pi) #km/s conversion
    vx_3    = loaders.get_dataset(file3, 'x_velocity') * 4.74 * (2*np.pi) #km/s conversion
    vx_4    = loaders.get_dataset(file4, 'x_velocity') * 4.74 * (2*np.pi) #km/s conversion
    vy_1    = loaders.get_dataset(file1, 'y_velocity') * 4.74 * (2*np.pi) #km/s conversion
    vy_2    = loaders.get_dataset(file2, 'y_velocity') * 4.74 * (2*np.pi) #km/s conversion
    vy_3    = loaders.get_dataset(file3, 'y_velocity') * 4.74 * (2*np.pi) #km/s conversion
    vy_4    = loaders.get_dataset(file4, 'y_velocity') * 4.74 * (2*np.pi) #km/s conversion
    sigma_1 = loaders.get_dataset(file1, 'sigma')
    sigma_2 = loaders.get_dataset(file2, 'sigma')
    sigma_3 = loaders.get_dataset(file3, 'sigma')
    sigma_4 = loaders.get_dataset(file4, 'sigma')


    radial_cut_1 = (r_1 > 1.5) * (r_1 < 5.0)
    radial_cut_2 = (r_2 > 1.5) * (r_2 < 5.0)
    radial_cut_3 = (r_3 > 1.5) * (r_3 < 5.0)
    radial_cut_4 = (r_4 > 1.5) * (r_4 < 5.0)



    def get_LOS_1_diff(a1):

        LOS_1   = vx_1 * np.cos(a1) + vy_1 * np.sin(a1) 

        count1, bins1 = np.histogram(LOS_1,weights=dA_1 * (r_1 < 3) * (r_1 > 2),density=True,bins=100)
        maxcount1    = np.where((count1[1:-1] > count1[0:-2]) * (count1[1:-1] > count1[2:]))
        i0,  i1     = np.argsort(count1[tuple(i+1 for i in maxcount1)])[-2:]
        j0,  j1     = maxcount1[0][i0], maxcount1[0][i1]
        if j0 > j1:
            j0, j1 = j1, j0
        diff1   = count1[j1] - count1[j0]
        return diff1


    def get_LOS_2_diff(a2):

        LOS_2   = vx_2 * np.cos(a2) + vy_2 * np.sin(a2)

        count2, bins2 = np.histogram(LOS_2,weights=dA_2 * (r_2 < 3) * (r_2 > 2),density=True,bins=100)
        maxcount2    = np.where((count2[1:-1] > count2[0:-2]) * (count2[1:-1] > count2[2:]))
        i0,  i1     = np.argsort(count2[tuple(i+1 for i in maxcount2)])[-2:]
        j0,  j1     = maxcount2[0][i0], maxcount2[0][i1]
        if j0 > j1:
            j0, j1 = j1, j0
        diff2   = count2[j1] - count2[j0]
        return diff2



    def get_LOS_3_diff(a3):

        LOS_3   = vx_3 * np.cos(a3) + vy_3 * np.sin(a3)

        count3, bins3 = np.histogram(LOS_3,weights=dA_3 * (r_3 < 3) * (r_3 > 2),density=True,bins=100)
        maxcount3    = np.where((count3[1:-1] > count3[0:-2]) * (count3[1:-1] > count3[2:]))
        i0,  i1     = np.argsort(count3[tuple(i+1 for i in maxcount3)])[-2:]
        j0,  j1     = maxcount3[0][i0], maxcount3[0][i1]
        if j0 > j1:
            j0, j1 = j1, j0
        diff3   = count3[j1] - count3[j0]
        return diff3

    
    def get_LOS_4_diff(a4):

        LOS_4   = vx_4 * np.cos(a4) + vy_4 * np.sin(a4)

        count4, bins4 = np.histogram(LOS_4,weights=dA_4 * (r_4 < 3) * (r_4 > 2),density=True,bins=100)
        maxcount4    = np.where((count4[1:-1] > count4[0:-2]) * (count4[1:-1] > count4[2:]))
        i0,  i1     = np.argsort(count4[tuple(i+1 for i in maxcount4)])[-2:]
        j0,  j1     = maxcount4[0][i0], maxcount4[0][i1]
        if j0 > j1:
            j0, j1 = j1, j0
        diff4  = count4[j1] - count4[j0]
        return diff4



    angles = np.linspace(0.01,2*np.pi,100)
    total1 = [get_LOS_1_diff(angle) for angle in angles]
    total2 = [get_LOS_2_diff(angle) for angle in angles]
    total3 = [get_LOS_3_diff(angle) for angle in angles]
    total4 = [get_LOS_4_diff(angle) for angle in angles] 


    optimalangleindex1 = total1.index(max(total1))
    optimalangleindex2 = total2.index(max(total2))
    optimalangleindex3 = total3.index(max(total3))
    optimalangleindex4 = total4.index(max(total4))

    angle1 = angles[optimalangleindex1]
    angle2 = angles[optimalangleindex2]
    angle3 = angles[optimalangleindex3]
    angle4 = angles[optimalangleindex4]
    print(angle1)
    print(angle2)
    print(angle3)
    print(angle4)

    LOS_1   = vx_1 * np.cos(angle1) + vy_1 * np.sin(angle1) + np.random.normal(loc=0,size=vx_1.shape,scale=4)
    LOS_2   = vx_2 * np.cos(angle2) + vy_2 * np.sin(angle2) + np.random.normal(loc=0,size=vx_2.shape,scale=4)
    LOS_3   = vx_3 * np.cos(angle3) + vy_3 * np.sin(angle3) + np.random.normal(loc=0,size=vx_3.shape,scale=4)
    LOS_4   = vx_4 * np.cos(angle4) + vy_4 * np.sin(angle4) + np.random.normal(loc=0,size=vx_4.shape,scale=4)



    
    #ax = plt.subplot(1,1,1)
    ax1 = plt.subplot(4,1,1)

    count1, bins1 = np.histogram(LOS_1,weights=dA_1 * 1.4 * (r_1 < 3) * (r_1 > 2),density=False,bins=100)
    count2, bins2 = np.histogram(LOS_2,weights=dA_2 * 1.4 * (r_2 < 3) * (r_2 > 2),density=False,bins=100)
    count3, bins3 = np.histogram(LOS_3,weights=dA_3 * 1.4 * (r_3 < 3) * (r_3 > 2),density=False,bins=100)
    count4, bins4 = np.histogram(LOS_4,weights=dA_4 * 1.4 * (r_4 < 3) * (r_4 > 2),density=False,bins=100)

    

    plt.hist(
        LOS_1.flat,
        weights=(dA_1 * 1.4 * (r_1 < 3) * (r_1 > 2)).flat,
        bins=100,
        density=False,
        histtype='step',
        label=r'$\rm{:n} M_J$'.format(run_1),
        color='black')
        #label=r'$\rm{{orbit}} = {:.01f}$'.format(time / 2 / np.pi))


    ax1.fill_between(bins1[1:],count1,0,alpha=0.3,color='black')

    
    plt.text(-50,0.5,r'5 $M_J$')
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.xlim(-60,60)
    plt.ylim(0,1.33)
    #plt.yscale('log')
    #plt.legend(loc='upper left')

    ax2 = plt.subplot(4,1,2,sharex=ax1)
    

    plt.hist(
        LOS_2.flat,
        weights=(dA_2 * 1.4 *  (r_2 < 3) * (r_2 > 2)).flat,
        bins=100,
        density=False,
        histtype='step',
        label=r'$\rm{:n} M_J$'.format(run_2),
        color='black')
        #label=r'$\rm{{orbit}} = {:.01f}$'.format(time / 2 / np.pi))

    ax2.fill_between(bins2[1:],count2,0,alpha=0.3,color='black')

    plt.text(-50,0.5,r'10 $M_J$')
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.xlim(-60,60)
    plt.ylim(0,1.33)
    #plt.yscale('log')
    #plt.legend(loc='upper left')

    ax3 = plt.subplot(4,1,3,sharex=ax1)

    plt.hist(
        LOS_3.flat,
        weights=(dA_3 * 1.4 * (r_3 < 3) * (r_3 > 2)).flat,
        bins=100,
        density=False,
        histtype='step',
        label=r'$\rm{:n} M_J$'.format(run_3),
        color='black')
        #label=r'$\rm{{orbit}} = {:.01f}$'.format(time / 2 / np.pi))

    
    ax3.fill_between(bins3[1:],count3,0,alpha=0.3,color='black')
    plt.text(-50,0.5,r'50 $M_J$')
    plt.setp(ax3.get_xticklabels(), visible=False)
    plt.xlim(-60,60)
    plt.ylim(0,1.33)
    #plt.yscale('log')
    #plt.legend(loc='upper left')


    ax4 = plt.subplot(4,1,4,sharex=ax1)
    

    plt.hist(
        LOS_4.flat,
        weights=(dA_4 * 1.4 * (r_4 < 3) * (r_4 > 2)).flat,
        bins=100,
        density=False,
        histtype='step',
        label=r'$\rm{:n} M_J$'.format(run_4),
        color='black')
        #label=r'$\rm{{orbit}} = {:.01f}$'.format(time / 2 / np.pi))

    ax4.fill_between(bins4[1:],count4,0,alpha=0.3,color='black')
    plt.text(-50,0.5,r'100 $M_J$')
    plt.xlim(-60,60)
    #plt.yscale('log')
    #plt.legend(loc='upper left')
    plt.xlabel(r'$V_{\rm LOS} \, [{\rm km/s}]$')
    #plt.ylabel('Flux[arb.]')
    plt.ylim(0,1.33)


    plt.figtext(0,0.5,'Flux[arb.]',rotation='vertical')

    plt.tight_layout()
    plt.show()
