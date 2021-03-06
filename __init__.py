# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoGame
                                 A QGIS plugin
 Wikipedia challenge in QGis
                             -------------------
        begin                : 2018-08-23
        copyright            : (C) 2018 by Roel
        email                : roel@huybrechts.re
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GeoGame class from file GeoGame.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .geogame import GeoGame
    return GeoGame(iface)
