"""
Convert between atomic units and SI

CODATA values from NIST are used

"""
from math import pi, sqrt
from units import unit, scaled_unit, named_unit


def ParseCODATA(filename):
    """
    Parse CODATA ASCII file and return dict of the constants and their
    value in SI units

    >>> C = ParseCODATA("codata.txt")
    >>> C['electron mass']
    (9.10938291e-31, 'kg')

    """

    codata = dict()

    #For now we assume fixed-field width
    with open(filename, "r") as f:
        for idx, line in enumerate(f):
            if (idx > 10):
                key = line[:55].strip()
                rawVal = line[55:76].replace(" ", "").replace("...","").strip()
                val = float(rawVal)
                unit = line[99:].strip()
                codata[key] = (unit, val)

    return codata

class ConstantsAU:
    """Simple class defining the atomic unit constants values (in SI),
    and supplying some common conversion factors.

    """

    def __init__(self, codata):
        #SI units
        self.si_mass = unit('kg')
        self.si_charge = unit('C')
        self.si_energy = unit('J')
        self.si_action = unit('J') * unit('s')
        self.si_time = unit('s')
        self.si_frequency = unit('Hz')
        #farad_per_meter = unit('F') / unit('m')

        self.codata = codata

        #Define basic atomic units constants
        self.mass = scaled_unit('mass_au', *codata['electron mass'])
        self.charge = scaled_unit('charge_au', *codata['atomic unit of charge'])
        self.electrostatic_constant = named_unit('eps0_au', ['F'], ['m'],
                codata['atomic unit of permittivity'][1])
        self.hbar = named_unit('action_au', ['J'], ['s'],
                codata['atomic unit of action'][1])
        self.alpha = codata['fine-structure constant'][1]
        self.time = scaled_unit('time_au', *codata['atomic unit of time'])

        #Derived units
        self.speed = scaled_unit("speed_au", *codata['atomic unit of velocity'])
        self.lightspeed = self.speed(codata['speed of light in vacuum'][1])
        self.length = scaled_unit('length_au', 'm',
                (self.electrostatic_constant * self.hbar**2 /
                    (self.mass * self.charge**2)).squeeze())
        self.energy = scaled_unit('energy_au', 'J',
                (self.hbar**2 / (self.mass * self.length**2)).squeeze())
        self.electric_field_strength = named_unit('efield_au', ['V'], ['m'],
            (self.charge / (self.electrostatic_constant * self.length**2)).squeeze())
        self.frequency = scaled_unit('frequency_au', 'Hz', 1.0/self.time.squeeze())

        #Other units
        self.electron_volt = scaled_unit('eV', *codata['electron volt'])
        self.femtosecond = scaled_unit('fs', 's', self.si_time.squeeze()*1e-15)


#    def ConvertEnergyEVToAU(self, energy_eV):
#        """Convert energy from electron volts to atomic units of energy
#        """
#        return energy_eV * self.codata['Hartree energy in eV'][1]


    def ConvertElectricFieldAtomicFromIntensitySI(self, intensity):
        """
        Intensity [W/cm**2] -> E-field strength [a.u.]

        Relation obtained from time-averaging over one cycle,

          E0 = sqrt( (2 <I>) / (eps0 * c) )

        """
        watt_per_squarecm = unit('W') / unit('cm')**2
        val = sqrt(2.0 * intensity / (self.electrostatic_constant.squeeze() /
                (4*pi) * self.lightspeed))
        return val * 100.0 / self.electric_field_strength.squeeze()


    def ConvertIntensitySIFromElectricFieldAtomic(self, efield):
        """
        Intensity [W/cm**2] <- E-field strength [a.u.]

          I = 0.5 * eps0 * c * E0**2

        """
        val = 0.5 * self.electrostatic_constant.squeeze() / (4*pi) * \
            self.lightspeed * efield**2
        return val / 100.0**2 * self.electric_field_strength.squeeze()**2


