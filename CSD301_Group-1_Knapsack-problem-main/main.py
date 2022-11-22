import os
import sys
from PyQt5 import QtWidgets
from UIDesign.GUI import GUI
# Add base path to system for more imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# Run GUI app
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = GUI()
    ui.show()
    sys.exit(app.exec_())
