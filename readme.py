read_me = \
"""
IEEE New England 39 bus power system with 18% share of renewables.

This dictionary holds 'key & value' pairs for the three different
short-circuit types --- three-phase (SC3), two-phase (SC2) and
single-phase (SC1) faults --- applied on main buses of the adapted
IEEE New England 39 bus power system with 18% share of renewables.
Total power production equals 6192 MW, of which 5075.8 MW is from
conventional power plants and 1116.13 MW is from the renewables,
where 742.43 MW is produced by the Wind farm and 373.7 MW by the
PV plant.

Each dict key has the form: 'SCX-BUSY', where X is a number that
identifies the type of short-circuit (3, 2, 1) and Y is a bus index.
To each key is assigned a Pandas DataFrame which holds time-domain
signals from the transient analysis of that particular SC type
and location. Analysis is carried out in EMTP-RV, using Parametric
Studio, with a 40 us time step and a 2 ms output resolution.

Signals from conventional generators are prefixed by the 'PowerPlant'
word, those from the Wind Farm have a 'DEV2' prefix and those from
the PV plant have a 'DEV3' prefix. Bus voltages (three phases) are
prefixed by the bus name. Fault Ride Through (FRT) signals for the
Wind farm and PV plant are recorded as well.

PowerPlant signals variable names:
    '/Teta_1_SM1',   # rotor angle
    '/Omega_1_SM1',  # rotor speed
    '/PowerAng_SM1', # power angle
    '/Pe_SM1',       # electrical power
    '/vd_SM1',  # d-axis stator voltage
    '/id_SM1',  # d-axis stator current
    '/Ef_SM1',  # EMF voltage (q-axis)
    '/vq_SM1',  # q-axis stator voltage
    '/iq_SM1',  # q-axis stator current

WindFarm signals variable names:
    'DEV2/P'   # active power
    'DEV2/Q'   # reactive power
    'DEV2/V0', 'DEV2I0'  # zero component voltage & current
    'DEV2/V1', 'DEV2I1'  # direct component voltage & current
    'DEV2/V2', 'DEV2I2'  # inverse component voltage & current
    'WindFarm/PMSG_T_rotor'  #  aggregated wind turbines torque
    'WindFarm/PMSG_w_rotor'  #  aggregated wind turbines speed
    'WindFarm/FRT_flag'      # wind farm FRT indicator

PVPlant signals variable names:
    'DEV3/P'   # active power
    'DEV3/Q'   # reactive power
    'DEV3/V0', 'DEV3I0'  # zero component voltage & current
    'DEV3/V1', 'DEV3I1'  # direct component voltage & current
    'DEV3/V2', 'DEV3I2'  # inverse component voltage & current
    'PVPlant/FRT_flag'   # PV plant FRT indicator

Authors:
Ivica Juric-Grgic, Ivan Krolo, Dino Lovric, Petar Sarajcev
University of Split, FESB, Department of Power Engineering,
R. Boskovica 32, HR-21000 Split, Croatia.
Corresponding author: petar.sarajcev@fesb.hr

License: CC-BY
"""