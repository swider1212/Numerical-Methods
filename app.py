import random
import sys
import pyqtgraph as pg
from utilities import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QLineEdit, QPushButton
from PyQt6.QtGui import QPalette, QColor


SETTINGS = {
    "accuracy": .01,
    "default_left": -10,
    "default_right": 10,
    "default_function": 0,
    "default_iterations": 10,
    "default_epsilon": .001
}


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Zadanie 1")

        self.functions = ['x³-x²-2x+1=0', '2^x-3=0',
                     '3x+sin(x)-e^x=0', 'x³-x+1=0','tan(x)-1=-0', '2+cos(2x)=0', 'sin(x)-cos(x)=0']
        self.radioButtons = []
        self.isIterations=True
        layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        center_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        for (i, f) in enumerate(self.functions):
            functions_box = QHBoxLayout()
            rb=QRadioButton()
            self.radioButtons.append([rb, i])
            functions_box.addWidget(rb)
            functions_box.addWidget(QLabel(f))
            left_panel.addLayout(functions_box)
        
        self.radioButtons[SETTINGS["default_function"]][0].setChecked(True)
        layout.addLayout(left_panel)

        range_box = QHBoxLayout()
        range_box.addWidget(QLabel("Od: "))
        self.from_range = QLineEdit()
        self.from_range.setText(str(SETTINGS["default_left"]))
        range_box.addWidget(self.from_range)
        range_box.addWidget(QLabel("Do: "))
        self.to_range = QLineEdit()
        self.to_range.setText(str(SETTINGS["default_right"]))
        range_box.addWidget(self.to_range)

        variant_box = QHBoxLayout()

        self.epsi = QPushButton("Dokładność")
        self.epsi.clicked.connect(self.switchViews)
        variant_box.addWidget(self.epsi)

        self.iter=QPushButton("Iteracje")
        self.iter.clicked.connect(self.switchViews)
        self.iter.setEnabled(False)
        variant_box.addWidget(self.iter)

        iteration_box = QHBoxLayout()
        self.iteration_label = QLabel("Ilość iteracji")
        iteration_box.addWidget(self.iteration_label)
        self.iteration_count = QLineEdit(str(SETTINGS["default_iterations"]))
        iteration_box.addWidget(self.iteration_count)

        method_choice_box = QHBoxLayout()
        method_choice_box.addWidget(QPushButton("Dokładność"))
        method_choice_box.addWidget(QPushButton("Iteracje"))


        method2_choice_box = QHBoxLayout()
        self.bisekcja = QPushButton("Bisekcja")
        self.bisekcja.clicked.connect(self.drawBisekcja)
        method2_choice_box.addWidget(self.bisekcja)
        self.styczne = QPushButton("Styczne")
        self.styczne.clicked.connect(self.drawStyczne)
        method2_choice_box.addWidget(self.styczne)



        center_panel.addLayout(range_box)
        center_panel.addLayout(variant_box)
        center_panel.addLayout(iteration_box)
        center_panel.addLayout(method2_choice_box)      

        padding = 30
        center_panel.setContentsMargins(padding, padding, padding, padding)

        layout.addLayout(center_panel)

        self.graph = pg.PlotWidget()
        self.graph.showGrid(x=True, y=True)
        right_panel.addWidget(self.graph)
        self.result = QLabel("Wynik")
        right_panel.addWidget(self.result )

        layout.addLayout(right_panel)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def getFunction(self):
        for x in self.radioButtons:
            if(x[0].isChecked()):
                return all_functions[x[1]]

    def switchViews(self, _):
        if(self.isIterations):
            self.epsi.setEnabled(False)
            self.iter.setEnabled(True)
            self.isIterations = False
            self.iteration_label.setText("E=")
            self.iteration_count.setText(str(SETTINGS["default_epsilon"]))

        else:
            self.iter.setEnabled(False)
            self.epsi.setEnabled(True)
            self.isIterations = True
            self.iteration_label.setText("Ilość iteracji")
            self.iteration_count.setText(str(SETTINGS["default_iterations"]))

    def drawBisekcja(self):
        self.drawGraph(half_algoritm)

    def drawStyczne(self):
        self.drawGraph(newton_algoritm)

    def drawGraph(self, func):
        f = self.getFunction()
        left = SETTINGS["default_left"]
        right = SETTINGS["default_right"]
        if(self.from_range.text()):
            left = int(float(self.from_range.text()))
        if(self.to_range.text()):
            right = int(float(self.to_range.text()))
        if(left>right):
            left, right = right, left

        if(self.iteration_count.text()):
            if(self.isIterations):
                iter = int(self.iteration_count.text())
            else:
                iter = float(self.iteration_count.text())
        else:
            if(self.isIterations):
                iter = SETTINGS["default_iterations"]
            else:
                iter = SETTINGS["default_epsilon"]
        
        range_axis = [x for x in np.arange(left, right, SETTINGS["accuracy"]) ]
        value_axis = [f(x) for x in np.arange(left, right, SETTINGS["accuracy"])]

        self.graph.clear()
        method = 1 if self.isIterations else 2
        res = func(f, left, right, method, iter)
        self.graph.plot(range_axis, value_axis)
        if(not res):
            self.result.setText('Podaj inny przedział') 
            return False
        else: 
            [n, x] = res
            self.graph.plot([x], [f(x)], symbol='o', symbolSize=10, symbolBrush=('b'))
            self.result.setText('Ilość iteracji: ' + str(n) + '. Znalezione rozwiązanie: ' + str(x)) 
        return 0



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()