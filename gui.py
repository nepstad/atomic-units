import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
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
                unicode('energy'): au.energy
        }
        convertKeys = sorted(self.convertDict.keys(), key=lambda s: s.lower())

        #Set up input widgets
        self.formIn = QLineEdit()
        self.formOut = QLineEdit()

        #Set up input widgets
        self.unitTypeIn = QComboBox()
        self.unitTypeIn.addItems(convertKeys)
        self.unitTypeOut = QComboBox()
        self.unitTypeOut.addItems(convertKeys)

        #Info widgets
        self.atomicUnitsList = QLabel()
        self.atomicUnitsList.setText("<b>List of atomic units</b> <br> time: %s" %
                "".join(["%s " % el for el in reversed(au.codata['atomic unit of time'])]))

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
        outputVal = g(f(inputVal))

        self.formOut.setText("%g" % outputVal)



def main():
    app = QApplication(sys.argv)
    form = UnitsForm()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
