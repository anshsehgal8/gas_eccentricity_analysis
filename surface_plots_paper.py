#!/usr/bin/env python3
import argparse
import numpy as np
import h5py
import matplotlib.pyplot as plt

text_width = 6.97385


def configure_matplotlib(hardcopy=False):
    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=8)
    plt.rc('axes', labelsize=8)
    plt.rc('legend', fontsize=8)
    plt.rc('font', family='Times New Roman' if hardcopy else 'DejaVu Sans', size=8)
    plt.rc('text', usetex=hardcopy)



def plot_sigma(ax, filename):
    h5f = h5py.File(filename, 'r')

    for block_index in h5f['vertices']:
        X = h5f['vertices'][block_index][...][:,:,0]
        Y = h5f['vertices'][block_index][...][:,:,1]
        S = h5f['sigma'][block_index]
        cm = ax.pcolormesh(X, Y, np.log10(S), vmin=-7.9, vmax=-4.1, cmap='inferno')
    return cm


def main():
    fig = plt.figure(figsize=[text_width, text_width * 0.4])
    gs  = fig.add_gridspec(nrows=2, ncols=4, height_ratios=[28, 2])
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    ax4 = fig.add_subplot(gs[0, 3])
    cax = fig.add_subplot(gs[1, :])
    axes = [ax1, ax2, ax3, ax4]

    filenames = [
        'data/q_suite_v2_diagnostics/q0050-a02-b64.diagnostics.0273.h5',
        'data/q_suite_v2_diagnostics/q0300-a02-b64.diagnostics.0254.h5',
        'data/q_suite_v2_diagnostics/q0700-a02-b64.diagnostics.0256.h5',
        'data/q_suite_v2_diagnostics/q1200-a02-b64.diagnostics.0257.h5']

    for ax, filename in zip(axes, filenames):
        print(filename)
        cm = plot_sigma(ax, filename)
        ax.set_aspect('equal')
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.colorbar(cm, cax, orientation='horizontal')

    for ax in axes:
        ax.set_xlabel(r'$x$')

    ax1.set_title(r'$5 M_J$')
    ax2.set_title(r'$30 M_J$')
    ax3.set_title(r'$70 M_J$')
    ax4.set_title(r'$120 M_J$')
    ax1.set_ylabel(r'$y$')

    fig.subplots_adjust(left=0.03, right=0.998, top=0.93, wspace=0.01)
    plt.show()


if __name__ == "__main__":
    configure_matplotlib(hardcopy=True)
    main()

# import argparse
# import numpy as np
# import h5py
# import matplotlib.pyplot as plt




# def get_ranges(args):
#     """
#     @brief      Return the vmin and vmax keywords for fields.
    
#     @param      args  The arguments (argparse result)
    
#     @return     The vmin/vmax values
#     """
#     return dict(
#         sigma_range=eval(args.sigma, dict(default=[ -8,-4])),
#         vr_range   =eval(args.vr,    dict(default=[ -0.5, 0.5])),
#         vp_range   =eval(args.vp,    dict(default=[  0.0, 2.0])))




# def plot_single_block(ax, h5_verts, h5_values, edges=False, **kwargs):
#     X = h5_verts[...][:,:,0]
#     Y = h5_verts[...][:,:,1]
#     Z = h5_values[...]

#     if edges:
#         Xb = X[::X.shape[0]//2, ::X.shape[1]//2]
#         Yb = Y[::Y.shape[0]//2, ::Y.shape[1]//2]
#         Zb = np.zeros_like(Xb + Yb)
#         ax.pcolormesh(Xb, Yb, Zb, edgecolor=(1.0, 0.0, 1.0, 0.3))

#     return ax.pcolormesh(X, Y, Z, **kwargs)






# def plot_single_file_sigma_only(fig,filename,depth=0,edges=False,sigma_range=[None, None],vr_range=[None, None],vp_range=[None, None]):

#     ax, cax = fig.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [19, 1]})
#     h5f = h5py.File(filename, 'r')

#     for block_index in h5f['vertices']:

#         if int(block_index[0]) < depth:
#             continue

#         verts = h5f['vertices'][block_index]
#         ls = np.log10(h5f['sigma'][block_index])
#         m0 = plot_single_block(ax, verts, ls, edges=edges, cmap='inferno', vmin=sigma_range[0], vmax=sigma_range[1])

#     fig.colorbar(m0, cax=cax, orientation='horizontal')

#     ax.set_title(r'$\log_{10} \Sigma$')
#     ax.set_xlabel(r'$x$')
#     ax.set_ylabel(r'$y$')
#     ax.set_aspect('equal')
#     ax.set_xticks([])

#     return fig





# def raise_figure_windows_impl(args, plot_fn, figsize=[16, 6]):

#     fig = plt.figure(figsize=figsize)
#     ax1 = fig.add_subplot(1,4,1)
#     ax2 = fig.add_subplot(1,4,2)
#     ax3 = fig.add_subplot(1,4,3)
#     ax4 = fig.add_subplot(1,4,4)
#     for filename in args.filenames:
#         print(filename)
#         plot_fn(fig, filename, edges=args.edges, depth=args.depth, **get_ranges(args))
#         fig.suptitle(filename)
#     plt.show()




# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("filenames", nargs='+')
#     parser.add_argument("--window-size", type=int, default=1000)
#     parser.add_argument("--sigma", default="default", type=str)
#     parser.add_argument("--depth", default=0, type=int)
#     parser.add_argument("--edges", action='store_true')
#     parser.add_argument("--vr", default="default", type=str)
#     parser.add_argument("--vp", default="default", type=str)

#     args = parser.parse_args()

#     raise_figure_windows_impl(args, plot_single_file_sigma_only, figsize=[10, 10])
