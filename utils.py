import re
import matplotlib.pylab as plt


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
