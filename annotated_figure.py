#!/usr/bin/env python3

import argparse
import numpy as np
import h5py
import matplotlib.pyplot as plt

filename = 'data/q_suite_v2_diagnostics/q0700-a02-b64.diagnostics.0256.h5'


def configure_matplotlib(hardcopy=False):
    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=8)
    plt.rc('axes', labelsize=8)
    plt.rc('legend', fontsize=8)
    plt.rc('font', family='Times New Roman' if hardcopy else 'DejaVu Sans', size=8)
    plt.rc('text', usetex=hardcopy)




def get_ranges():
    """
    @brief      Return the vmin and vmax keywords for fields.
    
    @param      args  The arguments (argparse result)
    
    @return     The vmin/vmax values
    """
    return dict(
        sigma_range=[ -7.9,-4.1])




def plot_single_block(ax, h5_verts, h5_values, edges=False, **kwargs):
    X = h5_verts[...][:,:,0]
    Y = h5_verts[...][:,:,1]
    Z = h5_values[...]

    if edges:
        Xb = X[::X.shape[0]//2, ::X.shape[1]//2]
        Yb = Y[::Y.shape[0]//2, ::Y.shape[1]//2]
        Zb = np.zeros_like(Xb + Yb)
        ax.pcolormesh(Xb, Yb, Zb, edgecolor=(1.0, 0.0, 1.0, 0.3))

    cm = ax.pcolormesh(X, Y, Z, **kwargs)
    cm.set_rasterized(True)
    return cm




def plot_single_file_sigma_only(
    fig,
    filename,
    depth=0,
    edges=False,
    sigma_range=[None, None],
    vr_range=[None, None],
    vp_range=[None, None]):

    ax, cax = fig.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [19, 1]})
    h5f = h5py.File(filename, 'r')

    for block_index in h5f['vertices']:

        if int(block_index[0]) < depth:
            continue

        verts = h5f['vertices'][block_index]
        ls = np.log10(h5f['sigma'][block_index])
        m0 = plot_single_block(ax, verts, ls, edges=edges, cmap='inferno', vmin=sigma_range[0], vmax=sigma_range[1])

    fig.colorbar(m0, cax=cax, orientation='horizontal')
    #x1,y1,x2,y2 = plot_annulus()

    ax.set_title(r'$\log_{10} \Sigma$')
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.add_artist(manual_fit)
    ax.add_artist(inner_edge)
    ax.add_artist(outer_edge)

    n, radii = 100, [1.5, 3.0]
    theta = np.linspace(0, 2*np.pi, n)
    xs = np.outer(radii, np.cos(theta))
    ys = np.outer(radii, np.sin(theta))

    # in order to have a closed area, the circles
    # should be traversed in opposite directions
    xs[1,:] = xs[1,::-1]
    ys[1,:] = ys[1,::-1]
    ax.fill(np.ravel(xs), np.ravel(ys), color='aqua', alpha=0.3, edgecolor='None')

    # inner = 1.5
    # outer = 3.

    # x = np.linspace(-outer, outer, 1000, endpoint=True)

    # yO = outer*np.sin(np.arccos(x/outer)) # x-axis values -> outer circle
    # yI = inner*np.sin(np.arccos(x/inner)) # x-axis values -> inner circle (with nan's beyond circle)
    # yI[np.isnan(yI)] = 0.                 # yI now looks like a boulder hat, meeting yO at the outer points
    # ax.fill_between(x, yI, yO, alpha=0.3, color='red')
    # ax.fill_between(x, -yO, -yI, alpha=0.3, color='red')
    #ax.fill(x1,y1,'None',x2, y2, 'green')
    #ax.fill_between(x2, y1, y2 ,alpha=0.2)
    ax.text(-1.3,-0.5,'Planet',     color='white', fontsize=6)
    ax.text(1.28,1.5, 'Annulus',     color='black', fontsize=6)
    ax.text(1.1,-3.3, 'Manual Fit', color='black', fontsize=6)
    ax.set_xlim(-4,4)
    ax.set_ylim(-4,4)

    return fig




def raise_figure_windows(plot_fn, figsize=[3.32, 3.5]):
    #print(filename)
    fig = plt.figure(figsize=figsize)
    plot_fn(fig, filename, **get_ranges())
    #fig.suptitle(filename)
    plt.subplots_adjust(left=0.057,bottom=0.08,right=0.97,top=0.92,wspace=0.2,hspace=0.2)
    plt.show()




# def plot_annulus():
#     theta = np.linspace(0, 2 * np.pi, 100)
#     r1 = 1.5
#     x1 = r1 * np.cos(theta)
#     y1 = r1 * np.sin(theta)
#     r2 = 3.0
#     x2 = r2 * np.cos(theta)
#     y2 = r2 * np.sin(theta)
#     return x1,y1,x2,y2
    



if __name__ == "__main__":
    configure_matplotlib(hardcopy=True)
    # parser = argparse.ArgumentParser()
    # parser.add_argument("filenames", nargs='+')
    # parser.add_argument("--sigma", default="default", type=str)
    # parser.add_argument("--depth", default=0, type=int)
    # parser.add_argument("--edges", action='store_true')
    # args = parser.parse_args()
    manual_fit = plt.Circle((-0.86,-0.86),2.8, color='white', fc='None')
    inner_edge = plt.Circle((0,0),1.5, color='aqua', fc='None', linestyle='--')
    outer_edge = plt.Circle((0,0),3.0, color='aqua', fc='None', linestyle='--')
    #plot_annulus()


    raise_figure_windows(plot_single_file_sigma_only)

