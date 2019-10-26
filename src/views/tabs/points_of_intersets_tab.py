from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QPushButton, QGridLayout, QLabel, QComboBox, QLineEdit, \
    QSpacerItem, QSizePolicy, QTextEdit

from src.common.tab_layout import TabLayout


class PointsOfInterestTab(TabLayout):
    def __init__(self):
        super().__init__("Points of Interest View", "Detailed Points of Interest View")
        super().addContentToLeftPanel(self.leftPanelBuilder())
        super().addContentToRightPanel(self.rightPanelBuilder())
        super().build()

    def leftPanelBuilder(self):
        layout = QVBoxLayout()
        self.poiList = QListWidget()
        addPoiButton = QPushButton('Add New Point of Interest')

        self.poiList.addItem("Point of Interest 1")
        self.poiList.addItem("Point of Interest 2")
        self.poiList.addItem("Point of Interest 3")
        self.poiList.addItem("Point of Interest 4")

        self.poiList.itemSelectionChanged.connect(self.useSelectedItem)

        layout.addLayout(self.searchBuilder())
        layout.addWidget(self.poiList)
        layout.addWidget(addPoiButton)

        return layout

    def rightPanelBuilder(self):
        layout = QGridLayout()

        existingPluginsDropdown = QComboBox()
        self.typeDropdown = QComboBox()
        self.content = QTextEdit()

        existingPluginsDropdown.addItems(["Network Plugin"])
        self.typeDropdown.addItems(["Variable", "String", "DLL", "Function", "Packet Protocol", "Struct"])

        layout.addWidget(QLabel("Plugin"), 0, 0, Qt.AlignRight)
        layout.addWidget(QLabel("Point of Interest Type"), 0, 3, Qt.AlignRight)
        layout.addWidget(existingPluginsDropdown, 0, 1)
        layout.addWidget(self.typeDropdown, 0, 4)

        spacer = QSpacerItem(1, 1, QSizePolicy.Expanding)

        layout.addWidget(self.content, 1, 0, 1, 9)

        layout.addItem(spacer, 0, 4, 1, 4)

        return layout

    def searchBuilder(self):
        layout = QGridLayout()

        searchBox = QLineEdit()
        searchBox.setPlaceholderText("Search Points of Interest")

        searchButton = QPushButton('Search')

        layout.addWidget(searchBox, 0, 0, 1, 4)
        layout.addWidget(searchButton, 0, 4, 1, 2)

        return layout

    def useSelectedItem(self):
        self.content.setText(f"{self.poiList.currentItem().text()} of type {self.typeDropdown.currentText()}")
