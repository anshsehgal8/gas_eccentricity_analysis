#!/usr/bin/env python3
import argparse
import numpy as np
import h5py
import scipy.interpolate
import scipy.optimize
import matplotlib.pyplot as plt
import loaders

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
		#print(np.log10(np.mean((sigma - sigma.max())**2)))
		return np.log10(np.mean((sigma - sigma.max())**2)) #+ abs(a - 2.5) + abs(b - 2.5)
		#return np.log(sigma).std() / np.log(sigma).mean() #+ abs(a - 2.5) + abs(b - 2.5) #+ abs(xcm + 0.2) + abs(ycm + 0.6)

	return lambda x: result(*x)





if __name__ == '__main__':
	# parser = argparse.ArgumentParser()
	# parser.add_argument("filename")
	# args = parser.parse_args()
	x0 = [0.,0.,2.2,2.2,0.]
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
