import matplotlib.pylab as plt
from matplotlib.gridspec import GridSpec


def create_white_list(varnames, exclude, buses, variant):
    """
    Create a `white_list` variable for extracting 
    EMTP simulations signals from the IEEE New England 
    39-bus test power system.

    Parameters
    ----------
    varnames : list
        List of machine variable names that will be in the 
        `white_list` variable.
    exclude : list
        List of indexes for the conventional generators that are 
        excluded from the simulation (and possibly replaced by the 
        renewable sources). This list can be empty.
    buses : list
        List of BUS indexes that have voltage measurements.
    variant : str
        Variable that specifies scenario variant. It can take
        one of the following values:
        'V0' - classical IEEE New England 39-bus power system
               (with no renewables),
        'V1' - adapted IEEE New England 39-bus power system with
               20% share of renewables (connected at locations
               of excluded generators).
        
    Returns
    -------
    white_list : list
        List with variable names for the simulation.
    """
    # Form a "white list" of variable names.
    white_list = []

    # Bus voltages.
    for bus in buses:       
        # Phase a, b and c values.
        busa = 'BUS' + str(bus) + '/Vrms_a'
        busb = 'BUS' + str(bus) + '/Vrms_b'
        busc = 'BUS' + str(bus) + '/Vrms_c'
        # Direct sequence magnitude and phase angle.
        mag = 'BUS' + str(bus) + '/V1_mag'
        phase = 'BUS' + str(bus) + '/V1_phase'
        # Frequency measurement.
        freq = 'BUS' + str(bus) + '/Freq'
        # Add variables to the white list.
        white_list.extend([busa, busb, busc])
        white_list.extend([mag, phase])
        white_list.append(freq)

    # Machine signals.
    for name in varnames:
        white_list.extend(
            ['PowerPlant_' + f'{i:02d}' + name 
            for i in range(1, 11) # ten machines
            if i not in exclude]
        )
    
    # Renewables connected to the power system?
    if variant in ['V1', 'V2', 'V3', 'V4']:
        # Wind farm signals (DEV2). 
        # This WF replaces machine G8.
        white_list.extend(['DEV2/P', 'DEV2/Q'])
        white_list.extend(['DEV2/V0', 'DEV2/V1', 'DEV2/V2'])
        white_list.extend(['DEV2/I0', 'DEV2/I1', 'DEV2/I2'])
        white_list.append('FFC_WP1/Wind_Turbine/PMSG_T_rotor')
        white_list.append('FFC_WP1/Wind_Turbine/PMSG_w_rotor')
        white_list.append('FFC_WP1/Converter_control/Control/Grid_Ctrl/FRT_flag')
        # PV plant signals (DEV3). 
        # This PV replaces machine G5.
        white_list.extend(['DEV3/P', 'DEV3/Q'])
        white_list.extend(['DEV3/V0', 'DEV3/V1', 'DEV3/V2'])
        white_list.extend(['DEV3/I0', 'DEV3/I1', 'DEV3/I2'])
        white_list.append(
            'WECC_PVPark_1/Converter_control/Control/GridControl_DLL/FRT_flag'
        )
    
    if variant in ['V2', 'V3', 'V4']:
        # These are variants with 40% share of renewables.
        # Wind farm 2 (WF2) signals (DEV4).
        # This WF replaces machine G9.
        white_list.extend(['DEV4/P', 'DEV4/Q'])
        white_list.extend(['DEV4/V0', 'DEV4/V1', 'DEV4/V2'])
        white_list.extend(['DEV4/I0', 'DEV4/I1', 'DEV4/I2'])
        white_list.append('FFC_WP2/Wind_Turbine/PMSG_T_rotor')
        white_list.append('FFC_WP2/Wind_Turbine/PMSG_w_rotor')
        white_list.append('FFC_WP2/Converter_control/Control/Grid_Ctrl/FRT_flag')
        # PV plant 2 (PV2) signals (DEV5).
        # This PV replaces machine G3.
        white_list.extend(['DEV5/P', 'DEV5/Q'])
        white_list.extend(['DEV5/V0', 'DEV5/V1', 'DEV5/V2'])
        white_list.extend(['DEV5/I0', 'DEV5/I1', 'DEV5/I2'])
        white_list.append(
            'WECC_PVPark_2/Converter_control/Control/GridControl_DLL/FRT_flag'
        )
    
    if variant in ['V4']:
        # This is a variant with 60% share of renewables.
        # PV plant 3 (PV3) signals (DEV6).
        # This PV replaces machine G10.
        white_list.extend(['DEV6/P', 'DEV6/Q'])
        white_list.extend(['DEV6/V0', 'DEV6/V1', 'DEV6/V2'])
        white_list.extend(['DEV6/I0', 'DEV6/I1', 'DEV6/I2'])
        white_list.append(
            'WECC_PVPark_3/Converter_control/Control/GridControl_DLL/FRT_flag'
        )
    
    return white_list


def plot_machine_signals(data, category, title=False, xlim=None, save=False):
    """
    Plot EMTP-RV simulation signals for the machines.

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame holding simulation signals.
    category : str
        Name of the category for the signals in the "white
        list" that will be plotted. Category can be, for
        example, 'Teta', 'Omega', etc., which defines a
        particular group of signals in the white list.
    title : bool, default=False
        Figure title from key.
    xlim : float or None, default=None
        Time limit of the signal display. It is
        ignored if None.
    save : bool, default=False
        Indicator for saving figure to disk.

    Returns
    -------
    Show matplotlib figure with plots of signals from the
    selected category.

    Notes
    -----
    This function is tailored for the machine signals,
    which contain 'PowerPlant' string in their name.
    DataFrame is exported from the simulation class.
    """
    time = data['time'].values

    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    if title:
        ax.set_title(str(title), fontsize=9)
    for name in data.columns:
        if category in name:
            signal = data[name].values
            ax.plot(time, signal, ls='-', lw=1.5, label=name.split('/')[0])
    ax.legend(loc='upper right', frameon=True, fancybox=True, fontsize=8)
    ax.grid(which='major', axis='both')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel(category)
    if xlim is not None:
        ax.set_xlim(0, xlim)
    fig.tight_layout()
    if save:
        plt.savefig(category + '_signals.pdf')
    plt.show()

    return


def plot_machine_delta_signals(data, title=False, lims=None, save=False):
    """
    Plot machine angles in regard to the external grid.

    Machine angles ploted in regard to the external grid,
    which is represented by the generator G1. This machine
    is traditionally used as a reference generator to which
    all other generators' angles are referenced.

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame holding simulation signals.
    title : bool, default=False
        Figure title from key.
    lims : tuple or None
        A tuple with a lower and upper limit of the delta angle
        for y-axis display or None.
    save : bool, default=False
        Indicator for saving figure to disk.

    Returns
    -------
    Show matplotlib figure with plots of machine angles
    in regard to the external grid.

    Notes
    -----
    This function is tailored for the machine signals,
    which contain 'Teta' string in their name.

    References
    ----------
    IEEE PES Task Force on Benchmark Systems for Stability Controls,
    Report on the EMTP-RV 39-bus system (New England Reduced Model),
    Version 1.5 - Mars 04, 2015.
    """
    time = data['time'].values
    # External grid is represented by the machine G1.
    slack_signal = data['PowerPlant_01/Teta_1_SM1'].values
    
    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    if title:
        ax.set_title(str(title), fontsize=9)
    for name in data.columns:
        if 'Teta' in name:
            signal = data[name].values
            pp = name.split('/')[0][-2:]
            if pp == '01':
                # This is the external grid, skip it.
                continue
            else:
                # Difference in the swing from the reference.
                delta_signal = slack_signal - signal
                ax.plot(time, delta_signal, ls='-', lw=1.5,
                        label=name.split('/')[0])
    ax.legend(loc='upper right', frameon=True, fancybox=True, fontsize=8)
    ax.grid(which='major', axis='both')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Angle difference (deg)')
    if lims is not None:
        b, t = lims  # bottom, top limits
        ax.set_ylim(bottom=b, top=t)
    fig.tight_layout()
    if save:
        plt.savefig('machine_delta_signals.pdf')
    plt.show()

    return


def plot_frequency(data, list_of_nodes, xlim=None, save=False):
    """Plot frequency at selected nodes.

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame holding simulation signals.
    list_of_nodes : list of integers
        List of nodes to plot. First node is emphasized.
    xlim : float or None, default=None
        Time limit of the signal display. It is
        ignored if None.
    save : bool, default=False
        Indicator for saving figure to disk.

    Returns
    -------
    Show matplotlib figure.
    """
    time = data['time']

    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    for k, node in enumerate(list_of_nodes):
        bus = 'BUS' + str(node)
        if k == 0:
            # First node is emphasized.
            ax.plot(time, data[bus + '/Freq'], ls='-', lw=2, c='dimgrey',
                    label=bus)
        else:
            ax.plot(time, data[bus + '/Freq'], ls='-', lw=1, label=bus)
    ax.legend(loc='lower right', frameon=True, fancybox=True, fontsize=9)
    ax.grid(which='major', axis='both')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    if xlim is not None:
        ax.set_xlim(0.4, xlim)
    fig.tight_layout()
    if save:
        plt.savefig('frequency.pdf')
    plt.show()

    return


def plot_bus_voltages_rms(data, bus, xlim=None, save=False):
    """
    Plot three-phase bus voltage RMS values.

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame holding simulation signals.
    bus : str
        Name of the bus, e.g. 'BUS2'.
    xlim : float or None, default=None
        Time limit of the signal display. It is
        ignored if None.
    save : bool, default=False
        Indicator for saving figure to disk.

    Returns
    -------
    Show matplotlib figure.
    """
    time = data['time'].values

    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    ax.set_title(f'RMS voltage at: {bus}', fontsize=10)
    ax.plot(time, data[bus+'/Vrms_a'], ls='-', lw=1.5, label='Vrms_a')
    ax.plot(time, data[bus+'/Vrms_b'], ls='-', lw=1.5, label='Vrms_b')
    ax.plot(time, data[bus+'/Vrms_c'], ls='-', lw=1.5, label='Vrms_c')
    ax.plot(time, data[bus+'/V1_mag'], ls="--", lw=1.5,
            c="dimgrey", label="dir. comp.")
    ax.legend(loc='lower right', frameon=True, fancybox=True, fontsize=9)
    ax.grid(which='major', axis='both')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('RMS voltage (p.u.)')
    if xlim is not None:
        ax.set_xlim(0, xlim)
    fig.tight_layout()
    if save:
        plt.savefig(bus + '.pdf')
    plt.show()

    return


def plot_bus_voltage(data, key, bus, t_sc=0.1, limit=None,
                         show_line=True, save=False):
    """
    Plot BUS voltages.

    Plot three-phase bus voltage RMS values, along with a direct
    sequence bus voltage as a polar plot.

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame holding simulation signals.
    key : str
        String identifying dictionary key with information
        on type and location of the short-circuit. Then,
        data[key] is a pandas DataFrame with simulation signals
        for that particular case, e.g. data['SC3-BUS2'] holds
        data for the three-phase short circuit at bus number 2.
    bus : str
        Name of the bus, e.g. 'BUS2'.
    t_sc : float, default=0.1
        Duration of the short-circuit (s).
    limit : float or None, default=None
        Time limit of the voltage display in seconds.
    show_line : bool, default=True
        Show the line connecting individual points of
        voltage measurements.
    save : bool, default=False
        Indicator for saving the figure to external file.

    Returns
    -------
    Show matplotlib figure.
    """
    data = data[key]
    time = data['time'].values

    dt = time[1] - time[0]
    # Time of SC start, and index points for the SC start and end.
    sc_start = 0.5
    t_start = int(sc_start/dt)
    t_end = int((sc_start + t_sc)/dt)
    # Starting time and index point for plotting.
    t_begin = sc_start - 0.1
    ti_begin = int(t_begin/dt)
    if limit is None:
        lim = -1
    else:
        # Index of the time limit for plotting.
        lim = int(limit/dt) + 1
    mag = data[bus+'/V1_mag'].values
    ang = data[bus+'/V1_phase'].values

    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(5.5, 6.5),
                           height_ratios=[1, 3])
    ax_top = ax[0]
    ax[1].remove()

    # Top row subplot.
    ax_top.plot(data['time'], data[bus + '/Vrms_a'], label='phase a')
    ax_top.plot(data['time'], data[bus + '/Vrms_b'], label='phase b')
    ax_top.plot(data['time'], data[bus + '/Vrms_c'], label='phase c')
    ax_top.plot(data['time'], mag, ls='--', c='dimgrey', label='dir. comp.')
    ax_top.axvspan(t_begin, limit, color='wheat', alpha=0.3)
    ax_top.legend(loc='lower right', frameon=True, fancybox=True, fontsize=9)
    ax_top.set_xlabel('Time (s)')
    ax_top.set_ylabel('Voltage (pu)')
    ax_top.grid()

    # Main area subplot (polar voltage plot).
    ax = fig.add_subplot(2, 1, 2, projection='polar')
    # Mark the starting time of SC.
    ax.text(ang[t_start], mag[t_start], f't = {sc_start} s',
            color='red', fontsize=9)
    # Mark the ending time of SC.
    ax.text(ang[t_end], mag[t_end], f't = {sc_start + t_sc} s',
            color='red', fontsize=9)
    if show_line:
        # Connect individual time points with lines.
        ax.plot(ang[ti_begin:t_start], mag[ti_begin:t_start], c='dimgrey',
                ls='--', lw=1, zorder=-1)
        ax.plot(ang[t_start:t_end], mag[t_start:t_end], c='red',
                ls='--', lw=1, zorder=-1)
        ax.plot(ang[t_end:lim], mag[t_end:lim], c='dimgrey',
                ls='--', lw=1, zorder=-1)
    # Plot individual points (time is color).
    sc = ax.scatter(ang[ti_begin:lim], mag[ti_begin:lim], c=time[ti_begin:lim],
                    cmap='cividis', marker='o', s=8, zorder=1)
    cb = plt.colorbar(sc, ax=ax, orientation='vertical', fraction=0.15, pad=0.1)
    cb.set_label('Time (s)')

    if save:
        plt.savefig(key + ':' + bus + '.pdf')
    plt.show()

    return


def tsi_from_angle(data, tol=60):
    """
    Transient Stability Index (TSI) for the simulation.

    TSI is obtained from the machine swing angles,
    in regard to the reference machine angle (i.e. machine
    G1 which serves as an extenal system). If any of the
    machines in the system is unstable, then TSI = 1;
    otherwise, if all machines are stable then TSI = 0.

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame holding simulation signals.
    tol : float, default=60
        Tolerance for signal detection in degrees.

    Returns
    -------
    tsi : int
        TSI value: 0 - stable case, 1 - unstable case.
    """
    # Machine's swing angle in regard to the reference,
    # which is represented by the machine G1 (external system).
    slack_signal = data['PowerPlant_01/Teta_1_SM1'].values
    tsi = 0
    for name in data.columns:
        if 'Teta' in name:
            signal = data[name].values
            pp = name.split('/')[0][-2:]
            if pp == '01':
                # This is the external system, skip it.
                continue
            else:
                # Difference in the swing from the reference.
                delta_signal = slack_signal - signal
                # Absolute difference between the first and last point
                # of the swing difference.
                dd = abs(delta_signal[0] - delta_signal[-1])
                if dd > tol:
                    # If this difference is larger than the prescribed
                    # tolerance, then the swing is considered unstable.
                    tsi = 1
                    break
    return tsi


def plot_machine_multi_figure(data, key, plant, save=False):
    """
    Plot machine signals with multiple subplots.

    Parameters
    ----------
    data : dictionary
        Dictionary holding simulation data.
    key : str
        String identifying dictionary key with information
        on type and location of the short-circuit. Then,
        data[key] is a pandas DataFrame with simulation signals
        for that particular case, e.g. data['SC3-BUS2'] holds
        data for the three-phase short circuit at bus number 2.
    plant : str
        String identifying machine for which signals will
        be plotted, e.g. 'PowerPlant_07'.
    save : bool, default=False
        Indicator for saving the figure to external file.

    Returns
    -------
    Shows a matplotlib figure.
    """
    data = data[key]
    tsi = 0
    fig = plt.figure(figsize=(6.5, 6), layout='constrained')
    gs = GridSpec(nrows=3, ncols=3, figure=fig)

    # Top row subplot.
    ax_top = fig.add_subplot(gs[0, :])
    ax_top.plot(data['time'], data[plant + '/Pe_SM1'], label='/Pe_SM1')
    ax_top.legend(loc='lower right', frameon=True, fancybox=True, fontsize=9)
    ax_top.set_xlabel('Time (s)')
    ax_top.set_ylabel('Power (pu)')
    ax_top.grid()

    # Main area subplot.
    ax_mid = fig.add_subplot(gs[1:, 0:-1])
    for name in data.columns:
        if 'Teta' in name:
            if data[name].values[-1] > 500:
                tsi = 1
            pp = name.split('/')[0]
            if pp == plant:
                ax_mid.plot(data['time'], data[name],
                            c='steelblue', lw=2.5, label=plant)
            else:
                ax_mid.plot(data['time'], data[name], c='grey', ls='-', lw=1)
    ax_mid.set_xlabel('Time (s)')
    ax_mid.set_ylabel('Rotor angle (deg)')
    ax_mid.grid()
    if tsi:
        ax_mid.set_ylim(bottom=0, top=500)

    # Right side upper subplot.
    ax_le1 = fig.add_subplot(gs[1, 2])
    ax_le1.plot(data[plant + '/vd_SM1'], data[plant + '/vq_SM1'],
                c='seagreen', lw=1)
    ax_le1.set_xlabel('vd (pu)')
    ax_le1.set_ylabel('vq (pu)')
    ax_le1.grid()

    # Right side lower subplot.
    ax_le2 = fig.add_subplot(gs[2, 2])
    ax_le2.plot(data[plant + '/id_SM1'], data[plant + '/iq_SM1'],
                c='darkorange', lw=1)
    ax_le2.set_xlabel('id (pu)')
    ax_le2.set_ylabel('iq (pu)')
    ax_le2.grid()

    if save:
        plt.savefig(key + ':' + plant + '.pdf')
    plt.show()

    return


def plot_ren_multi_figure(data, key, plant, save=False):
    """
    Plot renewables (Wind or PV) signals with multiple subplots.

    Parameters
    ----------
    data : dictionary
        Dictionary holding simulation data.
    key : str
        String identifying dictionary key with information
        on type and location of the short-circuit. Then,
        data[key] is a pandas DataFrame with simulation signals
        for that particular case, e.g. data['SC3-BUS2'] holds
        data for the three-phase short circuit at bus number 2.
    plant : str
        String that identifies if the 'WF' or 'PV' signals will
        be plotted.
    save : bool, default=False
        Indicator for saving the figure to external file.

    Returns
    -------
    Shows a matplotlib figure.
    """
    data = data[key]
    fig = plt.figure(figsize=(6.5, 5), layout='constrained')
    gs = GridSpec(nrows=3, ncols=3, figure=fig, height_ratios=[2, 2, 1])

    # Top row subplot.
    ax_top = fig.add_subplot(gs[0, :])
    ax_top.plot(data['time'], data[plant + '/P']/1e6, label='active (P)')
    ax_top.plot(data['time'], data[plant + '/Q']/1e6, label='react. (Q)')
    ax_top.legend(loc='best', frameon=True, fancybox=True, fontsize=9)
    ax_top.set_xlabel('Time (s)')
    ax_top.set_ylabel('Power (MW)')
    ax_top.grid()

    # Middle row subplots.
    ax0 = fig.add_subplot(gs[1, 0])
    ax0.plot(data['time'], data[plant + '/V1']/1e3, label='V1')
    ax0.legend(loc='best', frameon=True, fancybox=True)
    ax0.set_xlabel('Time (s)')
    ax0.set_ylabel('Voltage (kV)')
    ax0.grid()
    ax1 = fig.add_subplot(gs[1, 1])
    ax1.plot(data['time'], data[plant + '/V2']/1e3, c='darkorange', label='V2')
    ax1.legend(loc='best', frameon=True, fancybox=True)
    ax1.set_xlabel('Time (s)')
    #ax1.set_ylabel('Voltage (pu)')
    ax1.grid()
    ax2 = fig.add_subplot(gs[1, 2])
    ax2.plot(data['time'], data[plant + '/V0']/1e3, c='seagreen', label='V0')
    ax2.legend(loc='best', frameon=True, fancybox=True)
    ax2.set_xlabel('Time (s)')
    #ax2.set_ylabel('Voltage (pu)')
    ax2.grid()

    # Bottom row subplot.
    ax_bot = fig.add_subplot(gs[2, :])
    ax_bot.plot(data['time'], data[plant + '/FRT_flag'], c='steelblue')
    ax_bot.set_xlabel('Time (s)')
    ax_bot.set_ylabel('FRT flag')
    ax_bot.grid()

    if save:
        plt.savefig(key + ':' + plant + '.pdf')
    plt.show()

    return