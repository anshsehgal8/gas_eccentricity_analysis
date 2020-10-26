#!/usr/bin/env python3
import argparse
import numpy as np
import h5py
import scipy.interpolate
import scipy.optimize
import matplotlib.pyplot as plt
import loaders
#import cv2
filename = 'data/q_suite_v2_diagnostics/q0050-a08-b64.diagnostics.0177.h5'

def x_theta(xcm,ycm,a,b,omega,n):
	theta = np.linspace(0, 2 * np.pi, n)
	x = xcm + (a * np.cos(omega) * np.cos(theta)) - (b * np.sin(omega) * np.sin(theta))
	y = ycm + (a * np.sin(omega) * np.cos(theta)) + (b * np.cos(omega) * np.sin(theta))
	return x,y




def load_data():
	h5f = h5py.File(filename, 'r')
	domain_radius = np.array(h5f['run_config']['domain_radius'])
	block_size    = np.array(h5f['run_config']['block_size'])
	depth         = np.array(h5f['run_config']['depth'])
	real_depth = depth - 3
	step  = (2 * domain_radius)/(2**real_depth * block_size)
	vertices = h5f['vertices'].values()
	helpers = loaders.HelperFunctions()
	xc = np.array([helpers.cell_center_x_array(g[...]) for g in vertices])
	yc = np.array([helpers.cell_center_y_array(g[...]) for g in vertices])
	mass = loaders.get_dataset(filename, 'mass')
	nbins = 32
	bins = np.linspace(-nbins * step ,nbins * step,(2 * nbins) + 1)

	masses, xedges, yedges = np.histogram2d(xc.flatten(),yc.flatten(),weights=mass.flatten(),bins=bins)
	#plt.imshow(masses)

	return masses, xedges, yedges

	

def calc_sigma(xcm,ycm,a,b,omega,n):
	masses, xedges, yedges = load_data(filename)
	x,y = x_theta(xcm,ycm,a,b,omega,n)
	interp_function = scipy.interpolate.interp2d(xedges[1:],yedges[1:],masses)
	sigma = interp_function(x,y)
	#counts, bin_number = np.histogram(sigma,bins=100)
	#plt.step(bin_number[:-1],counts)
	return sigma.std()




if __name__ == '__main__':
	# parser = argparse.ArgumentParser()
	# parser.add_argument("filename")
	# args = parser.parse_args()
	x0 = [0.,0.,1.,1.,0.,100]
	residual  = scipy.optimize.least_squares(calc_sigma,x0)


# image = cv2.imread('figures/q0600-a08.png')
# window_name = 'Image'
# cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
# center_coordinates = (1045,961)
# axesLength = (419,385)
# a = min(axesLength[0],axesLength[1])
# b = max(axesLength[0],axesLength[1])
# e = np.sqrt(1. - (a / b)**2 )
# print(e)
# angle = 0
# startAngle = 0
# endAngle = 360
# color = (0,0,255)
# thickness = 5

# image = cv2.ellipse(image,center_coordinates,axesLength,angle,startAngle,endAngle,color,thickness)
# cv2.imshow(window_name,image)
# cv2.waitKey()