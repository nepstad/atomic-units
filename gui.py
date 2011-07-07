import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import units.exception
from unit_converter import ConstantsAU, ParseCODATA

class In_UNITS:
    WATT_PER_SQUARECM = 0

class UnitsForm(QWidget):

    def __init__(self, parent=None):
        super(UnitsForm, self).__init__(parent=parent)

        #Define In units that we know
        au = ConstantsAU(ParseCODATA("codata.txt"))
        self.convertDict = {
                #unicode('W/cm**2 -> E-field (a.u.)'): au.ConvertElectricFieldAtomicFromIntensityIn,
                unicode('eV'): au.electron_volt,
                unicode('(a.u.) energy'): au.energy,
                unicode('(a.u.) mass'): au.mass,
                unicode('(SI) kg'): au.si_mass,
                unicode('(SI) J'): au.si_energy,
        }
        convertKeys = sorted(self.convertDict.keys(), key=lambda s: s.lower())

        #Set up input widgets
        self.formIn = QLineEdit()
        self.formOut = QLineEdit()

        #Set up input widgets
        self.unitTypeIn = QComboBox()
        self.unitTypeIn.addItems(convertKeys)
        self.unitTypeOut = QComboBox()
        self.generateOutputUnits(convertKeys[0])

        #Info widgets
        self.atomicUnitsList = QLabel()
        self.atomicUnitsList.setText("<b>Basic atomic units</b> <br> mass: %s" %
                "".join(["%s " % el for el in reversed(au.codata['atomic unit of mass'])]))

        #Create widget layout
        grid = QGridLayout()
        grid.addWidget(self.formIn, 0, 0)
        grid.addWidget(self.unitTypeIn, 0, 1)
        grid.addWidget(self.formOut, 1, 0)
        grid.addWidget(self.unitTypeOut, 1, 1)
        grid.addWidget(self.atomicUnitsList, 2, 0, 1, -1)
        self.setLayout(grid)

        #Define form behavior
        self.connect(self.formIn, SIGNAL("returnPressed()"), self.computeUnit)
        self.connect(self.unitTypeIn, SIGNAL("currentIndexChanged(QString)"), self.generateOutputUnits)

        #Set the title
        self.setWindowTitle("Atomic Units")

    def computeUnit(self):
        #Get input In value
        try:
            inputVal = float(unicode(self.formIn.text()))
        except:
            inputVal = float("NaN")

        #Get input unit
        inputUnit = unicode(self.unitTypeIn.currentText())

        #Get output unit
        outputUnit = unicode(self.unitTypeOut.currentText())

        #Calculate value in a.u.
        f = self.convertDict[inputUnit]
        g = self.convertDict[outputUnit]
        try:
            outputVal = g(f(inputVal))
        except units.exception.IncompatibleUnitsError:
            self.errMsg = QMessageBox()
            self.errMsg.setText("Incompatible units")
            self.errMsg.setWindowTitle("Error!")
            self.errMsg.show()
        else:
            self.formOut.setText("%g" % outputVal)


    def generateOutputUnits(self, newItem):
        """
        Generate list of compatible output units based on input units

        newItem: (string) name of input unit

        """
        #Get input unit
        inUnit = self.convertDict[unicode(newItem)]

        #Filter list of units for compatible output units
        outputUnitNames = filter(
                lambda x: x[1].canonical() == inUnit.canonical(),
                self.convertDict.iteritems())
        outputUnits = sorted(dict(outputUnitNames).keys(), key=lambda s: s.lower())

        #Update output unit list
        self.unitTypeOut.clear()
        self.unitTypeOut.addItems(outputUnits)


def main():
    app = QApplication(sys.argv)
    form = UnitsForm()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
