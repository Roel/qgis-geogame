from PyQt5.QtCore import *
from PyQt5.QtGui import *

from qgis.core import *
from qgis.gui import *

from .utils import getRandomFeature

class Game(object):
    def __init__(self, iface, dockwidget):
        self.iface = iface
        self.dockwidget = dockwidget
        self.layer = None

        self.featureIdsGuessed = []
        self.featureToGuess = None
        self.pointToGuess = None
        self.score = 0

        self.mapToolPan = QgsMapToolPan(self.iface.mapCanvas())
        self.mapToolPoint = QgsMapToolEmitPoint(self.iface.mapCanvas())

        self.transformWGStoMap = QgsCoordinateTransform(
            QgsCoordinateReferenceSystem("EPSG:4326"),
            self.iface.mapCanvas().mapSettings().destinationCrs(),
            QgsProject.instance())

    def setNextFeature(self):
        if self.rounds > 0:
            self.rounds -= 1

            self.featureToGuess = getRandomFeature(self.layer, self.featureIdsGuessed)

            if self.featureToGuess:
                self.pointToGuess = self.transformWGStoMap.transform(self.featureToGuess.geometry().asPoint())

                name = self.featureToGuess.attribute("name") or ""
                self.dockwidget.nameLabel.setText(unicode(name))

                self.dockwidget.webView.setHtml("")
                self.dockwidget.hintLabel.setText("")
                wikiLang, wikiPage = self.featureToGuess.attribute("wikipedia").split(':')
                self.dockwidget.webView.setUrl(QUrl('http://' + wikiLang + '.m.wikipedia.org/wiki/' + wikiPage))
            else:
                self.stop()
        else:
            self.stop()

    def start(self):
        self.layer = self.iface.activeLayer()
        
        if self.layer:
            self.rounds = 4
            self.featureIdsGuessed = []
            self.resetScore()

            self.iface.mapCanvas().setMapTool(self.mapToolPoint)
            self.iface.mapCanvas().xyCoordinates.connect(self.hint)

            self.setNextFeature()

            self.dockwidget.startButton.setEnabled(False)
            self.dockwidget.stopButton.setEnabled(True)
            self.mapToolPoint.canvasClicked.connect(self.guess)
        else:
            self.dockwidget.hintLabel.setText("First select a vector layer in the legend tree.")

    def stop(self):
        self.layer = None
        self.featureToGuess = None
        self.pointToGuess = None

        self.iface.mapCanvas().setMapTool(self.mapToolPan)
        self.iface.mapCanvas().xyCoordinates.disconnect(self.hint)

        self.dockwidget.startButton.setEnabled(True)
        self.dockwidget.stopButton.setEnabled(False)
        self.dockwidget.nameLabel.setText("")
        self.dockwidget.hintLabel.setText("")
        self.dockwidget.webView.setHtml("")
        self.mapToolPoint.canvasClicked.disconnect()

    def resetScore(self):
        self.score = 0
        self.dockwidget.scorePanel.display(self.score)

    def guess(self, point):
        if self.pointToGuess:
            dist = self.pointToGuess.distance(point)
            score = max(int(1000-dist)/4, 0)

            self.score += score
            self.dockwidget.scorePanel.display(self.score)
            self.setNextFeature()

    def hint(self, point):
        if self.pointToGuess:
            dist = self.pointToGuess.distance(point)

            if dist > 2000:
                self.dockwidget.hintLabel.setText('Are you even trying?!')
            elif dist > 1000:
                self.dockwidget.hintLabel.setText('Still some room for improvement..')
            elif dist > 500:
                self.dockwidget.hintLabel.setText('Close but no cigar!')
            elif dist > 250:
                self.dockwidget.hintLabel.setText('Gotcha!')
        else:
            self.dockwidget.hintLabel.setText("")

