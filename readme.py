read_me = \
"""
IEEE New England 39-bus power system with 18% share of renewables.

This dictionary holds transient analysis results from applying
three different short-circuit types on main buses and half-points
of all transmission lines in the adapted IEEE New England 39-bus
power system with 18% share of renewables.

Total power production equals 6192 MW, of which 5075.8 MW is from
conventional power plants and 1116.13 MW is from the renewables,
where 742.43 MW is produced by the Wind farm and 373.7 MW by the
PV plant. Conventional power plants no. 8 and 10 were excluded
and replaced by the Wind farm and the PV plant. Aggregated Wind
and PV models were used for these plants.

Three short-circuits (SC) types are: three-phase (SC3), two-phase,
i.e. phase-to-phase fault between phases 'b' and 'c' (SC2), and a 
single-phase to ground fault in phase 'a' (SC1). Arc resistance
was neglected.

Dictionary keys have a form: 'SCX-BUSY', where X is a number that
identifies the type of short-circuit (3, 2, 1) and Y is an index
of the bus where the short-circuit has been applied. Short circuit
starts at 0.1 s and has a duration of 100 ms. Initial condition of
the power system was obtained from the load-flow analysis.

To each key is assigned a Pandas DataFrame which holds time-domain
signals from the transient analysis of that particular SC type and
location. Analysis was carried out in the EMTP-RV, using Parametric
Studio, with a 40 us time step and a 2 ms output resolution.

Signals from conventional plants are prefixed by the 'PowerPlant'
word, those from the Wind Farm have a 'DEV2' prefix and those from
the PV plant have a 'DEV3' prefix. Bus voltages (three phases) are
prefixed by the bus name. Fault Ride Through (FRT) signals for the
Wind farm and PV plant were recorded as well, where violations of
FRT criteria are identified by changing the indicator from 0 to 1.

PowerPlant signals variable names:
    '/Teta_1_SM1',   # rotor angle (deg)
    '/Omega_1_SM1',  # rotor speed
    '/PowerAng_SM1', # power angle
    '/Pe_SM1',       # electrical power (p.u)
    '/vd_SM1',  # d-axis stator voltage (p.u.)
    '/id_SM1',  # d-axis stator current (p.u.)
    '/Ef_SM1',  # EMF voltage (q-axis), (p.u.)
    '/vq_SM1',  # q-axis stator voltage (p.u.)
    '/iq_SM1',  # q-axis stator current (p.u.)

WindFarm signals variable names:
    'DEV2/P'   # active power (W)
    'DEV2/Q'   # reactive power (VAR)
    'DEV2/V0', 'DEV2I0'  # zero sequence voltage & current (V, A)
    'DEV2/V1', 'DEV2I1'  # direct sequence voltage & current (V, A)
    'DEV2/V2', 'DEV2I2'  # inverse sequence voltage & current (V, A)
    'WindFarm/PMSG_T_rotor'  # aggregated wind turbines torque
    'WindFarm/PMSG_w_rotor'  # aggregated wind turbines speed
    'WindFarm/FRT_flag'      # wind farm FRT indicator

PVPlant signals variable names:
    'DEV3/P'   # active power (W)
    'DEV3/Q'   # reactive power (VAR)
    'DEV3/V0', 'DEV3I0'  # zero sequence voltage & current (V, A)
    'DEV3/V1', 'DEV3I1'  # direct sequence voltage & current (V, A)
    'DEV3/V2', 'DEV3I2'  # inverse sequence voltage & current (V, A)
    'PVPlant/FRT_flag'   # PV plant FRT indicator

Bus signals variable names:
    '/Vrms_a'    # RMS voltage in phase a (p.u.)
    '/Vrms_b'    # RMS voltage in phase b (p.u.)
    '/Vrms_c'    # RMS voltage in phase c (p.u.)
    '/V1_mag'    # direct seq. voltage magnitude (p.u.)
    '/V1_phase'  # direct seq. voltage phase angle (deg)

Authors:
    Ivica Juric-Grgic, Ivan Krolo, Dino Lovric, Petar Sarajcev
    University of Split, FESB, Department of Power Engineering,
    R. Boskovica 32, HR-21000 Split, Croatia.
    Corresponding author: petar.sarajcev@fesb.hr

License: CC-BY
"""