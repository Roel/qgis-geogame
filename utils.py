from qgis.core import QgsFeatureRequest

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
