import re
import matplotlib.pylab as plt


def create_white_list(varnames, black, buses):
    """
    Create a `white_list` variable for extracting
    EMTP simulations signals.

    Parameters
    ----------
    varnames : list
        List of machine variable names that will
        be in the `white_list` variable.
    black : list
        List of indexes for the machines that are
        excluded from the simulation.
    buses : list
        List of bus indexes that have voltage
        measurements.
    
    returns
    -------
    white_list : list
        List with a variable names for the simulation.
    """
    # Form a "white list" of variable names.
    white_list = []
    # Bus voltages.
    for bus in buses:
        busa = 'BUS' + str(bus) + '/Vrms_a'
        white_list.append(busa)
        busb = 'BUS' + str(bus) + '/Vrms_b'
        white_list.append(busb)
        busc = 'BUS' + str(bus) + '/Vrms_c'
        white_list.append(busc)
    # Machine signals.
    for name in varnames:
        white_list.extend(
            ['PowerPlant_' + f'{i+1:02d}' + name 
            for i in range(10) 
            if i not in black]
        )
    return white_list


def plot_machine_signals(data, category):
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
    for name in data.columns:
        string = re.search(category, name)
        if string is not None:
            signal = data[name].values
            ax.plot(time, signal, ls='-', lw=1.5, label=name.split('/')[0])
    ax.legend(loc='upper left', frameon=True, fancybox=True, fontsize=8)
    ax.grid(which='major', axis='both')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel(category)
    fig.tight_layout()
    plt.show()
    return


def plot_machine_delta_signals(data):
    """
    Plot EMTP-RV simulation signals for the machines.

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame holding simulation signals.
    
    Returns
    -------
    Show matplotlib figure with plots of machine angles
    with regards to the slack machine.

    Notes
    -----
    This function is tailored for the machine signals,
    which contain 'PowerPlant' string in their name.
    DataFrame is exported from the simulation class.
    """
    time = data['time'].values
    fig, ax = plt.subplots(figsize=(6.5, 3.5))
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
                ax.plot(time, slack_signal-signal, ls='-', lw=1.5,
                        label=name.split('/')[0])
    ax.legend(loc='upper left', frameon=True, fancybox=True, fontsize=8)
    ax.grid(which='major', axis='both')
    ax.set_xlabel('Time (s)')
    fig.tight_layout()
    plt.show()
    return


def plot_bus_voltages_rms(data, bus):
    """
    Plot three-phase bus voltage RMS values.

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame holding simulation signals.
    bus : str
        Name of the bus, e.g. 'BUS2'.
    
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
    fig.tight_layout()
    plt.show()
    return