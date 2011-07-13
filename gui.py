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

        # Define In units that we know
        au = ConstantsAU(ParseCODATA("codata.txt"))
        self.ConvertIntensity = au.ConvertElectricFieldAtomicFromIntensitySI
        self.ConvertEfield = au.ConvertIntensitySIFromElectricFieldAtomic
        self.convertDict = {
                unicode('eV'): au.electron_volt,
                unicode('(a.u.) energy'): au.energy,
                unicode('(a.u.) mass'): au.mass,
                unicode('(SI) kg'): au.si_mass,
                unicode('(SI) J'): au.si_energy,
        }
        convertKeys = sorted(self.convertDict.keys(), key=lambda s: s.lower())

        # Set up input widgets
        self.formIn = QLineEdit()
        self.formOut = QLineEdit()

        # Intensity <-> E-field stuff
        self.intensityBox = QLineEdit()
        self.efieldBox = QLineEdit()
        intensityLabel = QLabel("I [W/cm**2] =")
        efieldLabel = QLabel("E [a.u.] =")

        # Set up input widgets
        self.unitTypeIn = QComboBox()
        self.unitTypeIn.addItems(convertKeys)
        self.unitTypeOut = QComboBox()
        self.generateOutputUnits(convertKeys[0])

        # Info widgets
        self.atomicUnitsList = QLabel()
        self.atomicUnitsList.setText("<b>Basic atomic units</b> <br> mass: %s" %
                "".join(["%s " % el
                    for el in reversed(au.codata['atomic unit of mass'])]))

        # Buttons!
        updateCodataButton = QPushButton("Fetch CODATA constants")

        # Create widget layout
        grid = QGridLayout()
        grid.addWidget(self.formIn, 0, 0)
        grid.addWidget(self.unitTypeIn, 0, 1)
        grid.addWidget(self.formOut, 1, 0)
        grid.addWidget(self.unitTypeOut, 1, 1)
#        grid.addWidget(self.atomicUnitsList, 2, 0, 1, -1)
        grid.addWidget(updateCodataButton, 3, 0, 1, -1)
        self.setLayout(grid)

        # Intensity <-> E-field layout
        subGrid = QGridLayout()
        subGrid.addWidget(intensityLabel, 0, 0)
        subGrid.addWidget(self.intensityBox, 0, 1)
        subGrid.addWidget(efieldLabel, 0, 2)
        subGrid.addWidget(self.efieldBox, 0, 3)
        grid.addLayout(subGrid, 2, 0, 1, -1)

        # Define form behavior
        self.connect(self.formIn, SIGNAL("textEdited(QString)"),
                self.updateOutputUnit)
        self.connect(self.unitTypeIn, SIGNAL("currentIndexChanged(QString)"),
                self.generateOutputUnits)
        self.connect(self.unitTypeIn, SIGNAL("currentIndexChanged(QString)"),
                self.updateOutputUnit)
        self.connect(self.unitTypeOut, SIGNAL("currentIndexChanged(QString)"),
                self.updateOutputUnit)
        self.connect(self.intensityBox, SIGNAL("textEdited(QString)"),
                self.updateEfield)
        self.connect(self.efieldBox, SIGNAL("textEdited(QString)"),
                self.updateIntensity)

        # Set the title
        self.setWindowTitle("Atomic Units")


    def updateOutputUnit(self):
        """Calculate and display value of output unit

        """

        # Get input In value
        try:
            inputVal = float(unicode(self.formIn.text()))
        except:
            inputVal = float("NaN")

        # Get input unit
        inputUnit = unicode(self.unitTypeIn.currentText())

        # Get output unit
        outputUnit = unicode(self.unitTypeOut.currentText())

        # Calculate value in a.u.
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


    def updateEfield(self):
        """Calculate and display electric field value from given intensity

        """

        # Get input value
        try:
            inputVal = float(unicode(self.intensityBox.text()))
        except:
            inputVal = float("NaN")

        # Compute electric field value
        outputVal = self.ConvertIntensity(inputVal)

        # Show it
        self.efieldBox.setText("%g" % outputVal)


    def updateIntensity(self):
        """Calculate and display intensity value from given electric field

        """

        # Get input value
        try:
            inputVal = float(unicode(self.efieldBox.text()))
        except:
            inputVal = float("NaN")

        # Compute electric field value
        outputVal = self.ConvertEfield(inputVal)

        # Show it
        self.intensityBox.setText("%g" % outputVal)


    def generateOutputUnits(self, newItem):
        """
        Generate list of compatible output units based on input units

        newItem: (string) name of input unit

        """
        # Get input unit
        inUnit = self.convertDict[unicode(newItem)]

        # Filter list of units for compatible output units
        outputUnitNames = filter(
                lambda x: x[1].canonical() == inUnit.canonical(),
                self.convertDict.iteritems())
        outputUnits = sorted(dict(outputUnitNames).keys(), key=lambda s: s.lower())

        # Update output unit list
        self.unitTypeOut.clear()
        self.unitTypeOut.addItems(outputUnits)
        self.unitTypeOut.setCurrentIndex(0)



def main():
    app = QApplication(sys.argv)
    form = UnitsForm()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
