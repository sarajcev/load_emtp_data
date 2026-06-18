read_me = \
"""
IEEE New England 39-bus power system.

This dictionary holds transient analysis results from applying
three different short-circuit types on main buses and half-points
of all transmission lines in the IEEE New England 39-bus power 
system with and without the inclusion of renewable sources.

Variant V0 is a classical IEEE New England 39-bus power system
with no renewables.

Variant V1 is an adapted IEEE New England 39-bus power system 
with a 20% share of renewables. Total power production in this
system equals 6187.82 MW, of which 1242.86 MW (20.08%) is from 
the renewables, where 742.43 MW (12%) is produced by the Wind 
farm (750 MW installed capacity) and 500.43 MW (8.08%) by the 
PV plant (500 MW installed capacity). Conventional power plants 
G5 and G8 were excluded and replaced by the PV plant and wind 
farm (WF), respectively. Aggregated Wind and PV models were used.

Variant V2 is an adapted IEEE New England 39-bus power system 
with a 40% share of renewables. Conventional power plants G3, G5,
G8 and G9 were excluded and replaced by renewables. Two PV plants 
and two wind farms were connected, where PV plant replaces G5, PV2 
plant replaces G5, while wind farm WF replaces G8 and WF2 replaces 
G9. Total power production in this system equals 6176.7 MW, of 
which 2485.72 MW (40.24%) is from the renewables, where 1484.86 MW 
(24.04%) comes from wind farms (2x750 MW installed capacity) and 
1000.86 MW (16.20%) is from the PV plants (2x500 MW installed 
capacity). Aggregated Wind and PV models were used. 

Three short-circuits (SC) types are: three-phase (SC3), two-phase,
i.e. phase-to-phase fault between phases 'a' and 'b' (SC2), and a 
single-phase to ground fault in phase 'a' (SC1). Arc resistance
was neglected.

Dictionary keys have a form: 'SCX-BUSY', where X is a number that
identifies the type of short-circuit (3, 2, 1) and Y is an index
of the bus where the short-circuit has been applied. Short circuit
starts at 0.1 s and has a duration as indicated in the file name
(i.e. 100 ms or 300 ms). Initial condition of the power system was 
obtained from the load flow analysis.

To each key is assigned a Pandas DataFrame which holds time-domain
signals from the transient analysis of that particular SC type and
location. Analysis was carried out in the EMTP-RV, using Parametric
Studio, with a 40 us time step and a 2 ms output resolution.

Signals from conventional plants are prefixed by the 'PowerPlant'
word. In variants where renewables are present, signals from the 
Wind Farm have a 'WF' prefix and those from the PV plant have a 
'PV' prefix. Bus voltages (three phases) are prefixed by the BUS 
name. Fault Ride Through (FRT) signals for the Wind farm and PV 
plant were recorded as well (when they are present in the system), 
where violations of FRT criteria are identified by changing the 
indicator from 0 to 1. When two PV plants are present, the second
one is prefixed with PV2; the same is for wind farms, where the
second one is then prefixed by WF2.

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

WindFarm (WF) signals variable names:
    '/P'   # active power (W)
    '/Q'   # reactive power (VAR)
    '/V0', 'WF/I0'  # zero sequence voltage & current (V, A)
    '/V1', 'WF/I1'  # direct sequence voltage & current (V, A)
    '/V2', 'WF/I2'  # inverse sequence voltage & current (V, A)
    '/PMSG_T_rotor'  # aggregated wind turbines torque
    '/PMSG_w_rotor'  # aggregated wind turbines speed
    '/FRT_flag'      # wind farm FRT indicator

PVPlant (PV) signals variable names:
    '/P'   # active power (W)
    '/Q'   # reactive power (VAR)
    '/V0', 'PV/I0'  # zero sequence voltage & current (V, A)
    '/V1', 'PV/I1'  # direct sequence voltage & current (V, A)
    '/V2', 'PV/I2'  # inverse sequence voltage & current (V, A)
    '/FRT_flag'     # PV plant FRT indicator

BUS signals variable names:
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