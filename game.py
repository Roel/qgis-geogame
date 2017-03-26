from qgis.core import *
from qgis.gui import *

import random

def getRandomFeature(vectorLayer, forbiddenIds):
    def getFeature(id):
        return vectorLayer.getFeatures(QgsFeatureRequest(id)).next()

    possibleIds = [id for id in vectorLayer.allFeatureIds() if id not in forbiddenIds]
    
    if len(possibleIds) == 0:
        return None
    elif len(possibleIds) == 1:
        chosenId = possibleIds[0]
        forbiddenIds.append(chosenId)
        return getFeature(chosenId)
    else:
        rIdx = random.randint(0, len(possibleIds)-1)
        chosenId = possibleIds[rIdx]
        forbiddenIds.append(chosenId)
        return getFeature(chosenId)

class Game(object):
    def __init__(self, iface, dockwidget):
        self.iface = iface
        self.dockwidget = dockwidget
        self.layer = None

        self.featureIdsGuessed = []
        self.featureToGuess = None

        self.mapToolPan = QgsMapToolPan(self.iface.mapCanvas())
        self.mapToolPoint = QgsMapToolEmitPoint(self.iface.mapCanvas())

    def setNextFeature(self):
        self.featureToGuess = getRandomFeature(self.layer, self.featureIdsGuessed)
        self.dockwidget.nameLabel.setText(str(self.featureToGuess.attribute("name")))

    def start(self):
        self.layer = self.iface.activeLayer()
        
        if self.layer:
            self.iface.mapCanvas().setMapTool(self.mapToolPoint)

            self.setNextFeature()

            self.dockwidget.startButton.setEnabled(False)
            self.dockwidget.stopButton.setEnabled(True)
            self.mapToolPoint.canvasClicked.connect(self.guess)

    def stop(self):
        self.layer = None
        self.iface.mapCanvas().setMapTool(self.mapToolPan)

        self.dockwidget.startButton.setEnabled(True)
        self.dockwidget.stopButton.setEnabled(False)
        self.dockwidget.nameLabel.setText("")
        self.mapToolPoint.canvasClicked.disconnect()

    def guess(self, point):
        print(point.x(), point.y())
