"""
Convert between atomic units and SI

CODATA values from NIST are used

"""
from units import unit

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
                codata[key] = (val, unit)

    return codata


class ConstantsAU:
    def __init__(self, codata):
        self.mass = codata['electron mass']
