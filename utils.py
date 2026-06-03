import re
import matplotlib.pylab as plt


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
        string = re.search(category, name)
        if string is not None:
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
    Plot machine angles with regards to the slack bus.

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
    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    if title:
        ax.set_title(title, fontsize=9)
    for name in data.columns:
        string = re.search('Teta', name)
        if string is not None:
            signal = data[name].values
            pp = name.split('/')[0][-2:]
            if pp == '02':
                # Slack machine.
                slack_signal = signal
                break
    for name in data.columns:
        string = re.search('Teta', name)
        if string is not None:
            signal = data[name].values
            pp = name.split('/')[0][-2:]
            if pp == '02':
                continue
            else:
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


def plot_bus_voltage_dir(data, bus, limit=None, show_line=False):
    """
    Plot direct sequence bus voltage as a polar plot.

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame holding simulation signals.
    bus : str
        Name of the bus, e.g. 'BUS2'.
    limit : float or None, default=None
        Time limit of the voltage display in seconds.
    show_line : bool, default=False
        Show the line connecting points of voltage measurements.
    
    Returns
    -------
    Show matplotlib figure.
    """
    time = data['time'].values
    dt = time[1] - time[0]
    t_start = int(0.1/dt)
    t_end = int(0.2/dt)
    if limit is None:
        lim = -1
    else:
        lim = int(limit/dt)+1
    mag = data[bus+'/V1_mag'].values
    ang = data[bus+'/V1_phase'].values
    fig, ax = plt.subplots(figsize=(5.5, 5),
                           subplot_kw=dict(projection='polar'))
    ax.text(ang[t_start], mag[t_start], 't = 0.1 s', color='red', fontsize=10)
    ax.text(ang[t_end], mag[t_end], 't = 0.2 s', color='red', fontsize=10)
    ax.text(ang[lim], mag[lim], f't = {limit} s', color='red', fontsize=10)
    if show_line:
        ax.plot(ang[:lim], mag[:lim], c='steelblue', ls='-', lw=0.5, zorder=-1)
    sc = ax.scatter(ang[:lim], mag[:lim], c=time[:lim],
                    cmap='viridis', marker='o', s=8, zorder=1)
    cb = plt.colorbar(sc, shrink=0.8)
    cb.set_label('Time (s)')
    fig.tight_layout()
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
        string = re.search('Teta', name)
        if string is not None:
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
