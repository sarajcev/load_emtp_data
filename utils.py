import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import (
    RandomizedSearchCV,
    StratifiedKFold,
    cross_val_score,
)
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    balanced_accuracy_score,
    roc_auc_score,
    average_precision_score,
    precision_recall_curve,
    auc,
)


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
    if variant in ['V1', 'V2', 'V3', 'V4', 'V5']:
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
    
    if variant in ['V2', 'V3', 'V4', 'V5']:
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
    
    if variant in ['V4', 'V5']:
        # This is a variant with 60% share of renewables.
        # PV plant 3 (PV3) signals (DEV6).
        # This PV replaces machine G10.
        white_list.extend(['DEV6/P', 'DEV6/Q'])
        white_list.extend(['DEV6/V0', 'DEV6/V1', 'DEV6/V2'])
        white_list.extend(['DEV6/I0', 'DEV6/I1', 'DEV6/I2'])
        white_list.append(
            'WECC_PVPark_3/Converter_control/Control/GridControl_DLL/FRT_flag'
        )

    if variant == 'V5':
        # This is a variant with 80% share of renewables.
        # PV plant 4 (PV4) signals (DEV7).
        white_list.extend(['DEV7/P', 'DEV7/Q'])
        white_list.extend(['DEV7/V0', 'DEV7/V1', 'DEV7/V2'])
        white_list.extend(['DEV7/I0', 'DEV7/I1', 'DEV7/I2'])
        white_list.append(
            'WECC_PVPark_4/Converter_control/Control/GridControl_DLL/FRT_flag'
        )
        # Wind farm 3 (WF3) signals (DEV8).
        white_list.extend(['DEV8/P', 'DEV8/Q'])
        white_list.extend(['DEV8/V0', 'DEV8/V1', 'DEV8/V2'])
        white_list.extend(['DEV8/I0', 'DEV8/I1', 'DEV8/I2'])
        white_list.append('FFC_WP3/Wind_Turbine/PMSG_T_rotor')
        white_list.append('FFC_WP3/Wind_Turbine/PMSG_w_rotor')
        white_list.append('FFC_WP3/Converter_control/Control/Grid_Ctrl/FRT_flag')

    return white_list


def filter_signal(signal, filter_type='median', window=21):
    """
    Filter the time-domain signal.

    A two-step signal filtering. First a moving average or
    a moving median filter is applied to the raw data. Then,
    a Savitzky-Golay filter is applied on top of the filtered
    data (using the same window size) to further smooth the
    final output signal.

    Parameters
    ----------
    signal : array-like
        Array (1D) holding the raw signal data points.
    filter_type : str, default='median'
        A type of filter to apply, either `mean` or `median`.
    window : int, default=21
        Window length in sample points for the filter.

    Returns
    -------
    yhat : array
        Array holding the filtered signal data points. It
        has the same dimension as the original 1D array.
    """
    from scipy.ndimage import uniform_filter1d as mean_filter
    from scipy.signal import medfilt as median_filter
    from scipy.signal import savgol_filter

    # Filter's window length uses an odd number of sample points.
    if window % 2 == 0:
        window += 1

    if filter_type == 'median':
        # Moving median filter.
        sf = median_filter(signal, kernel_size=window)
    elif filter_type == 'mean':
        # Moving average (MA) filter.
        sf = mean_filter(signal, size=window)
    else:
        raise NotImplementedError(f'Filter type: {filter_type} is not recognized.')

    # Smooth the resulting signal with a Savitzky-Golay filter.
    yhat = savgol_filter(sf, window_length=window, polyorder=3)

    return yhat


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
    ax.legend(loc='best', frameon=True, fancybox=True, fontsize=8)
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
    ax.legend(loc='best', frameon=True, fancybox=True, fontsize=8)
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


def plot_frequency(data, list_of_nodes, raw=True, xlim=None,
                   save=False, **kwargs):
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
    raw : bool, default=True
        Indicator for filtering the signal. If raw=True,
        original raw signal is plotted; otherwise, if
        raw=False, filtered signal is plotted.
    save : bool, default=False
        Indicator for saving figure to disk.
    **kwargs : dict
        Dictionary of keyword arguments for filtering
        signal.

    Returns
    -------
    Show matplotlib figure.
    """
    time = data['time']

    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    for k, node in enumerate(list_of_nodes):
        bus = 'BUS' + str(node)
        if raw:
            # Use original data.
            signal = data[bus + '/Freq'].values
        else:
            # Filter signal.
            signal = filter_signal(data[bus + '/Freq'].values, **kwargs)
        if k == 0:
            # First node is emphasized.
            ax.plot(time, signal, ls='-', lw=2, c='dimgrey',
                    label=bus)
        else:
            ax.plot(time, signal, ls='-', lw=1, label=bus)
    ax.legend(loc='best', frameon=True, fancybox=True, fontsize=9)
    ax.grid(which='major', axis='both')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    if xlim is not None:
        ax.set_xlim(left=0, right=xlim)
    fig.tight_layout()
    if save:
        plt.savefig('frequency.pdf')
    plt.show()

    return


def plot_bus_voltages_rms(data, bus, xlim=None, title=False, save=False):
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
    title : bool, default=False
        Indicator for showing plot title.
    save : bool, default=False
        Indicator for saving figure to disk.

    Returns
    -------
    Show matplotlib figure.
    """
    time = data['time'].values
    mask = data.index[10:]

    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    if title:
        ax.set_title(f'RMS voltage at: {bus}', fontsize=9)
    ax.plot(time[mask], data[bus+'/Vrms_a'][mask], ls='-', lw=1.5, label='Vrms_a')
    ax.plot(time[mask], data[bus+'/Vrms_b'][mask], ls='-', lw=1.5, label='Vrms_b')
    ax.plot(time[mask], data[bus+'/Vrms_c'][mask], ls='-', lw=1.5, label='Vrms_c')
    ax.plot(time[mask], data[bus+'/V1_mag'][mask], ls="--", lw=1.5,
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
    mask = data.index[10:]

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
    ax_top.plot(data['time'][mask], data[bus + '/Vrms_a'][mask], label='phase a')
    ax_top.plot(data['time'][mask], data[bus + '/Vrms_b'][mask], label='phase b')
    ax_top.plot(data['time'][mask], data[bus + '/Vrms_c'][mask], label='phase c')
    ax_top.plot(data['time'][mask], mag[mask],
                ls='--', c='dimgrey', label='dir. comp.')
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
    fig.tight_layout()

    if save:
        plt.savefig(key + ':' + bus + '.pdf')
    plt.show()

    return


def plot_voltages_heatmap(data, key, phase='V1_mag', limit=None, save=False):
    """ Bus voltages as a heatmap.

    Display of a time-evolution of voltage magnitudes,
    in per-unit values, for all network main buses,
    organized as a heatmap. Phase values or direct-sequence
    voltage magnitudes can be selected for a display.

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame holding simulation signals.
    key : str
        String identifying dictionary key with information
        on type and location of the short-circuit. Then,
        data[key] is a pandas DataFrame with simulation signals
        for that particular case.
    phase : str, default='V1_mag'
        String identifying which phase will be used for plotting,
        "Vrms_a", "Vrms_b", "Vrms_c", for the RMS voltage in phase
        "a", "b", "c", or "V1_mag" for the direct-sequence voltage.
    limit : float or None, default=None
        Time limit of the voltage display in seconds.
    save : bool, default=False
        Indicator for saving the figure to external file.

    Returns
    -------
    Maplotlib plot with a heatmap display of bus voltages.
    """
    data = data[key]
    time = data['time'].values

    if limit is None:
        lim = -1
    else:
        # Index of the time limit for plotting.
        dt = time[1] - time[0]
        lim = int(limit/dt) + 1

    bus_names = []
    for column in data.columns:
        if 'BUS' in column:
            bus_names.append(column)
    signal_names = [bus for bus in bus_names if phase in bus]
    voltages = np.asarray([data[bus].values for bus in signal_names])
    buses = [name.split('/')[0] for name in signal_names]

    fig, ax = plt.subplots(figsize=(6.8, 5.5), constrained_layout=True)
    #ax.set_title(key+':'+phase, fontsize=10)
    im = ax.imshow(
        voltages[:, :lim],
        aspect='auto',
        origin='lower',
        extent=(time[0], time[lim], 0, voltages.shape[0]-1),
        cmap='viridis',
    )
    ax.set_yticks(np.arange(len(buses)))
    ax.set_yticklabels(buses, fontsize=8)
    ax.set_xlabel('Time (s)')
    ax.grid(axis='y', which='major', linewidth=0.2)
    cbar = fig.colorbar(im, ax=ax, pad=0.01)
    cbar.set_label('RMS voltage magnitude (pu)')
    if save:
        plt.savefig(key+'-heatmap' + '.pdf')
    plt.show()

    return


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
    from matplotlib.gridspec import GridSpec

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
    from matplotlib.gridspec import GridSpec

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


def frt_stability(data, THR=1000):
    """
    Transient stability from the FRT signal.

    If any FRT signal has value 1 persistently it is considered
    that power plant is unstable. A cumulative sum of FRT signal
    values is computed and compared aginst a threshold (THR). If
    it exceeds the threshold that indicates unstable power plant
    operation and a global FRT stability flag of 1 is returned.
    Otherwise, if the cumulative sum does not exceed the threshold,
    power plant is considered stable and a global FRT stability
    index of 0 is returned. All RES power plants are tested, and
    it is sufficient that only one of them is unstable for the
    global FRT stability index to become 1. If there is no RES,
    then global FRT stability index will be 0.

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame holding simulation signals.
    THR : ind, default=1000
        Threshold for FRT stability.
    Returns
    -------
    frt : int
        Stability index: 0 - stable case; 1 - unstable case
    """
    frt = 0
    for name in data.columns:
        if 'FRT' in name:
            signal = data[name].values
            # If FRT flag is persistent for a long time.
            if signal.sum() >= THR:
                # Unstable case.
                frt = 1
                break

    return frt


def features_engineering(path):
    """
    Engineer features from the voltage signals and targets
    from the transient stability index (TSI) analysis, where
    TSI is determined from rotor angle deviations.

    Parameters
    ----------
    path : pathlib.Path
        A pathlib constructed directory path where the pickle file is
        stored, including the name of that file. A pickle file stores
        the simulation data for a single variant.

    Returns
    -------
    features_targets : pd.DataFrame
        Features and targets for a single variant.
    """
    with open(file=path, mode='rb') as fp:
        data_all = pickle.load(fp)

    # Extract SC duration.
    file = str(path).split('/')[-1]
    sc_duration = file.split('-')[1][1:4]

    selected_keys = []
    if sc_duration == '100':
        # Extract all data.
        selected_keys = [key for key in data_all.keys() if key != 'README']
    elif sc_duration == '300':
        # Extract data for middle-points only. We don't consider
        # main bus faults lasting 300 ms, as these are too severe.
        middle_points = [f'BUS{point}' for point in range(40, 73)]
        for key in data_all.keys():
            if key == 'README':
                continue
            _, bus = key.split('-')
            if bus in middle_points:
                selected_keys.append(key)
    else:
        raise ValueError()

    # Engineer features and targets.
    features = {}
    targets = {}
    for key in selected_keys:
        data = data_all[key]
        features[key] = []
        for col in data.columns:
            if 'V1_mag' in col and 'BUS39' not in col:
                signal = data[col]
                # Voltage drop (onset time).
                v1 = signal.loc[data['time'] == 0.540].values[0].round(3)
                # Voltage recovery (clearing time).
                if sc_duration == '100':
                    v2 = signal.loc[data['time'] == 0.640].values[0].round(3)
                elif sc_duration == '300':
                    v2 = signal.loc[data['time'] == 0.840].values[0].round(3)
                else:
                    raise ValueError()
                # Add scenario features.
                features[key].extend([v1, v2])
        # Add short-circuit duration as a feature.
        #features[key].append(float(sc_duration) / 1000.)  # seconds

        # TSI analysis.
        tsi = tsi_from_angle(data)
        # FRT analysis.
        frt = frt_stability(data)
        # TSI OR FRT.
        stability = np.logical_or(tsi, frt)
        # Assign targets.
        targets[key] = stability

    # DataFrame with features and targets.
    features_targets = pd.DataFrame.from_dict(features, orient='index')
    size = len(features_targets.columns)
    # Rename features columns.
    features_targets.columns = [f'F{i+1}' for i in range(size)]
    # Add targets column.
    features_targets['TSI'] = pd.Series(targets)

    return features_targets


def train_extra_trees_classifier(
    df,
    n_iter=100,
    cv=3,
    scoring='balanced_accuracy',
    random_state=42,
    n_jobs=-1,
):
    """
    Train an Extra Trees binary classifier with class-weight balancing.

    The last DataFrame column is treated as the target; all preceding columns
    are treated as features.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame holding features and targets (as a last column).
    n_iter : int, default=100
        Number of iterations for the RandomSearch used for
        hyperparameters tuning.
    cv : int, default=3
        Number of folds for the k-fold stratified cross-validation.
    scoring : str, default='balanced_accuracy'
        String that defines sklearn scoring metric.
    random_state : int, default=42
        Random seed used during classifier training, both for the
        stratified k-fold and random search.
    n_jobs : int, default=-1
        Number of cores for parallel processing. Default value
        uses all cores.

    Returns
    -------
    ExtraTreesClassifier
        The best fitted classifier from the randomized search.
    """
    from scipy.stats import randint

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    classifier = ExtraTreesClassifier(
        class_weight='balanced',
        random_state=random_state,
        n_jobs=n_jobs,
    )

    param_distributions = {
        'n_estimators': randint(200, 1000),
        'max_depth': [None, 5, 10, 20, 30, 50],
        'min_samples_split': randint(2, 20),
        'min_samples_leaf': randint(1, 10),
        'max_features': ['sqrt', 'log2', None, 0.5, 0.75, 1.0],
        'criterion': ['gini', 'entropy', 'log_loss'],
        'bootstrap': [False, True],
    }

    cv_strategy = StratifiedKFold(n_splits=cv, shuffle=True,
                                  random_state=random_state)

    search = RandomizedSearchCV(
        estimator=classifier,
        param_distributions=param_distributions,
        n_iter=n_iter,
        scoring=scoring,
        cv=cv_strategy,
        refit=True,
        random_state=random_state,
        n_jobs=n_jobs,
        verbose=1,
    )

    search.fit(X, y)

    return search.best_estimator_


def calibrate_model(base_model, df):
    """
    Calibrate binary classification model.

    Parameters
    ----------
    base_model : sklearn model
        Base model instance.
    df : pd.DataFrame
        DataFrame holding calibration set.

    Returns
    -------
    model : sklearn model
        Calibrated sklearn model instance.
    """
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    calibrated_model = CalibratedClassifierCV(
        estimator=base_model,
        method='sigmoid',
        cv=3
    )
    calibrated_model.fit(X, y)

    return calibrated_model


def tune_model_threshold(model, df, scoring='roc_auc'):
    """
    Tune the classifier threshold on a validation set.

    Parameters
    ----------
    model : sklearn model
        Base model instance.
    df : pd.DataFrame
        DataFrame holding calibration set, where last column
        holds targets.
    scoring : str, default='roc_auc'
        String for the sklearn scoring metric.

    Returns
    -------
    threshold : float
        Best model threshold from the validation set.
    """
    from sklearn.model_selection import TunedThresholdClassifierCV

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    tuned_clf = TunedThresholdClassifierCV(
        model,
        scoring=scoring,
        response_method='predict_proba',
        n_jobs=-1
    )
    tuned_clf.fit(X, y)

    return tuned_clf.best_threshold_


def corrupt_measurements(data, bus, no_samples):
    """ Corrupting data measurements.

    Simulating random malfunctioning PMU units.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing data features.
    bus : int
        Integer bus number.
    no_samples : int
        Number of samples to simulate.

    Returns
    -------
    data : pd.DataFrame
        DataFrame containing corrupted data.
    """
    # Simulating measurement errors.
    ids_rand = data.sample(n=no_samples, replace=False).index
    f1, f2 = f'F{2*bus-1}', f'F{2*bus}'  # locate features
    # Replace selected measurement (features) with NaN values.
    data.loc[ids_rand, [f1, f2]] = None

    return data


def precision_recall_tradeoff(thresholds, precision, recall, save_fig=False):
    """
    Plot precision-recall tradeoff curves.

    Plot a precision and recall curves of the binary classifier,
    as a function of the decision-making threshold values.

    Parameters
    ----------
    thresholds : array
        Array holding threshold levels.
    precision : array
        Array holding classifier precisions at threshold levels.
    recall : array
        Array holding classifier recalls at threshold levels.
    save_fig: bool, default=False
        Indicator for saving the figure as external file.

    Returns
    -------
    Display matplotlib figure.
    """
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(thresholds, precision[:-1], lw=2, label='Precision')
    ax.plot(thresholds, recall[:-1], lw=2, label='Recall')
    ax.set_xlabel('Decision thresholds')
    ax.set_ylabel('Precision / Recall')
    ax.legend(loc='lower right')
    ax.set_ylim(ymin=0.1)
    ax.grid(which='major', axis='both')
    fig.tight_layout()
    if save_fig:
        fig.savefig('precis-recall.pdf')
    plt.show()


def roc_curve(y_true, y_score, save_fig=False):
    """
    Plot Receiver Operating Characteritic (ROC).

    Parameters
    ----------
    y_true : array
        Array holding true labels.
    y_score : array
        Array holding probability estimates of the positive class.
    save_fig : bool, default=False
        A flag for saving figure to disk (True/False).

    Returns
    -------
    Matplotlib figure.
    """
    from sklearn.metrics import RocCurveDisplay

    fig, ax = plt.subplots(figsize=(5, 5))
    RocCurveDisplay.from_predictions(y_true, y_score, pos_label=1, ax=ax)
    ax.grid(which='major', axis='both')
    fig.tight_layout()
    if save_fig:
        plt.savefig('roc_curve.pdf')
    plt.show()


def evaluate_extra_trees_classifier(model, test_df, thr=None, **kwargs):
    """
    Compare model predictions with true labels in test_df.

    Assumes the last column of test_df is the target and all preceding columns
    are features.

    Parameters
    ----------
    model : sklearn
        Trained model instance.
    test_df : pd.DataFrame
        Dataframe holding features and targets (as a last column).
    thr : floar or None, default=None
        Threshold of the classifier for making predictions.
    **kwargs : dict
        Additional keyword arguments packed in a dictionary.

    Returns
    -------
    Evaluation metrics.
        Function plots precision-recall curve, prints confusion matrix,
        classification report, ROC AUC, PR AUC, balanced accuracy,
        and returns a DataFrame with row-level comparison for further
        inspection.
    """
    X_test = test_df.iloc[:, :-1]
    y_test = test_df.iloc[:, -1]

    # Model predictions.
    probabilities = model.predict_proba(X_test)[:, 1]
    if thr is None:
        predictions = model.predict(X_test)
    else:
        predictions = (probabilities >= thr).astype(int)

    # Average precision.
    pr_auc_average = average_precision_score(y_test, probabilities)

    # Precision, recall, and thresholds.
    precision, recall, thresholds = precision_recall_curve(y_test, probabilities)
    # Plot precision-recall curves.
    precision_recall_tradeoff(thresholds, precision, recall, **kwargs)
    # Area under the precision-recall curve.
    pr_auc = auc(recall, precision)

    # Receiver operating characteristic (ROC).
    #roc_curve(y_test, probabilities)

    print('Confusion matrix:')
    print(confusion_matrix(y_test, predictions, labels=[0, 1]))

    print('\nClassification report:')
    print(classification_report(y_test, predictions, digits=3,
                                zero_division=0.0))

    print(f'Balanced accuracy: {balanced_accuracy_score(y_test, predictions):.4f}')
    print(f'ROC AUC: {roc_auc_score(y_test, probabilities):.4f}')
    print(f'PR AUC (average precision): {pr_auc_average:.4f}')
    print(f'PR AUC: {pr_auc:.4f}')

    # Cross-validated ROC AUC score.
    roc_auc = cross_val_score(model, X_test, y_test, scoring='roc_auc',
                              cv=3, n_jobs=-1)
    print(f'ROC AUC (3-fold CV) Score: {roc_auc.mean():.4f} +/- {roc_auc.std():.4f}')

    # Return row-level comparison for further inspection.
    comparison = test_df.copy()
    comparison['predicted'] = predictions
    comparison['prob_class_1'] = probabilities
    comparison['is_correct'] = predictions == y_test.to_numpy()

    return comparison