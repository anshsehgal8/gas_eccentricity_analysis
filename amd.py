#!usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt


def configure_matplotlib(hardcopy=False):
    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=8)
    plt.rc('axes', labelsize=8)
    plt.rc('legend', fontsize=8)
    plt.rc('font', family='Times New Roman' if hardcopy else 'DejaVu Sans', size=8)
    plt.rc('text', usetex=hardcopy)

configure_matplotlib(hardcopy=True)


m = np.linspace(10,50,50)

n0 = 0
#n1 = 1
n2 = 2
#n3 = 3
n4 = 4

denominator0 = (2 / (1 - (n0 + 1)/m**2) - 1)**2
#denominator1 = (2 / (1 - (n1 + 1)/m**2) - 1)**2
denominator2 = (2 / (1 - (n2 + 1)/m**2) - 1)**2
#denominator3 = (2 / (1 - (n3 + 1)/m**2) - 1)**2
denominator4 = (2 / (1 - (n4 + 1)/m**2) - 1)**2

e0 = np.sqrt(1 - 1 / denominator0)
#e1 = np.sqrt(1 - 1 / denominator1)
e2 = np.sqrt(1 - 1 / denominator2)
#e3 = np.sqrt(1 - 1 / denominator3)
e4 = np.sqrt(1 - 1 / denominator4)

approx_e_0 = 2 * np.sqrt(n0 + 1) / m
#approx_e_1 = 2 * np.sqrt(n1 + 1) / m
approx_e_2 = 2 * np.sqrt(n2 + 1) / m
#approx_e_3 = 2 * np.sqrt(n3 + 1) / m
approx_e_4 = 2 * np.sqrt(n4 + 1) / m

fig = plt.figure(figsize=[3.32,3.32])
ax1  = fig.add_subplot(1,1,1)
ax1.plot(m,e0, linewidth=0.5, label= 'n = 0', color='blue')
#ax1.plot(m,e1, linewidth=0.5, label= 'n = 1', color='green')
ax1.plot(m,e2, linewidth=0.5, label= 'n = 2', color='green')
#ax1.plot(m,e3, linewidth=0.5, label= 'n = 3', color='red')
ax1.plot(m,e4, linewidth=0.5, label= 'n = 4', color='red')
ax1.plot(m,approx_e_0,  linewidth=0.5, linestyle = '--', color='blue')
#ax1.plot(m,approx_e_1,  linewidth=0.5, linestyle = '--', color='green')
ax1.plot(m,approx_e_2,  linewidth=0.5, linestyle = '--', color='green')
#ax1.plot(m,approx_e_3,  linewidth=0.5, linestyle = '--', color='red')
ax1.plot(m,approx_e_4,  linewidth=0.5, linestyle = '--', color='red')
ax1.fill_between(m, e0, approx_e_0, alpha=0.2, color='blue')
#ax1.fill_between(m, e1, approx_e_1, alpha=0.2, color='green')
ax1.fill_between(m, e2, approx_e_2, alpha=0.2, color='green')
#ax1.fill_between(m, e3, approx_e_3, alpha=0.2, color='red')
ax1.fill_between(m, e4, approx_e_4, alpha=0.2, color='red')
plt.axvline(20, linestyle='--', color='black')
ax1.legend()
ax1.set_xlabel('Mach Number')
ax1.set_ylabel('AMD Eccentricity')
plt.subplots_adjust(left=0.146,bottom=0.11,right=0.97,top=0.97)
plt.show()