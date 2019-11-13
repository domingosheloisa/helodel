# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PointsByPolygons
                                 A QGIS plugin
 Etapa 4 do HeloDel
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-11-04
        git sha              : $Format:%H$
        copyright            : (C) 2019 by SUPGEP/CASAL
        email                : supgep.e1@casal.al.gov.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from PyQt5.QtWidgets import QAction, QFileDialog
from qgis.core import QgsProject, Qgis, QgsVectorLayer
from qgis.utils import iface

import dbf
import processing

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .points_by_polygons_dialog import PointsByPolygonsDialog
import os.path


class PointsByPolygons:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PointsByPolygons_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Points by Polygons')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PointsByPolygons', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        """icon_path = ':/plugins/points_by_polygons/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Points by Polygons'),
            callback=self.run,
            parent=self.iface.mainWindow())"""

        # will be set False in run()
        self.first_start = True
        
        self.actionRun = QAction(QIcon("/home/gedop/.local/share/QGIS/QGIS3/profiles/default/python/plugins/helonoi/icon.png"),"Points by Polygons", self.iface.mainWindow())
        self.iface.addPluginToVectorMenu("&HeloDel", self.actionRun)
        self.actionRun.triggered.connect(self.run)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Points by Polygons'),
                action)
            self.iface.removeToolBarIcon(action)
    
    def select_quad_files(self):
        filenames, _filter = QFileDialog.getOpenFileNames(self.dlg, "Selecione os arquivos de quadras")
        self.dlg.lineEdit_1.setText(', '.join(filenames))
        
    def select_lig_files(self):
        filename, _filter = QFileDialog.getOpenFileName(self.dlg, "Selecione o arquivo de ligações")
        self.dlg.lineEdit_2.setText(filename)
    
    def select_output_directory(self):
        filename = QFileDialog.getExistingDirectory(None, "Selecione o diretório de saída")
        self.dlg.lineEdit_3.setText(filename)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = PointsByPolygonsDialog()
            self.dlg.pushButton_1.clicked.connect(self.select_quad_files)
            self.dlg.pushButton_2.clicked.connect(self.select_lig_files)
            self.dlg.pushButton_3.clicked.connect(self.select_output_directory)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            arquivos_quadras = self.dlg.lineEdit_1.text().split(', ')
            camada_ligacoes = self.dlg.lineEdit_2.text()            
            for quadra in arquivos_quadras:
                arq_saida = self.dlg.lineEdit_3.text() + '/' + camada_ligacoes.split('/')[-1][0:-4] + '_' + quadra.split('/')[-1][0:-5] + ".shp"
                processing.run("qgis:clip", {'INPUT': camada_ligacoes,'OVERLAY': quadra, 'OUTPUT': arq_saida})
                
                #Alteração da tabela
                tabela = dbf.Table('%s'%(arq_saida[0:-4]+'.dbf'))
                tabela.open(mode=dbf.READ_WRITE)
                tabela.add_fields("quadra C(30)")
                #inserindo em cada dado
                nome_col = arq_saida[0:-4].split("_")
                for item in tabela:
                    dbf.write(item, quadra = nome_col[-1])
                tabela.close()
                
                iface.addVectorLayer(arq_saida, "", "ogr")
                self.iface.messageBar().pushMessage("Success", "Output file written at " + arq_saida,level=Qgis.Success, duration=3)