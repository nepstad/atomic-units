import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SI_UNITS:
    WATT_PER_SQUARECM = 0

class UnitsForm(QWidget):

    def __init__(self, parent=None):
        super(UnitsForm, self).__init__(parent=parent)

        #Define SI units that we know
        unitsSI = sorted({unicode('W/cm**2'): SI_UNITS.WATT_PER_SQUARECM}.keys())

        #Set up input widgets
        self.formSI = QLineEdit()
        self.formAU = QLineEdit()

        #Set up input widgets
        self.unitTypeSI = QComboBox()
        self.unitTypeSI.addItems(unitsSI)

        #Create widget layout
        grid = QGridLayout()
        grid.addWidget(self.formSI, 0, 0)
        grid.addWidget(self.unitTypeSI, 0, 1)
        grid.addWidget(self.formAU, 1, 0)
        self.setLayout(grid)



def main():
    app = QApplication(sys.argv)
    form = UnitsForm()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
