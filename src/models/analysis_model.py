from fuzzywuzzy import process

from src.analyzers.static_analyzer import StaticAnalyzer
from src.storage.entries_parser import EntriesParser


class AnalysisModel:
    def __init__(self):
        self.parser = EntriesParser()
        self.__staticAnalyzer = StaticAnalyzer()
        self.__pluginList = self.parser.getEntries("plugin")
        self.__poiList = dict()
        self.__message = ''

    def run_static(self, project, plugin):
        self.__staticAnalyzer.setPath(project.binaryPath)
        self.__poiList["Function"] = self.__staticAnalyzer.findPois("function")
        self.__poiList["DLL"] = self.__staticAnalyzer.findPois("dll")
        self.__poiList["String"] = self.__staticAnalyzer.findPois("strings")
        self.__poiList["Variable"] = self.__staticAnalyzer.findPois("variable")
        project.results[plugin] = self.__poiList
        self.__lint(plugin)
        self.__message = "Static analysis complete."

    def getPoiList(self):
        return self.__poiList

    def getTerminalOutput(self):
        return self.__message

    def getPluginFilters(self, pluginName):
        return self.__pluginList[pluginName].types

    def getPluginsList(self):
        return ["Select Plugin"] + [key for key in self.__pluginList.keys()]

    def setFilterList(self, filter):
        if len(self.__poiList) is 0:
            return []

        if filter == "All":
            temp = []
            for key in self.__poiList.keys():
                temp += self.__poiList[key]
            return temp

        if filter not in "Struct Packet Protocol":
            return self.__poiList[filter]
        else:
            return []

    def __lint(self, pluginName):
        plugin = self.__pluginList[pluginName]
        for key in self.__poiList.keys():
            lint = []
            for e in self.__poiList[key]:
                if key == 'Variable':
                    lint.append(e['name'])
                    continue
                name = ''
                if key == 'Function' or key == 'DLL' or key == 'Variable':
                    name = 'name'
                elif key == 'String':
                    name = 'value'
                if process.extractOne(e[name], list(plugin.pois.keys()))[1] > 80:
                    lint.append(e[name])
            self.__poiList[key] = lint

    def update(self):
        self.__pluginList = self.parser.getEntries("plugin")

    def saveProject(self, project):
        self.parser.updateEntry("project", project)
