from PyQt5 import QtWidgets

from src.models.analysis_model import AnalysisModel
from src.views.dialogs.analysis_result_dialog import AnalysisResultDialog
from src.views.dialogs.comment_dialog import CommentDialog
from src.views.dialogs.output_field_dialog import OutputField
from src.views.tabs.analysis_tab import AnalysisTab


class AnalysisTabController:
    def __init__(self):
        self.tab = AnalysisTab()
        self.project = None
        self.model = AnalysisModel()
        self.__addEventHandlers()
        self.__populateList()
        self.__populateDropdowns()

    def __addEventHandlers(self):
        self.tab.poiList.itemClicked.connect(lambda: self.__displayPOI())
        self.tab.searchBox.returnPressed.connect(lambda: self.__searchForPoi())
        self.tab.searchButton.clicked.connect(lambda: self.__searchForPoi())
        self.tab.commentBtn.clicked.connect(lambda: self.__commentWindow())
        self.tab.analysisResultBtn.clicked.connect(lambda: self.__analysisResultWindow())
        self.tab.outputFieldViewBtn.clicked.connect(lambda: self.__outputFieldWindow())
        self.tab.staticRunBtn.clicked.connect(lambda : self.__runStatic())
        self.tab.poiTypeDropdown.currentIndexChanged.connect(lambda : self.__populateList())
        self.tab.pluginDropdown.currentIndexChanged.connect(lambda: self.__selectPlugin())
        self.tab.dynamicRunbtn.clicked.connect(lambda: self.__runDynamic())

    def __populateList(self):
        filter = str(self.tab.poiTypeDropdown.currentText())
        self.tab.poiList.clear()
        list = self.model.setFilterList(filter)
        for item in list:
            self.tab.poiList.addItem(item)

    def __selectPlugin(self):
        selected = self.tab.pluginDropdown.currentText()
        if selected in "Select Plugin":
            self.tab.poiTypeDropdown.setEnabled(False)
            self.tab.staticRunBtn.setEnabled(False)
            self.tab.dynamicRunbtn.setEnabled(False)
            self.tab.dynamicStopbtn.setEnabled(False)
            self.tab.poiTypeDropdown.clear()
            self.tab.poiContentArea.clear()
            self.tab.poiList.clear()
        else:
            self.tab.poiList.clear()
            self.tab.poiTypeDropdown.setEnabled(True)
            self.tab.staticRunBtn.setEnabled(True)
            self.tab.dynamicRunbtn.setEnabled(True)
            self.tab.dynamicStopbtn.setEnabled(True)
            self.tab.poiTypeDropdown.clear()
            self.tab.poiTypeDropdown.addItems(self.model.getPluginFilters(selected))
            if self.project is not None:
                if len(self.project.results) > 0:
                    filter = self.tab.poiTypeDropdown.currentText()
                    self.tab.poiList.clear()
                    pois = []
                    try:
                        if filter == "All":
                            for key in self.project.results[selected].keys():
                                pois += self.project.results[selected][key]
                        else:
                            pois = self.project.results[selected][filter]
                        for item in pois:
                            # TODO: refactor to dictionary
                            self.tab.poiList.addItem(item)
                    except:
                        pass

    def __populateDropdowns(self):
        self.tab.pluginDropdown.addItems(self.model.getPluginsList())

    def __searchForPoi(self):
        searchText = self.tab.searchBox.text().lower()
        if searchText is "":
            self.tab.poiList.clear()
            self.__populateList()
        else:
            searchList = []
            for poiType in self.model.getPoiList().keys():
                for poiName in self.model.getPoiList()[poiType]:
                    if searchText in poiName.lower():
                        searchList.append(poiName)
            self.tab.poiList.clear()
            for item in searchList:
                self.tab.poiList.addItem(item)

    def __commentWindow(self):
        self.tab.commentView = CommentDialog()
        self.tab.commentView.show()

    def __outputFieldWindow(self):
        self.tab.outputFieldWindow = OutputField()
        self.tab.outputFieldWindow.show()

    def __analysisResultWindow(self):
        self.tab.analysisResultWindow = AnalysisResultDialog()
        self.tab.analysisResultWindow.show()

    def __displayPOI(self):
        selected = self.tab.poiTypeDropdown.currentText()
        temp = []
        items = [e.text() for e in self.tab.poiList.selectedItems()]
        for e in self.model.setFilterList(selected):
            if e in items:
                temp.append(self.model.findPoi(e))
        self.__updatePOI(temp)

    def __runStatic(self):
        if self.project is not None:
            plugin = self.tab.pluginDropdown.currentText()
            self.model.run_static(self.project, plugin)
            self.__updateTerminal()
            self.__populateList()
            self.model.saveProject(self.project)
        else:
            errorDialog = QtWidgets.QMessageBox()
            errorDialog.setText('Project Not Selected')
            errorDialog.setWindowTitle("Error")
            errorDialog.setInformativeText("Select a project from the Project Tab.")
            errorDialog.setIcon(3)
            errorDialog.exec_()

    def __updatePOI(self, x):
        screen = ""
        for e in x:
            info = ""
            for key in e.keys():
                info += f"{key}: {e[key]}\n"
            screen += info + "============\n"
        self.tab.poiContentArea.setPlainText(screen)

    def __updateTerminal(self):
        self.tab.terminalContent.appendPlainText(self.model.getTerminalOutput())

    def setProject(self, project):
        self.project = project

    def __runDynamic(self):
        if self.project is not None:
            # TODO: Replace with dynamic stuff
            pass
        else:
            errorDialog = QtWidgets.QMessageBox()
            errorDialog.setText('Project Not Selected')
            errorDialog.setWindowTitle("Error")
            errorDialog.setInformativeText("Select a project from the Project Tab.")
            errorDialog.setIcon(3)
            errorDialog.exec_()

    def update(self):
        self.model.update()
        self.tab.pluginDropdown.clear()
        self.__populateDropdowns()
        self.tab.pluginDropdown.setCurrentIndex(0)