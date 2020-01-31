# -*- coding: utf-8 -*-
"""
/***************************************************************************
 shapefileloader
                                 A QGIS plugin
 this plugin will display shapefile
                              -------------------
        begin                : 2020-01-26
        git sha              : $Format:%H$
        copyright            : (C) 2020 by KIPYEGON AMOS
        email                : kiptoamos@gmail.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QMenu
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from shapefile_loader_dialog import shapefileloaderDialog
import os.path


class shapefileloader:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
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
            'shapefileloader_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        self.dlg = shapefileloaderDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Shapefile  LORDER')

        # self.menu= self.tr(u'&Showme')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'shapefileloader')
        self.toolbar.setObjectName(u'shapefileloader')
        # self.dlg.lineEdit.clear()
        # self.dlg.pushButton.clicked.connect(self.select_input)
        # self.dlg.lable_3.clear()

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
        return QCoreApplication.translate('shapefileloader', message)

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

        # Create the dialog (after translation) and keep reference
        # self.dlg = shapefileloaderDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/shapefileloader/icon.png'
        self.add_action(
            icon_path,
            text=self.tr('shapefile loader'),
            callback=self.select_input,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/shapefileloader/icon.png'
        self.add_action(
            icon_path,
            text=self.tr('county identifier'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Shapefile'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def select_input(self):
        # filename=QFileDialog.getSaveFileName(self.dlg,"select input file","",'*.sph')
        layer = QFileDialog.getOpenFileName(self.dlg, "select input file", '', '*.shp')
        # self.dlg.lineEdit.setText(filename)
        self.layer = self.iface.addVectorLayer(layer, '', 'ogr')

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()

        # for field in layer.fields():
        # print(field.name(),field.NAME_1())
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # layer=self.dlg.lineEdit.text()
            # filename=QFileDialog.getOpenFileName(self.dlg,"select input file",'','*.shp')

            # self.layer=self.iface.addVectorLayer(layer,'','ogr')
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
