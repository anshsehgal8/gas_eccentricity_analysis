#!/usr/bin/env python3
import argparse
import numpy as np
import h5py
import matplotlib.pyplot as plt
import loaders
import cv2

def load_data(filename):
	h5f = h5py.File(filename, 'r')
	domain_radius = np.array(h5f['run_config']['domain_radius'])
	block_size    = np.array(h5f['run_config']['block_size'])
	depth         = np.array(h5f['run_config']['depth'])
	real_depth = depth - 1
	step  = (2 * domain_radius)/(2**real_depth * block_size)
	vertices = h5f['vertices'].values()
	helpers = loaders.HelperFunctions()
	xc = np.array([helpers.cell_center_x_array(g[...]) for g in vertices])
	yc = np.array([helpers.cell_center_y_array(g[...]) for g in vertices])
	mass = loaders.get_dataset(filename, 'mass')
	bins = np.linspace(-96 * step ,96 * step,193)

	counts, xedges, yedges = np.histogram2d(xc.flatten(),yc.flatten(),weights=mass.flatten(),bins=bins)
	plt.imshow(counts)
	plt.show()



def fit_func(x,y,a,b,phi):
	return (x/a)**2 + (y/b)**2



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("filename")
	args = parser.parse_args()
	load_data(args.filename)

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