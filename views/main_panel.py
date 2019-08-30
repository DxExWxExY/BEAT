from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel

from common import constants


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.buttonBuilder()
        self.buildWindow()

    def buttonBuilder(self):
        self.projectButton = QPushButton('Project')
        self.analysisButton = QPushButton('Analysis')
        self.pluginManagementButton = QPushButton('Plugin Management')
        self.poiButton = QPushButton('Points of Interest')
        self.documentationButton = QPushButton('Documentation')
    #     TODO: Add events

    def buildWindow(self):
        menuGrid = QGridLayout()
        menuGrid.addWidget(self.projectButton, 0 , 0)
        menuGrid.addWidget(self.analysisButton, 0, 1)
        menuGrid.addWidget(self.pluginManagementButton, 0, 2)
        menuGrid.addWidget(self.poiButton, 0, 3)
        menuGrid.addWidget(self.documentationButton, 0, 4)

        contentGrid = QGridLayout()
        contentGrid.addWidget(QLabel('Panel'), 3, 1, 5, 5)

        mainGrid = QGridLayout()
        mainGrid.addLayout(menuGrid, 0, 0, 1, 5)
        mainGrid.addLayout(contentGrid, 1, 0)

        self.setWindowTitle(constants.SYSTEM_TITLE)
        self.setLayout(mainGrid)
        self.show()