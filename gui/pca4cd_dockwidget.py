# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PCA4CD
                                 A QGIS plugin
 Principal components analysis for change detections
                              -------------------
        copyright            : (C) 2018 by Xavier Corredor Llano, SMByC
        email                : xcorredorl@ideam.gov.co
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

import os
import tempfile
import configparser
import webbrowser

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtWidgets import QMessageBox, QFileDialog, QDockWidget
from qgis.core import QgsProject, QgsVectorFileWriter, QgsMapLayerProxyModel, Qgis, QgsUnitTypes
from qgis.utils import iface

from pca4cd.gui.about_dialog import AboutDialog
from pca4cd.utils.qgis_utils import load_and_select_filepath_in

# plugin path
plugin_folder = os.path.dirname(os.path.dirname(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    plugin_folder, 'ui', 'pca4cd_dockwidget.ui'))

cfg = configparser.ConfigParser()
cfg.read(os.path.join(plugin_folder, 'metadata.txt'))
VERSION = cfg.get('general', 'version')
HOMEPAGE = cfg.get('general', 'homepage')


class PCA4CDDockWidget(QDockWidget, FORM_CLASS):
    closingPlugin = pyqtSignal()
    dockwidget = None

    def __init__(self, parent=None):
        """Constructor."""
        super(PCA4CDDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setup_gui()
        # tmp dir for all process and intermediate files
        self.tmp_dir = tempfile.mkdtemp()
        # save instance
        PCA4CDDockWidget.dockwidget = self

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def setup_gui(self):
        # ######### plugin info ######### #
        self.about_dialog = AboutDialog()
        self.QPBtn_PluginInfo.setText("v{}".format(VERSION))
        self.QPBtn_PluginInfo.clicked.connect(self.about_dialog.show)
        self.QPBtn_PluginDocs.clicked.connect(lambda: webbrowser.open("https://smbyc.bitbucket.io/qgisplugins/pca4cd"))

        # ######### load input raster image ######### #
        ## A
        # set properties to QgsMapLayerComboBox
        self.QCBox_InputData_A.setCurrentIndex(-1)
        self.QCBox_InputData_A.setFilters(QgsMapLayerProxyModel.RasterLayer)
        # call to browse the thematic raster file
        self.QPBtn_browseData_A.clicked.connect(lambda: self.fileDialog_browse(
            self.QCBox_InputData_A,
            dialog_title=self.tr("Select the first period of the raster image to analyze"),
            dialog_types=self.tr("Raster files (*.tif *.img);;All files (*.*)"),
            layer_type="raster"))
        self.QCBox_InputData_A.currentIndexChanged.connect(self.set_number_components)
        ## B
        # set properties to QgsMapLayerComboBox
        self.QCBox_InputData_B.setCurrentIndex(-1)
        self.QCBox_InputData_B.setFilters(QgsMapLayerProxyModel.RasterLayer)
        # call to browse the thematic raster file
        self.QPBtn_browseData_B.clicked.connect(lambda: self.fileDialog_browse(
            self.QCBox_InputData_B,
            dialog_title=self.tr("Select the second period of the raster image to analyze"),
            dialog_types=self.tr("Raster files (*.tif *.img);;All files (*.*)"),
            layer_type="raster"))
        self.QCBox_InputData_B.currentIndexChanged.connect(self.set_number_components)

    @pyqtSlot()
    def fileDialog_browse(self, combo_box, dialog_title, dialog_types, layer_type):
        file_path, _ = QFileDialog.getOpenFileName(self, dialog_title, "", dialog_types)
        if file_path != '' and os.path.isfile(file_path):
            # load to qgis and update combobox list
            load_and_select_filepath_in(combo_box, file_path, layer_type)

    @pyqtSlot()
    def set_number_components(self):
        current_layer_A = self.QCBox_InputData_A.currentLayer()
        current_layer_B = self.QCBox_InputData_B.currentLayer()
        self.QCBox_nComponents.clear()
        if current_layer_A is not None and current_layer_B is not None:
            number_components = current_layer_A.bandCount() + current_layer_B.bandCount()
            # set number of components to combobox
            self.QCBox_nComponents.addItems([str(x) for x in range(1, number_components + 1)])
            # select the last item
            self.QCBox_nComponents.setCurrentIndex(number_components-1)
