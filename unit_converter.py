"""
Convert between atomic units and SI

CODATA values from NIST are used

"""
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
        kg = unit('kg')
        coulomb = unit('C')
        joule_second = unit('J') * unit('s')
        farad_per_meter = unit('F') / unit('m')

        self.codata = codata

        #Define basic atomic units constants
        self.mass = scaled_unit('mass_au', *codata['electron mass'])
        self.charge = scaled_unit('charge_au', *codata['atomic unit of charge'])
        self.electrostatic_constant = named_unit('eps0_au', ['F'], ['m'],
                codata['atomic unit of permittivity'][1])
        self.hbar = named_unit('action_au', ['J'], ['s'],
                codata['atomic unit of action'][1])
        self.alpha = codata['inverse fine-structure constant']

        #Derived units
        self.length = scaled_unit('length_au', 'm',
                (self.electrostatic_constant * self.hbar**2 /
                    (self.mass * self.charge**2)).squeeze())
        self.energy = scaled_unit('energy_au', 'J',
                (self.hbar**2 / (self.mass * self.length**2)).squeeze())

        #Other units
        self.electron_volt = scaled_unit('eV', *codata['electron volt'])


    def eVToAU(self):
        """Scaling factor giving 1 eV in atomic units of energy
        """
        return codata['hartree energy in eV']

