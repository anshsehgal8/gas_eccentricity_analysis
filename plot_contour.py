#!/usr/bin/env python3
import argparse
import numpy as np
import h5py
import scipy.interpolate
import scipy.optimize
import matplotlib.pyplot as plt
import loaders
#import cv2
filename = 'data/q_suite_v2_diagnostics/q0600-a08-b64.diagnostics.0178.h5'

def x_theta(xcm,ycm,a,b,omega):
	theta = np.linspace(0, 2 * np.pi, 100)
	x = xcm + (a * np.cos(omega) * np.cos(theta)) - (b * np.sin(omega) * np.sin(theta))
	y = ycm + (a * np.sin(omega) * np.cos(theta)) + (b * np.cos(omega) * np.sin(theta))
	return x,y




def load_data():
	h5f = h5py.File(filename, 'r')
	domain_radius = np.array(h5f['run_config']['domain_radius'])
	block_size    = np.array(h5f['run_config']['block_size'])
	depth         = np.array(h5f['run_config']['depth'])
	real_depth = depth - 4
	step  = (2 * domain_radius)/(2**real_depth * block_size)
	vertices = h5f['vertices'].values()
	helpers = loaders.HelperFunctions()
	xc = np.array([helpers.cell_center_x_array(g[...]) for g in vertices])
	yc = np.array([helpers.cell_center_y_array(g[...]) for g in vertices])
	mass = loaders.get_dataset(filename, 'mass')
	nbins = 16
	bins = np.linspace(-nbins * step ,nbins * step,(2 * nbins) + 1)

	masses, xedges, yedges = np.histogram2d(xc.flatten(),yc.flatten(),weights=mass.flatten(),bins=bins)
	#plt.imshow(masses)

	return masses, xedges, yedges

	

def calc_sigma():
	masses, xedges, yedges = load_data()
	x_center = 0.5 * (xedges[1:] +  xedges[:-1])
	y_center = 0.5 * (yedges[1:] +  yedges[:-1])
	interp_function = scipy.interpolate.interp2d(x_center,y_center,masses)

	def result(xcm,ycm,a,b,omega):
		x,y = x_theta(xcm,ycm,a,b,omega)
		interp_function = scipy.interpolate.interp2d(x_center,y_center,masses)
		sigma = interp_function(x,y)
		print(a,b)
		#counts, bin_number = np.histogram(sigma,bins=100)
		#plt.step(bin_number[:-1],counts)
		return np.log(sigma).std() / np.log(sigma).mean() #+ abs(a - 2.5) + abs(b - 2.5) #+ abs(xcm + 0.2) + abs(ycm + 0.6)

	return lambda x: result(*x)





if __name__ == '__main__':
	# parser = argparse.ArgumentParser()
	# parser.add_argument("filename")
	# args = parser.parse_args()
	x0 = [0.,0.,1.,1.,0.]
	#print(calc_sigma(*x0))
	residual  = scipy.optimize.minimize(calc_sigma(),x0)
	masses, xedges, yedges = load_data()
	#x , y = x_theta(*x0)
	plt.imshow(masses, extent=[xedges[0],xedges[-1],yedges[0],yedges[-1]])
	plt.colorbar()
	#plt.plot(*x_theta(*x0))
	plt.plot(*x_theta(*residual.x))
	a  = max(residual.x[2], residual.x[3])
	b  = min(residual.x[2], residual.x[3])
	frac = abs(b**2/a**2)
	e = np.sqrt(1 - frac)
	print(residual.x)
	print(e)
	plt.show()


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