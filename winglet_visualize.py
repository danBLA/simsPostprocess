import numpy as np
import matplotlib.pyplot as plt
import sim

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

def plot_sideforce_all(set_zrot, set_solids, zrot_solids_dict):
    """4 subplots with Fy """

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
            ax.plot(zrotelementsolid['lift'], zrotelementsolid['fy'], label=solid, color=linecolor, linestyle=linetype)

        ax.set_title("zrot: %s" % zrot)
        ax.set_xlabel('Lift [°]')
        ax.set_ylabel('Sideforce [dN]')
        ax.legend(loc="best")
        ax.margins(0.1)

    subplot += 1
    ax = plt.subplot(2,2,subplot)
    for solid,j in zip(set_solids,range(len(set_solids))):
        for zrot,i in zip(set_zrot,range(len(set_zrot))):
            linetype=linestyles[i]
            linecolor = colors[j]
            zrotelement = zrot_solids_dict[zrot][solid]
            ax.plot(zrotelement["lift"],zrotelement["fy"],label=solid,color=linecolor,linestyle=linetype)
    ax.set_title("Sideforce overall")
    ax.set_xlabel('Lift [°]')
    ax.set_ylabel('Sideforce [dN]')
    ax.margins(0.1)

    subplot += 1
    ax = plt.subplot(2,2,subplot)
    for solid,j in zip(set_solids,range(len(set_solids))):
        i=0
        linetype=linestyles[i]
        linecolor = colors[j]
        zrotelement1 = zrot_solids_dict[set_zrot[1]][solid]
        zrotelement0 = zrot_solids_dict[set_zrot[0]][solid]
        delta_fz = zrotelement1['fy'] - zrotelement0['fy']
        ax.plot(zrotelement["lift"],delta_fz,label=solid,color=linecolor,linestyle=linetype)

    ax.set_title("Sideforce change (fy(zrot=-2) - fy(zrot=0)")
    ax.set_xlabel('Lift [°]')
    ax.set_ylabel('Sideforce change [dN]')
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

def plot_derivative_lift_all(set_zrot, set_solids, zrot_solids_dict):
    """4 subplots with Fz """

    fig = plt.figure()
    subplot=0

    sim.create_forces_derivative('lift', 'fz', set_zrot, set_solids, zrot_solids_dict)

    for zrot,i in zip(set_zrot, range(len(set_zrot))):
        linetype=linestyles[i]
        subplot += 1
        ax = plt.subplot(2,2,subplot)
        print("* zrot: %s"%zrot)
        for solid,j in zip(set_solids,range(len(set_solids))):
            zrotelementsolid = zrot_solids_dict[zrot][solid]
            linecolor = colors[j]
            print("  * solid: %s" % solid)
            ax.plot(zrotelementsolid['avg_lift'], zrotelementsolid['DfzDlift'], label=solid, color=linecolor, linestyle=linetype)

        ax.set_title("zrot: %s" % zrot)
        ax.set_xlabel('Lift [°]')
        ax.set_ylabel('Lift [d(dN)/d(°)]')
        ax.legend(loc="best")
        ax.margins(0.1)

    subplot += 1
    ax = plt.subplot(2,2,subplot)
    for solid,j in zip(set_solids,range(len(set_solids))):
        for zrot,i in zip(set_zrot,range(len(set_zrot))):
            linetype=linestyles[i]
            linecolor = colors[j]
            zrotelement = zrot_solids_dict[zrot][solid]
            ax.plot(zrotelement["avg_lift"],zrotelement["DfzDlift"],label=solid,color=linecolor,linestyle=linetype)
    ax.set_title("Lift overall")
    ax.set_xlabel('Lift [°]')
    ax.set_ylabel('Lift [d(dN)/d(°)]')
    ax.margins(0.1)

    plt.show()

def plot_derivative_sideforce_all(set_zrot, set_solids, zrot_solids_dict):
    """4 subplots with Fz """

    fig = plt.figure()
    subplot=0

    sim.create_forces_derivative('lift', 'fy', set_zrot, set_solids, zrot_solids_dict)

    for zrot,i in zip(set_zrot, range(len(set_zrot))):
        linetype=linestyles[i]
        subplot += 1
        ax = plt.subplot(2,2,subplot)
        print("* zrot: %s"%zrot)
        for solid,j in zip(set_solids,range(len(set_solids))):
            zrotelementsolid = zrot_solids_dict[zrot][solid]
            linecolor = colors[j]
            print("  * solid: %s" % solid)
            ax.plot(zrotelementsolid['avg_lift'], zrotelementsolid['DfyDlift'], label=solid, color=linecolor, linestyle=linetype)

        ax.set_title("zrot: %s" % zrot)
        ax.set_xlabel('Lift [°]')
        ax.set_ylabel('Sideforce [d(dN)/d(°)]')
        ax.legend(loc="best")
        ax.margins(0.1)

    subplot += 1
    ax = plt.subplot(2,2,subplot)
    for solid,j in zip(set_solids,range(len(set_solids))):
        for zrot,i in zip(set_zrot,range(len(set_zrot))):
            linetype=linestyles[i]
            linecolor = colors[j]
            zrotelement = zrot_solids_dict[zrot][solid]
            ax.plot(zrotelement["avg_lift"], zrotelement["DfyDlift"], label=solid, color=linecolor, linestyle=linetype)
    ax.set_title("Sideforce overall")
    ax.set_xlabel('Lift [°]')
    ax.set_ylabel('Sideforce [d(dN)/d(°)]')
    ax.margins(0.1)

    plt.show()

def plot_yaw_derivative_lift_all(set_zrot, set_solids, zrot_solids_dict):
    """4 subplots with Fz """

    fig = plt.figure()
    subplot=0

    sim.create_forces_zrot_derivative('fz', set_zrot, set_solids, zrot_solids_dict)

    subplot += 1
    ax = plt.subplot()
    for solid,j in zip(set_solids,range(len(set_solids))):
        zrot = set_zrot[0]
        i = 0

        linetype=linestyles[i]
        linecolor = colors[j]
        zrotelement = zrot_solids_dict[zrot][solid]
        ax.plot(zrotelement["lift"], zrotelement["DfzDyaw"], label=solid, color=linecolor, linestyle=linetype)

    ax.set_title("Lift-by-Yaw derivative")
    ax.set_xlabel('Lift [°]')
    ax.set_ylabel('d(Lift)/d(Yaw) [d(dN)/d(°)]')
    ax.legend(loc="best")
    ax.margins(0.1)

    plt.show()

def plot_dragforceratio_all(set_zrot, set_solids, zrot_solids_dict):
    """4 subplots with Fy """

    fig = plt.figure()
    fig.subplots_adjust(hspace=0.34)
    fig.subplots_adjust(top=0.95)
    subplot=0

    sim.create_dragforcelift_ratios(set_zrot, set_solids, zrot_solids_dict)

    force_by_fx = ['fzBYfx', 'fyBYfx', 'fyzBYfx']

    for f_by_fx,k in zip(force_by_fx, range(len(force_by_fx))):
        subplot += 1
        ax = plt.subplot(3,1,subplot)
        for zrot,i in zip(set_zrot, range(len(set_zrot))):
            linetype=linestyles[i]
            print("* zrot: %s"%zrot)
            for solid,j in zip(set_solids,range(len(set_solids))):
                zrotelementsolid = zrot_solids_dict[zrot][solid]
                linecolor = colors[j]
                print("  * solid: %s" % solid)
                ax.plot(zrotelementsolid['lift'], zrotelementsolid[f_by_fx],
                        label=solid+", zrot=%.1f"%zrot, color=linecolor, linestyle=linetype)

        ax.set_title(f_by_fx.replace("BY", "/").replace('fx', '|fx|').replace('fyz', '(fy^2+fz^2)^0.5'))
        ax.set_xlabel('Lift [°]')
        ax.set_ylabel('[-]')
        ## Shrink current axis by 20%
        #box = ax.get_position()
        #ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ## Put a legend to the right of the current axis
        # Shrink current axis's height by 10% on the bottom
        #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        if subplot == 3:
            box = ax.get_position()
            ax.set_position([box.x0, box.y0 + box.height * 0.1,
                             box.width, box.height * 0.9])

            # Put a legend below current axis
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
                      fancybox=True, shadow=True, ncol=2)


    plt.show()

def plot_lift_ref_other(refsolid, refdict, ref_zrot,set_solids,zrot_solids_dict):
    """2 subplots with Fz """

    fig = plt.figure()
    subplot=0

    for zrot,i in zip(ref_zrot, range(len(ref_zrot))):
        linetype=linestyles[i]
        subplot += 1
        ax = plt.subplot(2,1,subplot)
        print("* zrot: %s"%zrot)
        # the reference
        j = 0
        zrotelementsolid = refdict[zrot][refsolid]
        refsolid_lift = zrotelementsolid['lift']
        linecolor = colors[j]
        print("  * solid: %s" % refsolid)
        ax.plot(refsolid_lift, zrotelementsolid['fz'], label=refsolid, color=linecolor, linestyle=linetype)
        # the new sims
        for solid,j in zip(set_solids,range(1,len(set_solids)+1)):
            zrotelementsolid = zrot_solids_dict[zrot][solid]
            linecolor = colors[j]
            print("  * solid: %s" % solid)
            ax.plot(refsolid_lift, zrotelementsolid['fz'], label=solid, color=linecolor, linestyle=linetype)

        ax.set_title("Ref-Zrot: %s" % zrot)
        ax.set_xlabel('Ref-Lift [°]')
        ax.set_ylabel('Lift [dN]')
        ax.legend(loc="best")
        ax.margins(0.1)
    plt.show()

def plot_drag_ref_other(refsolid, refdict, ref_zrot,set_solids,zrot_solids_dict):
    """2 subplots with Fx """

    fig = plt.figure()
    subplot=0

    for zrot,i in zip(ref_zrot, range(len(ref_zrot))):
        linetype=linestyles[i]
        subplot += 1
        ax = plt.subplot(2,1,subplot)
        print("* zrot: %s"%zrot)
        # the reference
        j = 0
        zrotelementsolid = refdict[zrot][refsolid]
        refsolid_lift = zrotelementsolid['lift']
        linecolor = colors[j]
        print("  * solid: %s" % refsolid)
        ax.plot(refsolid_lift, np.absolute(zrotelementsolid['fx']), label=refsolid, color=linecolor, linestyle=linetype)
        # the new sims
        for solid,j in zip(set_solids,range(1,len(set_solids)+1)):
            zrotelementsolid = zrot_solids_dict[zrot][solid]
            linecolor = colors[j]
            print("  * solid: %s" % solid)
            ax.plot(refsolid_lift, np.absolute(zrotelementsolid['fx']), label=solid, color=linecolor, linestyle=linetype)

        ax.set_title("Ref-Zrot: %s" % zrot)
        ax.set_xlabel('Ref-Lift [°]')
        ax.set_ylabel('Drag [dN]')
        ax.legend(loc="best")
        ax.margins(0.1)
    plt.show()

def plot_liftangle_ref_other(refsolid, refdict, ref_zrot,set_solids,zrot_solids_dict):
    """2 subplots with Fx """

    fig = plt.figure()
    subplot=0

    for zrot,i in zip(ref_zrot, range(len(ref_zrot))):
        linetype=linestyles[i]
        subplot += 1
        ax = plt.subplot(2,1,subplot)
        print("* zrot: %s"%zrot)
        # the reference
        j = 0
        zrotelementsolid = refdict[zrot][refsolid]
        refsolid_lift = zrotelementsolid['lift']
        linecolor = colors[j]
        print("  * solid: %s" % refsolid)
        ax.plot(refsolid_lift, zrotelementsolid['lift'], label=refsolid, color=linecolor, linestyle=linetype)
        # the new sims
        for solid,j in zip(set_solids,range(1,len(set_solids)+1)):
            zrotelementsolid = zrot_solids_dict[zrot][solid]
            linecolor = colors[j]
            print("  * solid: %s" % solid)
            ax.plot(refsolid_lift, zrotelementsolid['lift'], label=solid, color=linecolor, linestyle=linetype)

        ax.set_title("Ref-Zrot: %s" % zrot)
        ax.set_xlabel('Ref-Lift [°]')
        ax.set_ylabel('Lift [°]')
        ax.grid(color='gray', linestyle='--', linewidth=1)
        ax.legend(loc="best")
        ax.margins(0.1)
    plt.show()

def plot_dragforceratio_ref_other(refsolid , refdict, set_zrot, set_solids, zrot_solids_dict):
    """4 subplots with Fy """

    fig = plt.figure()
    fig.subplots_adjust(hspace=0.34)
    fig.subplots_adjust(top=0.95)
    subplot=0

    sim.create_dragforcelift_ratios(set_zrot, set_solids, zrot_solids_dict)

    force_by_fx = ['fzBYfx', 'fyBYfx', 'fyzBYfx']

    for f_by_fx,k in zip(force_by_fx, range(len(force_by_fx))):
        subplot += 1
        ax = plt.subplot(3,1,subplot)
        for zrot,i in zip(set_zrot, range(len(set_zrot))):
            linetype=linestyles[i]
            print("* zrot: %s"%zrot)

            zrotelementsolid = refdict[zrot][refsolid]
            refsolid_lift = zrotelementsolid['lift']

            for solid,j in zip(set_solids,range(1,len(set_solids)+1)):
                zrotelementsolid = zrot_solids_dict[zrot][solid]
                linecolor = colors[j]
                print("  * solid: %s" % solid)
                ax.plot(zrotelementsolid['lift'], zrotelementsolid[f_by_fx],
                        label=solid+", zrot=%.1f"%zrot, color=linecolor, linestyle=linetype)

        ax.set_title(f_by_fx.replace("BY", "/").replace('fx', '|fx|').replace('fyz', '(fy^2+fz^2)^0.5'))
        ax.set_xlabel('Lift [°]')
        ax.set_ylabel('[-]')
        ## Shrink current axis by 20%
        #box = ax.get_position()
        #ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ## Put a legend to the right of the current axis
        # Shrink current axis's height by 10% on the bottom
        #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        if subplot == 3:
            box = ax.get_position()
            ax.set_position([box.x0, box.y0 + box.height * 0.1,
                             box.width, box.height * 0.9])

            # Put a legend below current axis
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
                      fancybox=True, shadow=True, ncol=2)


    plt.show()

def plot_dragforceratio_ref_other2(refsolid , refdict, set_zrot, set_solids, zrot_solids_dict):
    """4 subplots with Fy """

    fig = plt.figure()
    fig.subplots_adjust(hspace=0.63)
    fig.subplots_adjust(bottom=0.23)
    fig.subplots_adjust(top=0.95)
    subplot=0

    sim.create_dragforcelift_ratios(set_zrot, set_solids, zrot_solids_dict)

    force = ['fz', 'fy', 'fyz']

    for f_by_fx,k in zip(force, range(len(force))):
        subplot += 1
        ax = plt.subplot(3,1,subplot)
        for zrot,i in zip(set_zrot, range(len(set_zrot))):
            linetype=linestyles[i]
            print("* zrot: %s"%zrot)

            linecolor = colors[0]

            zrotelementsolid = refdict[zrot][refsolid]
            ax.plot(np.absolute(zrotelementsolid['fx']), zrotelementsolid[f_by_fx],
                    label=refsolid+", zrot=%.1f"%zrot, color=linecolor, linestyle=linetype)

            for solid,j in zip(set_solids,range(1,len(set_solids)+1)):
                zrotelementsolid = zrot_solids_dict[zrot][solid]
                linecolor = colors[j]
                print("  * solid: %s" % solid)
                ax.plot(np.absolute(zrotelementsolid['fx']), zrotelementsolid[f_by_fx],
                        label=solid+", zrot=%.1f"%zrot, color=linecolor, linestyle=linetype)

        ax.set_title(f_by_fx.replace('fyz', '(fy^2+fz^2)^0.5'))
        ax.set_xlabel('Drag [dN]')
        ax.set_ylabel('force [dN]')
        ax.grid(color='gray', linestyle='--', linewidth=1)
        ## Shrink current axis by 20%
        #box = ax.get_position()
        #ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ## Put a legend to the right of the current axis
        # Shrink current axis's height by 10% on the bottom
        #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        if subplot == 3:
            box = ax.get_position()
            ax.set_position([box.x0, box.y0 + box.height * 0.1,
                             box.width, box.height * 0.9])

            # Put a legend below current axis
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.5),
                      fancybox=True, shadow=True, ncol=2)


    plt.show()
