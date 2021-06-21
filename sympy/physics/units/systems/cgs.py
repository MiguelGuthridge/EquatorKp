from sympy import sqrt, S
from sympy.physics.units import UnitSystem, centimeter, gram, second, coulomb, charge, speed_of_light, current, mass, \
    length, voltage, magnetic_density, magnetic_flux
from sympy.physics.units.definitions import coulombs_constant
from sympy.physics.units.definitions.unit_definitions import statcoulomb, statampere, statvolt, volt, tesla, gauss, \
    weber, maxwell, debye, oersted, ohm, farad, henry, erg, ampere, coulomb_constant
from sympy.physics.units.systems.mks import dimsys_length_weight_time

One = S.One

dimsys_cgs = dimsys_length_weight_time.extend(
    [],
    new_dim_deps=dict(
        # Dimensional dependencies for derived dimensions
        impedance=dict(time=1, length=-1),
        conductance=dict(time=-1, length=1),
        capacitance=dict(length=1),
        inductance=dict(time=2, length=-1),
        charge=dict(mass=S.Half, length=S(3)/2, time=-1),
        current=dict(mass=One/2, length=3*One/2, time=-2),
        voltage=dict(length=-One/2, mass=One/2, time=-1),
        magnetic_density=dict(length=-One/2, mass=One/2, time=-1),
        magnetic_flux=dict(length=3*One/2, mass=One/2, time=-1),
    )
)

cgs_gauss = UnitSystem(
    base_units=[centimeter, gram, second],
    units=[],
    name="cgs_gauss",
    dimension_system=dimsys_cgs)


cgs_gauss.set_quantity_scale_factor(coulombs_constant, 1)

cgs_gauss.set_quantity_dimension(statcoulomb, charge)
cgs_gauss.set_quantity_scale_factor(statcoulomb, centimeter**(S(3)/2)*gram**(S(1)/2)/second)

cgs_gauss.set_quantity_dimension(coulomb, charge)

cgs_gauss.set_quantity_dimension(statampere, current)
cgs_gauss.set_quantity_scale_factor(statampere, statcoulomb/second)

cgs_gauss.set_quantity_dimension(statvolt, voltage)
cgs_gauss.set_quantity_scale_factor(statvolt, erg/statcoulomb)

cgs_gauss.set_quantity_dimension(volt, voltage)

cgs_gauss.set_quantity_dimension(gauss, magnetic_density)
cgs_gauss.set_quantity_scale_factor(gauss, sqrt(gram/centimeter)/second)

cgs_gauss.set_quantity_dimension(tesla, magnetic_density)

cgs_gauss.set_quantity_dimension(maxwell, magnetic_flux)
cgs_gauss.set_quantity_scale_factor(maxwell, sqrt(centimeter**3*gram)/second)

# SI units expressed in CGS-gaussian units:
cgs_gauss.set_quantity_scale_factor(coulomb, speed_of_light*statcoulomb/10)
cgs_gauss.set_quantity_scale_factor(ampere, speed_of_light*statcoulomb/second/10)
cgs_gauss.set_quantity_scale_factor(volt, speed_of_light*statvolt/10**6)
cgs_gauss.set_quantity_scale_factor(weber, 10**8*maxwell)
cgs_gauss.set_quantity_scale_factor(tesla, 10**4*gauss)
cgs_gauss.set_quantity_scale_factor(debye, One/10**18*statcoulomb*centimeter)
cgs_gauss.set_quantity_scale_factor(oersted, sqrt(gram/centimeter)/second)
cgs_gauss.set_quantity_scale_factor(ohm, 10**9/speed_of_light**2*second/centimeter)
cgs_gauss.set_quantity_scale_factor(farad, One/10**9*speed_of_light**2*centimeter)
cgs_gauss.set_quantity_scale_factor(henry, 10**9/speed_of_light**2/centimeter*second**2)

# Coulomb's constant:
cgs_gauss.set_quantity_dimension(coulomb_constant, 1)
cgs_gauss.set_quantity_scale_factor(coulomb_constant, 1)

__all__ = [
    'ohm', 'tesla', 'maxwell', 'speed_of_light', 'volt', 'second', 'voltage',
    'debye', 'dimsys_length_weight_time', 'centimeter', 'coulomb_constant',
    'farad', 'sqrt', 'UnitSystem', 'current', 'charge', 'weber', 'gram',
    'statcoulomb', 'gauss', 'S', 'statvolt', 'oersted', 'statampere',
    'dimsys_cgs', 'coulomb', 'magnetic_density', 'magnetic_flux', 'One',
    'length', 'erg', 'mass', 'coulombs_constant', 'henry', 'ampere',
    'cgs_gauss',
]
