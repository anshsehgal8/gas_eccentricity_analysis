#!/usr/bin/env python3
import argparse
import numpy as np
import h5py
import matplotlib.pyplot as plt




def get_ranges(args):
    """
    @brief      Return the vmin and vmax keywords for fields.
    
    @param      args  The arguments (argparse result)
    
    @return     The vmin/vmax values
    """
    return dict(
        sigma_range=eval(args.sigma, dict(default=[ -6.5,-4.5])),
        vr_range   =eval(args.vr,    dict(default=[ -0.5, 0.5])),
        vp_range   =eval(args.vp,    dict(default=[  0.0, 2.0])))




def plot_single_block(ax, h5_verts, h5_values, edges=False, **kwargs):
    X = h5_verts[...][:,:,0]
    Y = h5_verts[...][:,:,1]
    Z = h5_values[...]

    if edges:
        Xb = X[::X.shape[0]//2, ::X.shape[1]//2]
        Yb = Y[::Y.shape[0]//2, ::Y.shape[1]//2]
        Zb = np.zeros_like(Xb + Yb)
        ax.pcolormesh(Xb, Yb, Zb, edgecolor=(1.0, 0.0, 1.0, 0.3))

    return ax.pcolormesh(X, Y, Z, **kwargs)




def fit_func(x, y, a, b, phi):
    return (x / a)**2 + (y / b)**2



def plot_single_file_sigma_only(fig,filename,depth=0,edges=False,sigma_range=[None, None],vr_range=[None, None],vp_range=[None, None]):

    ax, cax = fig.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [19, 1]})
    h5f = h5py.File(filename, 'r')

    for block_index in h5f['vertices']:

        if int(block_index[0]) < depth:
            continue

        verts = h5f['vertices'][block_index]
        ls = np.log10(h5f['sigma'][block_index])
        m0 = plot_single_block(ax, verts, ls, edges=edges, cmap='inferno', vmin=sigma_range[0], vmax=sigma_range[1])
        #Z = fit_func(X,Y,a,b,phi)


    fig.colorbar(m0, cax=cax, orientation='horizontal')

    ax.set_title(r'$\log_{10} \Sigma$')
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    ax.set_aspect('equal')
    ax.set_xticks([])

    return fig




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs='+')
    parser.add_argument("--sigma", default="default", type=str)
    parser.add_argument("--depth", default=0, type=int)
    parser.add_argument("--edges", action='store_true')
    parser.add_argument("--vr", default="default", type=str)
    parser.add_argument("--vp", default="default", type=str)

    args = parser.parse_args()

    for filename in args.filenames:
        fig = plt.figure(figsize=[5,5])
        plot_single_file_sigma_only(fig, filename, edges=args.edges, depth=args.depth, **get_ranges(args))
        plt.show()


