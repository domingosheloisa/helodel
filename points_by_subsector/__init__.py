# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PointsBySubsector
                                 A QGIS plugin
 Etapa 2 do HeloDel
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-11-04
        copyright            : (C) 2019 by SUPGEP/CASAL
        email                : supgep.e1@casal.al.gov.br
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
    """Load PointsBySubsector class from file PointsBySubsector.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .points_by_subsector import PointsBySubsector
    return PointsBySubsector(iface)
