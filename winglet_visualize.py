import numpy as np
import matplotlib.pyplot as plt

colors = ["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"]
linestyles = ['-', '--', '-.', ':']

def plot_lift_all(set_zrot, set_solids, zrot_solids_dict):
    """4 subplots with Fz """

    fig = plt.figure()
    subplot=0

    for zrot,i in zip(set_zrot, range(len(set_zrot))):
        linetype=linestyles[i]
        subplot += 1
        ax = plt.subplot(2,2,subplot)
        print("* zrot: %s"%zrot)
        for solid,j in zip(set_solids,range(len(set_solids))):
            zrotelementsolid = zrot_solids_dict[zrot][solid]
            linecolor = colors[j]
            print("  * solid: %s" % solid)
            ax.plot(zrotelementsolid['lift'], zrotelementsolid['fz'], label=solid, color=linecolor, linestyle=linetype)

        ax.set_title("zrot: %s" % zrot)
        ax.set_xlabel('Lift [°]')
        ax.set_ylabel('Lift [dN]')
        ax.legend(loc="best")
        ax.margins(0.1)

    subplot += 1
    ax = plt.subplot(2,2,subplot)
    for solid,j in zip(set_solids,range(len(set_solids))):
        for zrot,i in zip(set_zrot,range(len(set_zrot))):
            linetype=linestyles[i]
            linecolor = colors[j]
            zrotelement = zrot_solids_dict[zrot][solid]
            ax.plot(zrotelement["lift"],zrotelement["fz"],label=solid,color=linecolor,linestyle=linetype)
    ax.set_title("Lift overall")
    ax.set_xlabel('Lift [°]')
    ax.set_ylabel('Lift [dN]')
    ax.margins(0.1)

    subplot += 1
    ax = plt.subplot(2,2,subplot)
    for solid,j in zip(set_solids,range(len(set_solids))):
        i=0
        linetype=linestyles[i]
        linecolor = colors[j]
        zrotelement1 = zrot_solids_dict[set_zrot[1]][solid]
        zrotelement0 = zrot_solids_dict[set_zrot[0]][solid]
        delta_fz = zrotelement1['fz'] - zrotelement0['fz']
        ax.plot(zrotelement["lift"],delta_fz,label=solid,color=linecolor,linestyle=linetype)

    ax.set_title("Lift change (fz(zrot=-2) - fz(zrot=0)")
    ax.set_xlabel('Lift [°]')
    ax.set_ylabel('Lift change [dN]')
    ax.margins(0.1)

    plt.show()

def plot_lift_winglet_proto_EM18(simulation_dict, set_zrot, set_solids, zrot_solids_dict):
    """4 subplots with Fz """

    solid = "winglet_proto_EM18"
    assert solid in set_solids

    fig = plt.figure()
    subplot=0

    subplot += 1
    ax = plt.subplot(1,1,subplot)

    for zrot,i in zip(set_zrot, range(len(set_zrot))):
        linetype=linestyles[0]
        print("* zrot: %s"%zrot)
        j=1
        zrotelementsolid = zrot_solids_dict[zrot][solid]
        linecolor = colors[i]
        ax.plot(zrotelementsolid['lift'], zrotelementsolid['fz'], label="zrot: %s" % zrot, color=linecolor, linestyle=linetype)

    ax.plot((zrot_solids_dict[set_zrot[0]][solid]['lift']+zrot_solids_dict[set_zrot[1]][solid]['lift'])/2,
            (zrot_solids_dict[set_zrot[0]][solid]['fz']+zrot_solids_dict[set_zrot[1]][solid]['fz'])/2,
            label="average" % zrot, color=linecolor, linestyle=linestyles[1])

    ax.set_title(solid)
    ax.set_xlabel('Lift [°]')
    ax.set_ylabel('Lift [dN]')
    ax.legend(loc="best")
    ax.margins(0.1)

    plt.show()
