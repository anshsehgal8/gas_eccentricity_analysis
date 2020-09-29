#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

###########################################
### SCRIPT FOR GENERATING A PAPER FIGURE 
### RELATING THE THRESHOLD MASS TO THE
### ALPHA (VISCOSITY) VALUE 
###
###########################################


###########################################
###########################################
# MM08 PLOT
###########################################

x  = [0.02,0.04,0.08,0.1,0.16]  #Alpha values
y1 = [0.02,0.03,0.055,0.075,0.115] # Our resulting Q thresholds
y2 = [0.046,0.052,0.128,0.14,0.143] # Corresponding Eccentricity amplitudes


fig = plt.figure(1)
ax1 = plt.subplot(2,1,1)



#Farris 2014
ax1.plot(0.1,0.1, marker='.')
ax1.text(0.09,0.11,'Farris 14')

#D'Orazio 18
ax1.plot(0.00001,0.04, marker='.')
ax1.text(0.000008,0.042, "D'Orazio 18")

ax1.plot(x,y1, marker='.')
ax1.set_xscale('log')
ax1.set_xlabel('Alpha')
ax1.set_ylabel('Threshold Mass Ratio')
ax1.set_yscale('log')

ax2 = plt.subplot(2,1,2, sharex=ax1)



#Farris 2014
ax2.plot(0.1,0.11, marker='.')
ax2.text(0.09,0.12,'Farris 14')

#D'Orazio 18
ax2.plot(0.00001, 0.03, marker='.')
ax2.text(0.000008, 0.032, "D'Orazio 18")

ax2.plot(x,y2, marker='.')
ax2.set_xscale('log')
ax2.set_xlabel('Alpha')
ax2.set_ylabel('Eccentricity')
ax2.set_yscale('log')


#################################
#################################
## KD06 PLOT
#################################

x_kd06  = [0.02,0.04,0.08,0.16]  #Alpha values
y1_kd06 = [0.02,0.03,0.06,0.11] # Our resulting Q thresholds
y2_kd06 = [0.055,0.066,0.148,0.166] # Corresponding Eccentricity amplitudes


fig2 = plt.figure(2)
ax3  = plt.subplot(2,1,1)

#Kley-Dirksen result
ax3.plot(0.004,0.003, marker='.')
ax3.text(0.0035,0.004,'KD06')

#Teyssandier 2017
ax3.plot(0.005,0.0035, marker='.')
ax3.text(0.0048,0.0037, 'Teyssandier 17')


#Ragusa 2020
ax3.plot(0.005,0.05, marker='.')
ax3.text(0.0048, 0.06, 'Ragusa 20')

ax3.plot(x_kd06,y1_kd06, marker='.')
ax3.set_xscale('log')
ax3.set_xlabel('Alpha')
ax3.set_ylabel('Threshold Mass Ratio')
ax3.set_yscale('log')

ax4  = plt.subplot(2,1,2)

#Teyssandier 2017
ax4.plot(0.005,0.1, marker='.')
ax4.text(0.0048,0.12, 'Teyssandier 17')

#Ragusa 2020
ax4.plot(0.005,0.07, marker='.')
ax4.text(0.0048, 0.08, 'Ragusa 20')

#Kley-Dirksen Result
ax4.plot(0.004,0.15, marker='.')
ax4.text(0.0035,0.16,'KD06')

ax4.plot(x_kd06, y2_kd06, marker='.')
ax4.set_xscale('log')
ax4.set_xlabel('Alpha')
ax4.set_ylabel('Eccentricity')
ax4.set_yscale('log')

plt.show()
