# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QMainWindow, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
import sys
import cv2
import os
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor  #type: ignore


from setting import savePath, imgPath, elementPath, processPath, keepPath, svgPath, colorrefPath

from utils import image_processing
from src.extraction.extractor import extractor
from src.vectorization.vectorizator import vectorize_design_element
from src.generation.motif_generator import generate_motif_pattern
from src.generation.check_generator import generate_check_pattern
from src.generation.stripe_generator import generate_stripe_pattern

import warnings
warnings.filterwarnings("ignore")

def mkfolder(path):
    if not os.path.exists(path):
        os.makedirs(path)

for path in [savePath, imgPath, elementPath, processPath, keepPath, svgPath]:
    mkfolder(path)


class Ui_MainWindow(object):
    def __init__(self) -> None:
        super().__init__()
        self.element_pathes = None
        self.color_block_path = None
        self.svg_name = None

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
        self.label2DView = QtWidgets.QLabel(self.centralwidget)
        self.label2DView.setGeometry(QtCore.QRect(330, 40, 50, 15))
        self.label2DView.setObjectName("label2DView")

        # Load "input raster image" button
        self.LoadImageInput = QtWidgets.QPushButton(self.centralwidget)
        self.LoadImageInput.setGeometry(QtCore.QRect(100, 90, 50, 20))
        self.LoadImageInput.setObjectName("LoadImageInput")
        self.LoadImageInput.setText("Load")
        self.LoadImageInput.clicked.connect(self.load_input_image)

        # Load "input raster image" text
        self.ImageInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ImageInput.setGeometry(QtCore.QRect(20, 90, 78, 20))
        self.ImageInput.setObjectName("ImageInput")

        # "input raster image" view
        self.ImageInputView = QtWidgets.QGraphicsView(self.centralwidget)
        self.ImageInputView.setGeometry(QtCore.QRect(20, 115, 130, 120))
        self.ImageInputView.setObjectName("InputImageView")

        # Load color reference image button
        self.LoadColorReferenceImage = QtWidgets.QPushButton(self.centralwidget)
        self.LoadColorReferenceImage.setGeometry(QtCore.QRect(240, 90, 50, 20))
        self.LoadColorReferenceImage.setObjectName("LoadColorReferenceImage")
        self.LoadColorReferenceImage.setText("Load")
        self.LoadColorReferenceImage.clicked.connect(self.load_color_reference_image)

        # Color reference image view
        self.ColorRefView = QtWidgets.QGraphicsView(self.centralwidget)
        self.ColorRefView.setGeometry(QtCore.QRect(160, 115, 130, 120))
        self.ColorRefView.setObjectName("ColorRefView")
        
        # Color reference image text
        self.ColorReferenceImage = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ColorReferenceImage.setGeometry(QtCore.QRect(160, 90, 78, 20))
        self.ColorReferenceImage.setObjectName("ColorReferenceImage")

        # Color palette view
        self.ColorPaletteView = QtWidgets.QGraphicsView(self.centralwidget)
        self.ColorPaletteView.setGeometry(QtCore.QRect(20, 265, 270, 128))
        self.ColorPaletteView.setObjectName("ColorPaletteView")

        # Color palette text
        self.ColorPaletteText = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ColorPaletteText.setGeometry(QtCore.QRect(20, 240, 270, 20))
        self.ColorPaletteText.setObjectName("ColorPaletteText")

        # regenerate button
        self.ReGenerateButton = QtWidgets.QPushButton(self.centralwidget)
        self.ReGenerateButton.setGeometry(QtCore.QRect(170, 400, 82, 23))
        self.ReGenerateButton.setObjectName("ReGenerateButton")
        self.ReGenerateButton.clicked.connect(self.regenerate_button_click)
        
        # generate button
        self.GenerateButton = QtWidgets.QPushButton(self.centralwidget)
        self.GenerateButton.setGeometry(QtCore.QRect(55, 400, 83, 23))
        self.GenerateButton.setObjectName("GenerateButton")
        self.GenerateButton.clicked.connect(self.generate_button_click)

        # download button
        self.DownloadButton = QtWidgets.QPushButton(self.centralwidget)
        self.DownloadButton.setGeometry(QtCore.QRect(410, 400, 200, 23))
        self.DownloadButton.setObjectName("DownloadButton")
        self.DownloadButton.clicked.connect(self.download_button_click)

        # Scale label
        self.Scale = QtWidgets.QLabel(self.centralwidget)
        self.Scale.setGeometry(QtCore.QRect(350, 370, 33, 15))
        self.Scale.setObjectName("Scale")

        # Scale scrollbar
        self.ScaleScrollBar = QtWidgets.QSlider(self.centralwidget)
        self.ScaleScrollBar.setGeometry(QtCore.QRect(389, 370, 110, 15))
        self.ScaleScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.ScaleScrollBar.setObjectName("ScaleScrollBar")
        self.ScaleScrollBar.setMinimum(1)
        self.ScaleScrollBar.setMaximum(100)
        self.ScaleScrollBar.setValue(1)
        self.ScaleScrollBar.valueChanged.connect(self.scale_image)

        # Rotate scrollbar
        self.Rotate = QtWidgets.QLabel(self.centralwidget)
        self.Rotate.setGeometry(QtCore.QRect(524, 370, 40, 15))
        self.Rotate.setObjectName("Rotate")
        self.RotateScrollBar = QtWidgets.QSlider(self.centralwidget)
        self.RotateScrollBar.setGeometry(QtCore.QRect(570, 370, 109, 15))
        self.RotateScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.RotateScrollBar.setObjectName("RotateScrollBar")

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
        self.ColorSpinBox.setMinimum(2) 
        self.ColorSpinBox.setMaximum(9) 
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


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Vector Pattern Auto-Generation"))
        self.DownloadButton.setText(_translate("MainWindow", "Download"))
        self.label3DView.setText(_translate("MainWindow", "3D View"))
        self.label2DView.setText(_translate("MainWindow", "2D View"))
        self.ColorReferenceImage.setPlainText(_translate("MainWindow", "ColorRef"))
        self.LoadColorReferenceImage.setText(_translate("MainWindow", "Load"))
        self.LoadImageInput.setText(_translate("MainWindow", "Load"))
        self.ImageInput.setPlainText(_translate("MainWindow", "Input"))
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
        try:
            # Let the user choose a folder (pass `self` as the parent)
            folder_path = QFileDialog.getExistingDirectory(None, "Select Folder to Save Images", "/home/zoe/ResearchProjects/DesignGenerationVector/data/temp/temp_save")
            if not folder_path:
                QMessageBox.warning(None, "Warning", "No folder selected!", QMessageBox.Ok)
                return

            # Save the PNG and SVG files
            self.save_file(self.color_block_path, folder_path)
            self.save_file(self.svg_name, folder_path)

            # Show success message
            QMessageBox.information(None, "Success", f"Both images have been saved to:\n{folder_path}", QMessageBox.Ok)

        except Exception as e:
            # Display error message if something goes wrong
            QMessageBox.critical(None, "Error", f"An error occurred while saving files: {str(e)}", QMessageBox.Ok)


    def save_file(self, source_path, target_folder):
        """
        Save a file from source_path to the target folder.
        """
        if not os.path.exists(source_path):
            QMessageBox.warning(None, "Error", f"File not found: {source_path}", QMessageBox.Ok)
            return False

        target_path = os.path.join(target_folder, os.path.basename(source_path))
        try:
            with open(source_path, "rb") as src_file:
                with open(target_path, "wb") as target_file:
                    target_file.write(src_file.read())
            return True
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to save file: {str(e)}", QMessageBox.Ok)
            return False


    def generate_button_click(self):
        self.input_pattern_type = self.PatternTypecomboBox.currentText()
        self.input_color_number = self.ColorSpinBox.value()
        print("Generate button被click了")
        # print(self.input_pattern_type)
        # print(self.input_color_number)
        
        if self.input_pattern_type == "Check":
            svg_name, color_block_path = generate_check_pattern(self.input_color_image, num=self.input_color_number)
            self.svg_name = svg_name
            self.color_block_path = color_block_path
            self.display_gengrate_images(self.svg_name, self.color_block_path)
            
        elif self.input_pattern_type == "Motif":
            bk_color, keep  = extractor(self.input_design_image, self.name, visualization=True)
            element_pathes, color_block_path = vectorize_design_element(self.name, keep, bk_color, self.input_color_image, visualization=True)
            self.color_block_path = color_block_path
            self.element_pathes = element_pathes
            for element_path in self.element_pathes:
                svg_name = generate_motif_pattern(element_path)
                self.svg_name = svg_name
                self.display_gengrate_images(self.svg_name, self.color_block_path)

        else:
            svg_name, color_block_path = generate_stripe_pattern(self.input_color_image, num=self.input_color_number)
            self.svg_name = svg_name
            self.color_block_path = color_block_path
            self.display_gengrate_images(self.svg_name, self.color_block_path)


    def regenerate_button_click(self):
        print("ReGenerate button被click了")
        self.input_pattern_type = self.PatternTypecomboBox.currentText()
        self.input_color_number = self.ColorSpinBox.value()
                
        if self.input_pattern_type == "Check":
            svg_name, color_block_path = generate_check_pattern(self.input_color_image, num=self.input_color_number)
            self.color_block_path = color_block_path
            self.display_gengrate_images(svg_name, color_block_path)
            
        elif self.input_pattern_type == "Motif":
            for element_path in self.element_pathes:
                svg_name = generate_motif_pattern(element_path)

                self.display_gengrate_images(svg_name, self.color_block_path)

        else:
            svg_name, color_block_path = generate_stripe_pattern(self.input_color_image, num=self.input_color_number)
            self.display_gengrate_images(svg_name, color_block_path)


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
        fileName, _ = QFileDialog.getOpenFileName(None, "Select Image File", "/home/zoe/ResearchProjects/DesignGenerationVector/data/color_ref",
                                                  "Image Files (*.png *.jpg *.jpeg)", options=options)

        if fileName:
            self.ColorReferenceImage.setPlainText(fileName.split("/")[-1])
            self.display_input_image(self.ColorRefView, fileName)
            self.input_color_image = cv2.imread(fileName, cv2.IMREAD_COLOR)


    def load_input_image(self):
        # Open file dialog to select image
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(None, "Select Image File", "/home/zoe/ResearchProjects/DesignGenerationVector/data/input",
                                                  "Image Files (*.png *.jpg *.jpeg)", options=options)

        if fileName:
            self.ColorReferenceImage.setPlainText(fileName.split("/")[-1])
            self.display_input_image(self.ImageInputView, fileName)
            self.input_design_image = cv2.imread(fileName, cv2.IMREAD_COLOR)
            self.name = fileName.split("/")[-1].split(".")[0]


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


    def display_input_image(self, view, file_path):
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


    def display_gengrate_images(self, svg_name, color_pallete_name):
        # Load and display the SVG
        svg_scene = QtWidgets.QGraphicsScene()
        self.svg_item = QtSvg.QGraphicsSvgItem(svg_name) 
        svg_scene.addItem(self.svg_item)
        self.graphicsView.setScene(svg_scene)  # Set the scene in the view
        # Fit the view to the initial size
        self.graphicsView.fitInView(svg_scene.sceneRect(),  QtCore.Qt.KeepAspectRatioByExpanding)

        # # switch to display png
        # svg2png_scene = QtWidgets.QGraphicsScene()
        # svg2png_image = QtGui.QPixmap(svg_name)
        # svg2png_scene.addPixmap(svg2png_image)
        # self.graphicsView.setScene(svg2png_scene)
        # self.graphicsView.fitInView(svg2png_scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

        # Load and display the PNG
        png_scene = QtWidgets.QGraphicsScene()
        png_image = QtGui.QPixmap(color_pallete_name) 
        png_scene.addPixmap(png_image)
        self.ColorPaletteView.setScene(png_scene)


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


    def scale_image(self):
        # Scale the SVG based on the scrollbar value
        if self.svg_item is not None:
            # Ensure the scale factor starts at 1 for the initial size
            min_scale = 1.0
            max_scale = 10.0  # Adjust as needed for maximum scaling
            scale_factor = min_scale + (self.ScaleScrollBar.value() - self.ScaleScrollBar.minimum()) / (self.ScaleScrollBar.maximum() - self.ScaleScrollBar.minimum()) * (max_scale - min_scale)
            
            self.svg_item.setScale(scale_factor)
            self.graphicsView.setSceneRect(self.svg_item.boundingRect())
            self.graphicsView.fitInView(self.graphicsView.sceneRect(), QtCore.Qt.KeepAspectRatioByExpanding)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
