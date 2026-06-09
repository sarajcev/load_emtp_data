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
        white_list.extend([busa, busb, busc])
        white_list.extend([mag, phase])

    # Machine signals.
    for name in varnames:
        white_list.extend(
            ['PowerPlant_' + f'{i:02d}' + name 
            for i in range(1, 11) # ten machines
            if i not in exclude]
        )
    
    # Renewables connected to the power system?
    if variant in ['V1', 'V2', 'V3']:
        # Wind farm signals (DEV2).
        white_list.extend(['DEV2/P', 'DEV2/Q'])
        white_list.extend(['DEV2/V0', 'DEV2/V1', 'DEV2/V2'])
        white_list.extend(['DEV2/I0', 'DEV2/I1', 'DEV2/I2'])
        white_list.append('FFC_WP2/Wind_Turbine/PMSG_T_rotor')
        white_list.append('FFC_WP2/Wind_Turbine/PMSG_w_rotor')
        white_list.append('FFC_WP2/Converter_control/Control/Grid_Ctrl/FRT_flag')
        # Solar park signals (DEV3).
        white_list.extend(['DEV3/P', 'DEV3/Q'])
        white_list.extend(['DEV3/V0', 'DEV3/V1', 'DEV3/V2'])
        white_list.extend(['DEV3/I0', 'DEV3/I1', 'DEV3/I2'])
        white_list.append('WECC_PVPark_1/Converter_control/Control/GridControl_DLL/FRT_flag')
    
    return white_list


def plot_machine_signals(data, category, title=False):
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
        ax.set_title(title, fontsize=9)
    for name in data.columns:
        if category in name:
            signal = data[name].values
            ax.plot(time, signal, ls='-', lw=1.5, label=name.split('/')[0])
    ax.legend(loc='upper right', frameon=True, fancybox=True, fontsize=8)
    ax.grid(which='major', axis='both')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel(category)
    fig.tight_layout()
    plt.show()
    return


def plot_machine_delta_signals(data, title=False):
    """
    Plot machine angles in regard to the slack bus.

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame holding simulation signals.
    title : bool, default=False
        Figure title from key.
    
    Returns
    -------
    Show matplotlib figure with plots of machine angles
    with regards to the slack bus.

    Notes
    -----
    This function is tailored for the machine signals,
    which contain 'Teta' string in their name.
    """
    time = data['time'].values
    # Slack bus is represented by the machine G2.
    slack_signal = data['PowerPlant_02/Teta_1_SM1'].values

    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    if title:
        ax.set_title(title, fontsize=9)
    for name in data.columns:
        if 'Teta' in name:
            signal = data[name].values
            pp = name.split('/')[0][-2:]
            if pp == '02':
                # This is the slack bus, skip it.
                continue
            else:
                # Difference in the swing from the slack machine.
                delta_signal = slack_signal - signal
                ax.plot(time, delta_signal, ls='-', lw=1.5,
                        label=name.split('/')[0])
    ax.legend(loc='upper right', frameon=True, fancybox=True, fontsize=8)
    ax.grid(which='major', axis='both')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Angle difference')
    fig.tight_layout()
    plt.show()
    return


def plot_bus_voltages_rms(data, bus, xlim=None):
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
    ax.legend(loc='lower right', frameon=True, fancybox=True, fontsize=8)
    ax.grid(which='major', axis='both')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('RMS voltage (p.u.)')
    if xlim is not None:
        ax.set_xlim(0, xlim)
    fig.tight_layout()
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
    t_start = int(0.1/dt)
    t_end = int((0.1 + t_sc)/dt)
    if limit is None:
        lim = -1
    else:
        lim = int(limit/dt) + 1
    mag = data[bus+'/V1_mag'].values
    ang = data[bus+'/V1_phase'].values

    fig, ax = plt.subplots(2, 1, figsize=(5.5, 6.5),
                           height_ratios=[1, 3])
    ax_top = ax[0]
    ax[1].remove()
    # Top row subplot.
    ax_top.plot(data['time'], data[bus + '/Vrms_a'], label='phase a', c='darkorange')
    ax_top.plot(data['time'], data[bus + '/Vrms_b'], label='phase b', c='grey')
    ax_top.plot(data['time'], data[bus + '/Vrms_c'], label='phase c')
    ax_top.axvspan(0, limit, color='wheat', alpha=0.3)
    ax_top.legend(loc='lower right', frameon=True, fancybox=True)
    ax_top.set_xlabel('Time (s)')
    ax_top.set_ylabel('Voltage (pu)')
    ax_top.grid()
    # Main area subplot.
    ax = fig.add_subplot(2, 1, 2, projection='polar')
    ax.text(ang[t_start], mag[t_start], 't = 0.1 s', color='red', fontsize=9)
    ax.text(ang[t_end], mag[t_end], f't = {0.1+t_sc} s', color='red', fontsize=9)
    if show_line:
        ax.plot(ang[:t_start], mag[:t_start], c='dimgrey',
                ls='--', lw=1, zorder=-1)
        ax.plot(ang[t_start:t_end], mag[t_start:t_end], c='red',
                ls='--', lw=1, zorder=-1)
        ax.plot(ang[t_end:lim], mag[t_end:lim], c='dimgrey',
                ls='--', lw=1, zorder=-1)
    sc = ax.scatter(ang[:lim], mag[:lim], c=time[:lim],
                    cmap='cividis', marker='o', s=8, zorder=1)
    cb = plt.colorbar(sc, ax=ax, orientation='vertical', fraction=0.15, pad=0.1)
    cb.set_label('Time (s)')
    if save:
        plt.savefig(key + ':' + bus + '.png', dpi=600)
    plt.show()
    return


def tsi_from_angle(data, tol=5):
    """
    Transient Stability Index (TSI) for the simulation.

    TSI is obtained from the machine swing angles,
    in regard to the slack bus angle (i.e. machine G2).

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame holding simulation signals.
    tol : float, default=5
        Tolerance for signal detection in degrees.

    Returns
    -------
    tsi : int
        TSI value: 0 - stable case, 1 - unstable case.
    """
    # Machine's swing angle in regard to the slack bus,
    # which is represented by the machine G2.
    slack_signal = data['PowerPlant_02/Teta_1_SM1'].values
    tsi = 0
    for name in data.columns:
        if 'Teta' in name:
            signal = data[name].values
            pp = name.split('/')[0][-2:]
            if pp == '02':
                # This is the slack bus, skip it.
                continue
            else:
                # Difference in the swing from the slack machine.
                delta_signal = slack_signal - signal
                # Absolute difference between the first and last point
                # of the swing difference from the slack machine.
                dd = abs(delta_signal[0] - delta_signal[-1])
                if dd > tol:
                    # If this difference is larger than the prescribed
                    # tolerance, then the swing is unstable.
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
    fig = plt.figure(figsize=(7, 6.5), layout='constrained')
    gs = GridSpec(3, 3, figure=fig)
    # Top row subplot.
    ax_top = fig.add_subplot(gs[0, :])
    ax_top.plot(data['time'], data[plant + '/Pe_SM1'],
                c='royalblue', label='Pe')
    ax_top.legend(loc='best', frameon=True, fancybox=True)
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
    # Right side upper subplot.
    ax_le1 = fig.add_subplot(gs[1, 2])
    ax_le1.plot(data[plant + '/vd_SM1'], data[plant + '/vq_SM1'], lw=1)
    ax_le1.set_xlabel('vd (pu)')
    ax_le1.set_ylabel('vq (pu)')
    ax_le1.grid()
    # Right side lower subplot.
    ax_le2 = fig.add_subplot(gs[2, 2])
    ax_le2.plot(data[plant + '/id_SM1'], data[plant + '/iq_SM1'],
                c='steelblue', lw=1)
    ax_le2.set_xlabel('id (pu)')
    ax_le2.set_ylabel('iq (pu)')
    ax_le2.grid()
    if tsi:
        ax_mid.set_ylim(bottom=0, top=500)
    if save:
        plt.savefig(key + ':' + plant + '.png', dpi=600)
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
    #data = data[key]
    fig = plt.figure(figsize=(7, 6.5), layout='constrained')
    gs = GridSpec(3, 3, figure=fig)
    # Top row subplot.
    ax_top = fig.add_subplot(gs[0, :])
    ax_top.plot(data['time'], data[plant + '/P']/1e6, label='active (P)')
    ax_top.plot(data['time'], data[plant + '/Q']/1e6, label='reactive (Q)')
    ax_top.legend(loc='best', frameon=True, fancybox=True)
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
    ax_bot.plot(data['time'], data[plant + '/FRT_flag'])
    ax_bot.set_xlabel('Time (s)')
    ax_bot.set_ylabel('FRT flag')
    ax_bot.grid()
    if save:
        plt.savefig(key + ':' + plant + '.png', dpi=600)
    plt.show()
    return