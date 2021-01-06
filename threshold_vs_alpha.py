#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

###########################################
### SCRIPT FOR GENERATING A PAPER FIGURE 
### RELATING THE THRESHOLD MASS TO THE
### ALPHA (VISCOSITY) VALUE 
###
###########################################


## First Plot : Q vs. Alpha, for all measurements
## Second Plot : E ampl. vs. Alpha, with a curve for each measurements, different markers for each paper

###########################################
###########################################
# Threshold Mass Ratio vs. Alpha
###########################################


def configure_matplotlib(hardcopy=False):
    import matplotlib.pyplot as plt
    plt.rc('xtick', labelsize=11)
    plt.rc('ytick', labelsize=11)
    plt.rc('axes', labelsize=11)
    plt.rc('legend', fontsize=11)
    plt.rc('font', family='Times New Roman' if hardcopy else 'DejaVu Sans', size=11)
    plt.rc('text', usetex=hardcopy)
    plt.rc('figure', titlesize=11)



configure_matplotlib(hardcopy=True)

x  = [0.02,0.04,0.08,0.1,0.16]  #Alpha values
y1 = [0.02,0.03,0.055,0.075,0.115] # Our resulting Q thresholds
y2 = [0.072,0.08,0.128,0.14,0.143] # Corresponding Eccentricity amplitudes


x_kd06  = [0.02,0.04,0.08,0.16]  #Alpha values
y1_kd06 = [0.02,0.03,0.06,0.11] # Our resulting Q thresholds
y2_kd06 = [0.132,0.155,0.291,0.326] # Corresponding Eccentricity amplitudes




fig = plt.figure(1, figsize=[3.32088,3.32088])
#fig = plt.figure(1, figsize=[6.97385,5])


#Farris 2014
plt.plot(0.1,0.1, marker='.')
plt.text(0.05,0.11,'Farris 14', fontsize=9.)

# #D'Orazio 18
# plt.plot(0.00001,0.04, marker='.')
# plt.text(0.000008,0.042, "D'Orazio 18")

plt.plot(x,y1, marker='.',label='RVM')
plt.xscale('log')
plt.xlabel('Alpha')
plt.ylabel('Threshold Mass Ratio')
plt.yscale('log')



#Kley-Dirksen result
plt.plot(0.004,0.003, marker='.')
plt.text(0.0031,0.0023,'Kley 06',fontsize=9.)

#Teyssandier 2017
plt.plot(0.005,0.0035, marker='.')
plt.text(0.0041,0.0039, 'Teyssandier 17',fontsize=9.)


#Ragusa 2020
# plt.plot(0.005,0.05, marker='*')
# plt.text(0.0045, 0.06, 'Ragusa 20', fontsize=9.)

#Ragusa 2017
# plt.plot(0.001,0.013, marker='*')
# plt.text(0.001,0.015, 'Ragusa 17', fontsize=9.)

#Dunhill 2012
# plt.plot(0.01,0.02, marker='*')
# plt.text(0.009,0.022, 'Dunhill 12', fontsize=9.)

#Papaloizou 2001
# plt.errorbar(0.004,0.015,0.005, marker='*')
# plt.text(0.0034, 0.022, 'Papaloizou 01',fontsize=9.)

#Bitsch 2013
plt.plot(0.005,0.005, marker='.')
plt.text(0.0044,0.0053, 'Bitsch 13', fontsize=9.)


#Muley 2019
plt.errorbar(0.001,0.003,0.001, marker='.')
plt.text(0.0008,0.0042, 'Muley 19', fontsize=9.)

plt.plot(x_kd06,y1_kd06, marker='.', label='AMD')
plt.legend(loc='lower right',fontsize=9.)
plt.subplots_adjust(bottom=0.14, right=0.95, top=0.97, left=0.2)
#plt.tight_layout()

########################################
#### E Amplitude vs. Alpha #############
########################################


fig2 = plt.figure(2, figsize=[3.32088,3.32088])


plt.plot(x,y2, marker='.', label='RVM',mfc='None', color='black')
plt.plot(x_kd06, y2_kd06, marker='+', label='AMD',mfc='None', color='blue')
plt.xscale('log')
plt.xlabel('Alpha')
plt.ylabel('Eccentricity')
plt.yscale('log')
plt.legend(fontsize=9.)


# #D'Orazio 18
# plt.plot(0.00001, 0.03, marker='.')
# plt.text(0.000008, 0.032, "D'Orazio 18")

#Farris 2014
plt.plot(0.1,0.11, marker='.', color='black')
plt.text(0.08,0.10,'Farris 14', fontsize=9.)

#Teyssandier 2017
plt.plot(0.005,0.1, marker='+', color='blue')
plt.text(0.0041,0.108, 'Teyssandier 17', fontsize=9.)

#Ragusa 2020
plt.plot(0.005,0.07, marker='+',  color='blue')
plt.text(0.0043, 0.075, 'Ragusa 20', fontsize=9.)

#Kley-Dirksen Result
plt.plot(0.004,0.15, marker='+',  color='blue')
plt.text(0.0035,0.16,'Kley 06', fontsize=9.)

plt.subplots_adjust(bottom=0.14, right=0.95, top=0.97, left=0.25)
#plt.tight_layout()
plt.show()
