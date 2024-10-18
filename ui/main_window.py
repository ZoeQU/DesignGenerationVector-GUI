# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsScene, QFileDialog
from PyQt5.QtGui import QPixmap
import sys
import os
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(746, 444)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/qu_icon_16x16.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # # 3D view
        self.label3DView = QtWidgets.QLabel(self.centralwidget)
        self.label3DView.setGeometry(QtCore.QRect(520, 40, 200, 20))
        self.label3DView.setObjectName("label3DView")
        self.ThreeDWidget = QVTKRenderWindowInteractor(self.centralwidget)
        self.ThreeDWidget.setGeometry(QtCore.QRect(520, 60, 200, 290))
        self.ThreeDWidget.setObjectName("ThreeDWidget")

        # 2D view
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(320, 60, 190, 290))
        self.graphicsView.setObjectName("graphicsView")
        self.TwoDView_2 = QtWidgets.QLabel(self.centralwidget)
        self.TwoDView_2.setGeometry(QtCore.QRect(330, 40, 50, 15))
        self.TwoDView_2.setObjectName("TwoDView_2")

        # Load design element button
        self.LoadDesignElement = QtWidgets.QPushButton(self.centralwidget)
        self.LoadDesignElement.setGeometry(QtCore.QRect(100, 90, 50, 20))
        self.LoadDesignElement.setObjectName("LoadDesignElement")
        self.LoadDesignElement.setText("Load")
        self.LoadDesignElement.clicked.connect(self.load_svg)

        # Design element text
        self.DesignElement = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.DesignElement.setGeometry(QtCore.QRect(20, 90, 78, 20))
        self.DesignElement.setObjectName("DesignElement")

        # Design element view
        self.DesignElementView = QtWidgets.QGraphicsView(self.centralwidget)
        self.DesignElementView.setGeometry(QtCore.QRect(20, 115, 130, 110))
        self.DesignElementView.setObjectName("DesignElementView")

        # Load color reference image button
        self.LoadColorReferenceImage = QtWidgets.QPushButton(self.centralwidget)
        self.LoadColorReferenceImage.setGeometry(QtCore.QRect(240, 90, 50, 20))
        self.LoadColorReferenceImage.setObjectName("LoadColorReferenceImage")
        self.LoadColorReferenceImage.setText("Load")
        self.LoadColorReferenceImage.clicked.connect(self.load_color_reference_image)

        # Color reference image view
        self.ColorRefView = QtWidgets.QGraphicsView(self.centralwidget)
        self.ColorRefView.setGeometry(QtCore.QRect(160, 115, 130, 110))
        self.ColorRefView.setObjectName("ColorRefView")
        
        # Color reference image text
        self.ColorReferenceImage = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ColorReferenceImage.setGeometry(QtCore.QRect(160, 90, 78, 20))
        self.ColorReferenceImage.setObjectName("ColorReferenceImage")

        # Color palette view
        self.ColorPaletteView = QtWidgets.QGraphicsView(self.centralwidget)
        self.ColorPaletteView.setGeometry(QtCore.QRect(20, 255, 130, 130))
        self.ColorPaletteView.setObjectName("ColorPaletteView")

        # Color palette text
        self.ColorPaletteText = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ColorPaletteText.setGeometry(QtCore.QRect(20, 230, 130, 20))
        self.ColorPaletteText.setObjectName("ColorPaletteText")

        # regenerate button
        self.ReGenerateButton = QtWidgets.QPushButton(self.centralwidget)
        self.ReGenerateButton.setGeometry(QtCore.QRect(170, 400, 82, 23))
        self.ReGenerateButton.setObjectName("ReGenerateButton")
        self.ReGenerateButton.clicked.connect(self.regenerate_button_click)
        
        # generate button
        self.GenerateButton = QtWidgets.QPushButton(self.centralwidget)
        self.GenerateButton.setGeometry(QtCore.QRect(80, 400, 83, 23))
        self.GenerateButton.setObjectName("GenerateButton")
        self.GenerateButton.clicked.connect(self.generate_button_click)

        self.ScaleScrollBar = QtWidgets.QSlider(self.centralwidget)
        self.ScaleScrollBar.setGeometry(QtCore.QRect(389, 370, 110, 15))
        self.ScaleScrollBar.setOrientation(QtCore.Qt.Horizontal)

        # download button
        self.DownloadButton = QtWidgets.QPushButton(self.centralwidget)
        self.DownloadButton.setGeometry(QtCore.QRect(410, 400, 200, 23))
        self.DownloadButton.setObjectName("DownloadButton")
        self.DownloadButton.clicked.connect(self.download_button_click)

        self.ScaleScrollBar.setObjectName("ScaleScrollBar")
        self.Rotate = QtWidgets.QLabel(self.centralwidget)
        self.Rotate.setGeometry(QtCore.QRect(524, 370, 40, 15))
        self.Rotate.setObjectName("Rotate")
        self.RotateScrollBar = QtWidgets.QSlider(self.centralwidget)
        self.RotateScrollBar.setGeometry(QtCore.QRect(570, 370, 109, 15))
        self.RotateScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.RotateScrollBar.setObjectName("RotateScrollBar")
        self.Scale = QtWidgets.QLabel(self.centralwidget)
        self.Scale.setGeometry(QtCore.QRect(350, 370, 33, 15))
        self.Scale.setObjectName("Scale")

        # num of color
        self.NumColor = QtWidgets.QLabel(self.centralwidget)
        self.NumColor.setGeometry(QtCore.QRect(30, 49, 127, 24))
        self.NumColor.setObjectName("NumColor")

        # pattern type 
        self.PatternType = QtWidgets.QLabel(self.centralwidget)
        self.PatternType.setGeometry(QtCore.QRect(30, 20, 127, 23))
        self.PatternType.setObjectName("PatternType")

        # pattern type combo box
        self.PatternTypecomboBox = QtWidgets.QComboBox(self.centralwidget)
        self.PatternTypecomboBox.setGeometry(QtCore.QRect(163, 20, 126, 23))
        self.PatternTypecomboBox.setObjectName("PatternTypecomboBox")
        self.PatternTypecomboBox.addItem("")
        self.PatternTypecomboBox.addItem("")
        self.PatternTypecomboBox.addItem("")

        # color spin box
        self.ColorSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.ColorSpinBox.setGeometry(QtCore.QRect(163, 49, 126, 24))
        self.ColorSpinBox.setProperty("value", 3)
        self.ColorSpinBox.setDisplayIntegerBase(10)
        self.ColorSpinBox.setObjectName("ColorSpinBox")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # VTK Renderer setup
        self.vtk_renderer = vtk.vtkRenderer()
        self.ThreeDWidget.GetRenderWindow().AddRenderer(self.vtk_renderer)
        self.iren = self.ThreeDWidget.GetRenderWindow().GetInteractor()

        # Load OBJ model
        self.load_obj_model("/home/zoe/ResearchProjects/DesignGenerationVector/resources/3dModels/Shirt.obj")
        # Connect button to load SVG
        self.LoadDesignElement.clicked.connect(self.load_svg)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Vector Pattern Auto-Generation"))
        self.DownloadButton.setText(_translate("MainWindow", "Download"))
        self.label3DView.setText(_translate("MainWindow", "3D View"))
        self.TwoDView_2.setText(_translate("MainWindow", "2D View"))
        self.ColorReferenceImage.setPlainText(_translate("MainWindow", "ColorRef"))
        self.LoadColorReferenceImage.setText(_translate("MainWindow", "Load"))
        self.LoadDesignElement.setText(_translate("MainWindow", "Load"))
        self.DesignElement.setPlainText(_translate("MainWindow", "Element"))
        self.ColorPaletteText.setPlainText(_translate("MainWindow", "Color Palette"))
        self.ReGenerateButton.setText(_translate("MainWindow", "ReGenerate"))
        self.GenerateButton.setText(_translate("MainWindow", "Generate"))
        self.Rotate.setText(_translate("MainWindow", "Rotate"))
        self.Scale.setText(_translate("MainWindow", "Scale"))
        self.NumColor.setText(_translate("MainWindow", "Number of Color:"))
        self.PatternTypecomboBox.setItemText(0, _translate("MainWindow", "Motif"))
        self.PatternTypecomboBox.setItemText(1, _translate("MainWindow", "Check"))
        self.PatternTypecomboBox.setItemText(2, _translate("MainWindow", "Stripe"))
        self.PatternType.setText(_translate("MainWindow", "Pattern Type:"))


    def download_button_click(self):
        print("Download button被click了")

    def generate_button_click(self):
        print("Generate button被click了")

    def regenerate_button_click(self):
        print("ReGenerate button被click了")

    def load_svg(self):
        # Open file dialog to select SVG
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(None, "Select SVG File", "/home/zoe/ResearchProjects/DesignGenerationVector/resources",
                                                  "SVG Files (*.svg)", options=options)

        if fileName:
            self.DesignElement.setPlainText(fileName.split("/")[-1])
            self.display_svg(self.DesignElementView, fileName)
            # self.LoadDesignElement.setEnabled(False)  # Disable button after loading

    def load_color_reference_image(self):
        # Open file dialog to select image
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(None, "Select Image File", "/home/zoe/ResearchProjects/DesignGenerationVector/resources",
                                                  "Image Files (*.png *.jpg *.jpeg)", options=options)

        if fileName:
            self.ColorReferenceImage.setPlainText(fileName.split("/")[-1])
            self.display_image(self.ColorRefView, fileName)
            # self.LoadColorReferenceImage.setEnabled(False)  # Disable button after loading

    def display_svg(self, view, file_path):
        scene = QGraphicsScene()
        svg_item = QGraphicsSvgItem(file_path)

        # Get dimensions of the view and SVG
        view_width = view.width()
        view_height = view.height()
        svg_rect = svg_item.boundingRect()

        # Calculate scale factor while maintaining aspect ratio
        scale_factor = min(view_width / svg_rect.width(), view_height / svg_rect.height())
        svg_item.setScale(scale_factor)

        # Center the SVG in the view
        svg_item.setPos(
            (view_width - svg_rect.width() * scale_factor) / 2,
            (view_height - svg_rect.height() * scale_factor) / 2
        )

        scene.addItem(svg_item)
        view.setScene(scene)

    def display_image(self, view, file_path):
        scene = QGraphicsScene()
        pixmap = QPixmap(file_path)

        # Get dimensions of the view and image
        view_width = view.width()
        view_height = view.height()

        # Scale the pixmap to fill the view while maintaining the aspect ratio
        pixmap = pixmap.scaled(view_width, view_height, QtCore.Qt.KeepAspectRatioByExpanding)

        # Center the image in the view
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        item.setPos(
            (view_width - pixmap.width()) / 2,
            (view_height - pixmap.height()) / 2
        )

        scene.addItem(item)
        view.setScene(scene)

    def load_obj_model(self, filename):
        reader = vtk.vtkOBJReader()
        reader.SetFileName(filename)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        self.vtk_renderer.AddActor(actor)
        self.vtk_renderer.ResetCamera()

        self.ThreeDWidget.GetRenderWindow().Render()
        self.iren.Initialize()

