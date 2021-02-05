import numpy as np
import matplotlib.pyplot as plt
import h5py
import argparse



def get_dataset(filename, key):
	h5f = h5py.File(filename, 'r')
	domain_radius = h5f['model']['domain_radius'][()]
	block_size    = h5f['model']['block_size'][()]
	num_blocks    = h5f['model']['num_blocks'][()]
	blocks        = np.array(h5f['state']['solution'])

	
	x_array     = []
	y_array     = []
	vx_array    = []
	vy_array    = []
	sigma_array = []
	area_array  = []


	for block in blocks:
		sigma = h5f['state']['solution'][block]['conserved']['0']
		sigma_vx = h5f['state']['solution'][block]['conserved']['1']
		sigma_vy = h5f['state']['solution'][block]['conserved']['2']
		vx = sigma_vx / sigma
		vy = sigma_vy / sigma 
		n = block_size
		block_width = 2 * domain_radius / num_blocks
		block_index_x = int(block[2:5])
		block_index_y = int(block[6:])
		x_0 = -domain_radius + (block_width * block_index_x)
		x_1 = x_0 + block_width
		y_0 = -domain_radius + (block_width * block_index_y)
		y_1 = y_0 + block_width
		x_vertices = np.linspace(x_0 , x_1, n+1)
		y_vertices = np.linspace(y_0 , y_1, n+1)
		dx = np.diff(x_vertices)
		dy = np.diff(y_vertices)
		dx_m, dy_m = np.meshgrid(dx,dy)
		area = dx_m * dy_m
		x_center = 0.5 * (x_vertices[1:] +  x_vertices[:-1])
		y_center = 0.5 * (y_vertices[1:] +  y_vertices[:-1])
		xc, yc = np.meshgrid(x_center,y_center)
		x_array.append(xc)
		y_array.append(yc)
		vx_array.append(vx)
		vy_array.append(vy)
		sigma_array.append(sigma)
		area_array.append(area)


	x_array     = np.array(x_array)
	y_array     = np.array(y_array)
	vx_array    = np.array(vx_array)
	vy_array    = np.array(vy_array)
	sigma_array = np.array(sigma_array)
	area_array  = np.array(area_array)

	r      = np.sqrt(x_array**2 + y_array**2)
	vr     = ((x_array * vx_array )+ (y_array * vy_array)) / r
	vp     = ((x_array * vy_array) - (vx_array * y_array)) / r

	if key =='sigma':
		return sigma_array

	if key == 'radius':
		return r

	if key == 'phi':
		return np.arctan2(y_array, x_array)

	if key == 'cell_area':
		return area_array

	if key == 'mass':
		return get_dataset(filename, 'sigma') * get_dataset(filename, 'cell_area')

	if key == 'x_velocity':
		return vx_array

	if key == 'y_velocity':
		return vy_array
	
	if key == 'radial_velocity':
		return vr

	if key == 'phi_velocity':
		return vp


	raise KeyError('unknown dataset: ' + key)

