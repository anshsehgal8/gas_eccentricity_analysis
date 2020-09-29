import numpy as np
import matplotlib.pyplot as plt

x  = [0.02,0.04,0.08,0.1,0.16]
y1 = [0.02,0.03,0.055,0.07,0.11]
y2 = [0.046,0.052,0.128,0.14,0.143]


fig = plt.figure()
ax1 = plt.subplot(2,1,1)
ax1.plot(0.004,0.003, marker='.', label='KD06')
ax1.plot(x,y1, marker='.')
ax1.set_xscale('log')
ax1.set_xlabel('Alpha')
ax1.set_ylabel('Threshold Mass Ratio')
ax1.set_yscale('log')
ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2.plot(0.004,0.15, marker='.', label = 'KD06')
ax2.plot(x,y2, marker='.')
ax2.set_xscale('log')
ax2.set_xlabel('Alpha')
ax2.set_ylabel('Eccentricity')
ax2.set_yscale('log')

plt.show()
