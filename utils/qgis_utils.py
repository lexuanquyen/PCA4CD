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

from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.gui import QgsRendererPropertiesDialog, QgsRendererRasterPropertiesWidget
from qgis.core import QgsProject, QgsRasterLayer, QgsVectorLayer, Qgis, QgsStyle, QgsMapLayer
from qgis.utils import iface


def valid_file_selected_in(combo_box, combobox_name=False):
    try:
        combo_box.currentLayer().dataProvider().dataSourceUri()
        return True
    except:
        # if not empty (valid selected) and combobox name given
        if combo_box.currentText() and combobox_name:
            iface.messageBar().pushMessage("PCA4CD", "Error, please browse/select a valid file in "
                                           + combobox_name, level=Qgis.Warning)

        combo_box.setCurrentIndex(-1)
        return False


def get_layer_by_name(layer_name):
    layer = QgsProject.instance().mapLayersByName(layer_name)
    if layer:
        return layer[0]


def get_file_path_of_layer(layer):
    try:
        return str(layer.dataProvider().dataSourceUri().split('|layerid')[0])
    except:
        return None


def get_current_file_path_in(combo_box, show_message=True):
    try:
        file_path = str(combo_box.currentLayer().dataProvider().dataSourceUri().split('|layerid')[0])
        if os.path.isfile(file_path) or file_path.startswith("memory"):
            return file_path
    except:
        if show_message:
            iface.messageBar().pushMessage("PCA4CD", "Error, please select a valid file",
                                           level=Qgis.Warning)
    return None


def load_and_select_filepath_in(combo_box, file_path, layer_type="any"):
    filename = os.path.splitext(os.path.basename(file_path))[0]
    layer = get_layer_by_name(filename)
    if not layer:
        # load to qgis and update combobox list
        load_layer_in_qgis(file_path, layer_type)
    # select the sampling file in combobox
    selected_index = combo_box.findText(filename, Qt.MatchFixedString)
    combo_box.setCurrentIndex(selected_index)

    return get_layer_by_name(filename)


def load_layer_in_qgis(file_path, layer_type):
    # first unload layer from qgis if exists
    unload_layer_in_qgis(file_path)
    # create layer
    filename = os.path.splitext(os.path.basename(file_path))[0]
    if layer_type == "raster":
        layer = QgsRasterLayer(file_path, filename)
    if layer_type == "vector":
        layer = QgsVectorLayer(file_path, filename, "ogr")
    if layer_type == "any":
        if file_path.endswith((".tif", ".TIF", ".img", ".IMG")):
            layer = QgsRasterLayer(file_path, filename)
        if file_path.endswith((".gpkg", ".GPKG", ".shp", ".SHP")):
            layer = QgsVectorLayer(file_path, filename, "ogr")
    # load
    if layer.isValid():
        QgsProject.instance().addMapLayer(layer)
    else:
        iface.messageBar().pushMessage("PCA4CD", "Error, {} is not a valid {} file!"
                                       .format(os.path.basename(file_path), layer_type))
    return filename


def unload_layer_in_qgis(layer_path):
    layers_loaded = QgsProject.instance().mapLayers().values()
    for layer_loaded in layers_loaded:
        if hasattr(layer_loaded, "dataProvider"):
            if layer_path == layer_loaded.dataProvider().dataSourceUri().split('|layerid')[0]:
                QgsProject.instance().removeMapLayer(layer_loaded)


# plugin path
plugin_folder = os.path.dirname(os.path.dirname(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    plugin_folder, 'ui', 'classification_style_editor.ui'))


class StyleEditorDialog(QDialog, FORM_CLASS):
    def __init__(self, layer, canvas, parent=None):
        QDialog.__init__(self)
        self.setupUi(self)
        self.layer = layer

        self.setWindowTitle("{} - style editor".format(self.layer.name()))

        if self.layer.type() == QgsMapLayer.VectorLayer:
            self.StyleEditorWidget = QgsRendererPropertiesDialog(self.layer, QgsStyle(), True, parent)

        if self.layer.type() == QgsMapLayer.RasterLayer:
            self.StyleEditorWidget = QgsRendererRasterPropertiesWidget(self.layer, canvas, parent)

        self.scrollArea.setWidget(self.StyleEditorWidget)

        self.DialogButtons.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)
        self.DialogButtons.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        self.DialogButtons.button(QDialogButtonBox.Apply).clicked.connect(self.apply)

    def apply(self):
        self.StyleEditorWidget.apply()
        self.layer.triggerRepaint()