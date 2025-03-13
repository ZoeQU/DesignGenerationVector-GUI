# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QMainWindow, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PIL import Image
import subprocess
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
from src.generation.single_iga import SignleGA
from src.generation.multiple_iga import MultipleGA

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
        self.svg_names = []
        self.current_actor = None 
        self.selected_indices = []

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1010, 510)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/qu_icon_16x16.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Threhold scrollbar
        self.ScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.ScrollBar.setGeometry(QtCore.QRect(90, 88, 140, 15))  # Position below the download button
        # self.ScrollBar.setGeometry(QtCore.QRect(155, 83, 90, 15))  # Position below the download button
        self.ScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.ScrollBar.setMinimum(-10)  # Set the scroll bar's minimum value
        self.ScrollBar.setMaximum(10)   # Set the scroll bar's maximum value
        self.ScrollBar.setValue(0)     # Default value
        self.ScrollBar.setSingleStep(1)  # Smallest step
        
        # Label for scrollbar value
        self.ScrollBarValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.ScrollBarValueLabel.setGeometry(QtCore.QRect(245, 85, 60, 15))  # Position next to the scrollbar
        # self.ScrollBarValueLabel.setGeometry(QtCore.QRect(225, 83, 60, 15))  # Position next to the scrollbar
        self.ScrollBarValueLabel.setObjectName("ScrollBarValueLabel")
        self.ScrollBarValueLabel.setText("0.0")  # Default text

        # Connect scrollbar value change to the update function
        self.ScrollBar.valueChanged.connect(self.update_scrollbar_value)

        # Show "Hint" message
        self.Hint = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.Hint.setGeometry(QtCore.QRect(50, 105, 270, 60))
        self.Hint.setObjectName("SvgOutput")
        self.Hint.setPlainText("Hint: Higher similarity thresholds yield more design elements.") 
        self.Hint.setStyleSheet("border: none; background: transparent;")
        self.Hint.setReadOnly(True) 

        # Load "input raster image" text
        self.ImageInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ImageInput.setGeometry(QtCore.QRect(40, 145, 80, 25))
        self.ImageInput.setObjectName("ImageInput")

        # Load "input raster image" button
        self.LoadImageInput = QtWidgets.QPushButton(self.centralwidget)
        self.LoadImageInput.setGeometry(QtCore.QRect(125, 145, 50, 25))
        self.LoadImageInput.setObjectName("LoadImageInput")
        self.LoadImageInput.setText("Load")
        self.LoadImageInput.clicked.connect(self.load_input_image)

        # "input raster image" view
        self.ImageInputView = QtWidgets.QGraphicsView(self.centralwidget)
        self.ImageInputView.setGeometry(QtCore.QRect(40, 175, 130, 120))
        self.ImageInputView.setObjectName("InputImageView")
        
        # Color reference image text
        self.ColorReferenceImage = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ColorReferenceImage.setGeometry(QtCore.QRect(185, 145, 80, 25))
        self.ColorReferenceImage.setObjectName("ColorReferenceImage")

        # Load color reference image button
        self.LoadColorReferenceImage = QtWidgets.QPushButton(self.centralwidget)
        self.LoadColorReferenceImage.setGeometry(QtCore.QRect(270, 145, 50, 25))
        self.LoadColorReferenceImage.setObjectName("LoadColorReferenceImage")
        self.LoadColorReferenceImage.setText("Load")
        self.LoadColorReferenceImage.clicked.connect(self.load_color_reference_image)

        # Color reference image view
        self.ColorRefView = QtWidgets.QGraphicsView(self.centralwidget)
        self.ColorRefView.setGeometry(QtCore.QRect(187, 175, 130, 120))
        self.ColorRefView.setObjectName("ColorRefView")

        # Color palette text
        self.ColorPaletteText = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ColorPaletteText.setGeometry(QtCore.QRect(40, 302, 278, 25))
        self.ColorPaletteText.setObjectName("ColorPaletteText")

        # Color palette view
        self.ColorPaletteView = QtWidgets.QGraphicsView(self.centralwidget)
        self.ColorPaletteView.setGeometry(QtCore.QRect(40, 330, 278, 110))
        self.ColorPaletteView.setObjectName("ColorPaletteView")
        
        # generate button
        self.GenerateButton = QtWidgets.QPushButton(self.centralwidget)
        self.GenerateButton.setGeometry(QtCore.QRect(70, 450, 85, 25))
        self.GenerateButton.setObjectName("GenerateButton")
        self.GenerateButton.clicked.connect(self.generate_button_click)

        # regenerate button
        self.ReGenerateButton = QtWidgets.QPushButton(self.centralwidget)
        self.ReGenerateButton.setGeometry(QtCore.QRect(180, 450, 85, 25))
        self.ReGenerateButton.setObjectName("ReGenerateButton")
        self.ReGenerateButton.clicked.connect(self.regenerate_button_click)

        # pattern type 
        self.PatternType = QtWidgets.QLabel(self.centralwidget)
        self.PatternType.setGeometry(QtCore.QRect(40, 25, 125, 25))
        self.PatternType.setObjectName("PatternType")

        # pattern type combo box
        self.PatternTypecomboBox = QtWidgets.QComboBox(self.centralwidget)
        self.PatternTypecomboBox.setGeometry(QtCore.QRect(175, 25, 125, 25))
        self.PatternTypecomboBox.setObjectName("PatternTypecomboBox")
        self.PatternTypecomboBox.addItem("")
        self.PatternTypecomboBox.addItem("")
        self.PatternTypecomboBox.addItem("")

        # num of color
        self.NumColor = QtWidgets.QLabel(self.centralwidget)
        self.NumColor.setGeometry(QtCore.QRect(40, 55, 125, 25))
        self.NumColor.setObjectName("NumColor")

        # color spin box
        self.ColorSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.ColorSpinBox.setGeometry(QtCore.QRect(175, 55, 125, 25))
        self.ColorSpinBox.setProperty("value", 3)
        self.ColorSpinBox.setDisplayIntegerBase(10)
        self.ColorSpinBox.setMinimum(2) 
        self.ColorSpinBox.setMaximum(9) 
        self.ColorSpinBox.setObjectName("ColorSpinBox")

        # 2D view：display window + checkbox
        self.label2DView = QtWidgets.QLabel(self.centralwidget)
        self.label2DView.setGeometry(QtCore.QRect(350, 40, 200, 15))
        self.label2DView.setObjectName("label2DView")

        self.graphicsView11 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView11.setGeometry(QtCore.QRect(350, 70, 120, 130))
        self.graphicsView11.setObjectName("graphicsView11")

        self.CheckBox11 = QtWidgets.QCheckBox(self.centralwidget)
        self.CheckBox11.setGeometry(QtCore.QRect(370, 210, 120, 20))  # 设置位置和大小
        self.CheckBox11.setObjectName("CheckBox11")
        self.CheckBox11.setText("Satisfied")

        self.graphicsView12 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView12.setGeometry(QtCore.QRect(480, 70, 120, 130))
        self.graphicsView12.setObjectName("graphicsView12")

        self.CheckBox12 = QtWidgets.QCheckBox(self.centralwidget)
        self.CheckBox12.setGeometry(QtCore.QRect(500, 210, 120, 20))  # 设置位置和大小
        self.CheckBox12.setObjectName("CheckBox12")
        self.CheckBox12.setText("Satisfied")

        self.graphicsView13 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView13.setGeometry(QtCore.QRect(610, 70, 120, 130))
        self.graphicsView13.setObjectName("graphicsView13")
        
        self.CheckBox13 = QtWidgets.QCheckBox(self.centralwidget)
        self.CheckBox13.setGeometry(QtCore.QRect(630, 210, 120, 20))  # 设置位置和大小
        self.CheckBox13.setObjectName("CheckBox13")
        self.CheckBox13.setText("Satisfied")

        self.graphicsView21 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView21.setGeometry(QtCore.QRect(350, 260, 120, 130))
        self.graphicsView21.setObjectName("graphicsView21")

        self.CheckBox21 = QtWidgets.QCheckBox(self.centralwidget)
        self.CheckBox21.setGeometry(QtCore.QRect(370, 400, 120, 20))  # 设置位置和大小
        self.CheckBox21.setObjectName("CheckBox21")
        self.CheckBox21.setText("Satisfied")

        self.graphicsView22 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView22.setGeometry(QtCore.QRect(480, 260, 120, 130))
        self.graphicsView22.setObjectName("graphicsView22")

        self.CheckBox22 = QtWidgets.QCheckBox(self.centralwidget)
        self.CheckBox22.setGeometry(QtCore.QRect(500, 400, 120, 20))  # 设置位置和大小
        self.CheckBox22.setObjectName("CheckBox22")
        self.CheckBox22.setText("Satisfied")

        self.graphicsView23 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView23.setGeometry(QtCore.QRect(610, 260, 120, 130))
        self.graphicsView23.setObjectName("graphicsView23")

        self.CheckBox23 = QtWidgets.QCheckBox(self.centralwidget)
        self.CheckBox23.setGeometry(QtCore.QRect(630, 400, 120, 20))  # 设置位置和大小
        self.CheckBox23.setObjectName("CheckBox23")
        self.CheckBox23.setText("Satisfied")

        # Connect checkboxes to their respective slots
        self.CheckBox11.stateChanged.connect(self.checkbox11_state_changed)
        self.CheckBox12.stateChanged.connect(self.checkbox12_state_changed)
        self.CheckBox13.stateChanged.connect(self.checkbox13_state_changed)
        self.CheckBox21.stateChanged.connect(self.checkbox21_state_changed)
        self.CheckBox22.stateChanged.connect(self.checkbox22_state_changed)
        self.CheckBox23.stateChanged.connect(self.checkbox23_state_changed)

        # download button
        self.DownloadButton = QtWidgets.QPushButton(self.centralwidget)
        self.DownloadButton.setGeometry(QtCore.QRect(430, 450, 200, 23))
        self.DownloadButton.setObjectName("DownloadButton")
        self.DownloadButton.clicked.connect(self.download_button_click)

        # # 3D view
        self.label3DView = QtWidgets.QLabel(self.centralwidget)
        self.label3DView.setGeometry(QtCore.QRect(750, 40, 225, 25))
        self.label3DView.setObjectName("label3DView")
        self.ThreeDWidget = QVTKRenderWindowInteractor(self.centralwidget)
        self.ThreeDWidget.setGeometry(QtCore.QRect(750, 70, 225, 340))
        self.ThreeDWidget.setObjectName("ThreeDWidget")

        # Load OBJ button
        self.LoadOBJButton = QtWidgets.QPushButton(self.centralwidget)
        self.LoadOBJButton.setGeometry(QtCore.QRect(760, 450, 95, 20))
        self.LoadOBJButton.setObjectName("LoadOBJButton")
        self.LoadOBJButton.setText("Load OBJ")
        self.LoadOBJButton.clicked.connect(self.load_obj)

        # Load Texture button
        self.LoadTextureButton = QtWidgets.QPushButton(self.centralwidget)
        self.LoadTextureButton.setGeometry(QtCore.QRect(870, 450, 92, 20))
        self.LoadTextureButton.setObjectName("LoadTextureButton")
        self.LoadTextureButton.setText("Load Texture")
        self.LoadTextureButton.clicked.connect(self.change_texture)
        
        # VTK Renderer setup
        self.vtk_renderer = vtk.vtkRenderer()
        self.vtk_renderer.SetBackground(0.5, 0.5, 0.5) 
        self.ThreeDWidget.GetRenderWindow().AddRenderer(self.vtk_renderer)
        self.iren = self.ThreeDWidget.GetRenderWindow().GetInteractor()

        # Load OBJ model
        self.load_obj_model("/home/zoe/ResearchProjects/DesignGenerationVector/resources/3dModels/cube.obj")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Vector Pattern Auto-Generation"))
        self.DownloadButton.setText(_translate("MainWindow", "Download"))
        self.LoadOBJButton.setText(_translate("MainWindow", "Load Obj"))
        self.LoadTextureButton.setText(_translate("MainWindow", "Load Texture"))
        self.label3DView.setText(_translate("MainWindow", "3D View"))
        self.label2DView.setText(_translate("MainWindow", "Generate Pattern: 2D View"))
        self.ColorReferenceImage.setPlainText(_translate("MainWindow", "ColorRef"))
        self.LoadColorReferenceImage.setText(_translate("MainWindow", "Load"))
        self.LoadImageInput.setText(_translate("MainWindow", "Load"))
        self.ImageInput.setPlainText(_translate("MainWindow", "Input"))
        self.ColorPaletteText.setPlainText(_translate("MainWindow", "Color Palette"))
        self.ReGenerateButton.setText(_translate("MainWindow", "ReGenerate"))
        self.GenerateButton.setText(_translate("MainWindow", "Generate"))
        # self.Rotate.setText(_translate("MainWindow", "Rotate"))
        # self.Scale.setText(_translate("MainWindow", "Scale"))
        self.NumColor.setText(_translate("MainWindow", "Number of Color:"))
        self.PatternTypecomboBox.setItemText(0, _translate("MainWindow", "Motif"))
        self.PatternTypecomboBox.setItemText(1, _translate("MainWindow", "Check"))
        self.PatternTypecomboBox.setItemText(2, _translate("MainWindow", "Stripe"))
        self.PatternType.setText(_translate("MainWindow", "Pattern Type:"))


    def convert_svg_to_png(self, svg_path, jpg_name):
        """Convert an SVG file to PNG using rsvg-convert."""
        try:
            background_color=(255, 255, 255)
            # 临时 PNG 文件路径
            temp_png = jpg_name.replace(".jpg", ".png")

            # 使用 Inkscape 命令行导出 PNG
            command = [
                "inkscape",
                svg_path,
                "--export-png", temp_png,  # 导出为 PNG
                "--export-dpi", str(96),  # 设置分辨率
                "--export-area-drawing"   # 导出绘图区域
            ]
            subprocess.run(command, check=True)
            print(f"Successfully exported SVG to PNG: {temp_png}")

            # 使用 Pillow 将 PNG 转换为 JPG
            with Image.open(temp_png) as img:
                rgb_image = Image.new("RGB", img.size, background_color)
                rgb_image.paste(img, mask=img.split()[3])  # 使用 alpha 通道作为掩码
                rgb_image.save(jpg_name, "JPEG", quality=95)
            print(f"Successfully converted PNG to JPG: {jpg_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error during SVG to PNG conversion: {e}")
        except Exception as e:
            print(f"Error during PNG to JPG conversion: {e}")


    def download_button_click(self):
        print("Download button被click了")
        try:
            # Let the user choose a folder (pass `self` as the parent)
            folder_path = QFileDialog.getExistingDirectory(None, "Select Folder to Save Images", "/home/zoe/ResearchProjects/DesignGenerationVector/data/temp/temp_save")
            if not folder_path:
                QMessageBox.warning(None, "Warning", "No folder selected!", QMessageBox.Ok)
                return

            # # Save the PNG and SVG files
            # # print(self.svg_name)
            # svg_name = self.svg_name
            # jpg_name = svg_name.split('.')[0] + '.jpg'
            # # print(png_name)

            # self.convert_svg_to_png(svg_name, jpg_name)
            
            # self.save_file(self.color_block_path, folder_path)
            # self.save_file(self.svg_name, folder_path)
            # self.save_file(jpg_name, folder_path)


            # 检查是否有用户选择的图案
            if not hasattr(self, "selected_indices") or not self.selected_indices:
                QMessageBox.warning(None, "Warning", "No designs selected for download!", QMessageBox.Ok)
                return

            # 遍历用户选择的索引，保存相应的图案
            for index in self.selected_indices:
                if hasattr(self, "svg_names") and index < len(self.svg_names):
                    svg_name = self.svg_names[index]  # 获取对应的 SVG 文件
                    jpg_name = svg_name.split('.')[0] + '.jpg'  # 转换为 JPG 文件名

                    # 转换 SVG 为 PNG/JPG
                    self.convert_svg_to_png(svg_name, jpg_name)

                    # 保存文件到目标文件夹
                    self.save_file(self.color_block_path, folder_path)
                    self.save_file(svg_name, folder_path)  # 保存 SVG
                    self.save_file(jpg_name, folder_path)  # 保存 JPG

            # Show success message
            QMessageBox.information(None, "Success", f"All images have been saved to:\n{folder_path}", QMessageBox.Ok)

        except Exception as e:
            # Display error message if something goes wrong
            QMessageBox.critical(None, "Error", f"An error occurred while saving files: {str(e)}", QMessageBox.Ok)
    

    def update_scrollbar_value(self):
        value = self.ScrollBar.value()  
        float_value = value / 10.0 
        self.thre = float_value
        print(self.thre)
        self.ScrollBarValueLabel.setText(f"{float_value:.2f}")


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
        
        if self.input_pattern_type == "Check":
            savenames, color_block_path = generate_check_pattern(self.input_color_image, num=self.input_color_number)
            self.svg_names = savenames
            self.color_block_path = color_block_path
            self.display_gengrate_images(self.svg_names, self.color_block_path)
            
        elif self.input_pattern_type == "Motif":
            self.svg_name = savePath + "motif_generate.svg"
            bk_color, keep  = extractor(self.input_design_image, self.name, self.thre, visualization=True)
            element_pathes, color_block_path = vectorize_design_element(self.name, keep, bk_color, self.input_color_image, visualization=True)
            self.color_block_path = color_block_path
            self.element_pathes = element_pathes

            if len(self.element_pathes) > 1:
                self.multiple_ga = MultipleGA(self.svg_name, self.element_pathes)
                self.svg_names = self.multiple_ga.generate_pattern()
            else:
                self.single_ga = SignleGA(self.svg_name, self.element_pathes[0])
                self.svg_names = self.single_ga.generate_pattern()

            # # stright, tile, half-drop, mirror
            # svg_name = generate_motif_pattern(self.element_pathes)
            # self.svg_name = svg_name
            # self.display_gengrate_images(self.svg_name, self.color_block_path)
            # for element_path in self.element_pathes:
            #     svg_name = generate_motif_pattern(element_path)
            #     self.svg_name = svg_name
                
            self.display_gengrate_images(self.svg_names, self.color_block_path)

        else:  # generate stripe pattern
            savenames, color_block_path = generate_stripe_pattern(self.input_color_image, num=self.input_color_number)
            self.svg_names = savenames
            self.color_block_path = color_block_path
            self.display_gengrate_images(self.svg_names, self.color_block_path)


    def regenerate_button_click(self):
        print("ReGenerate button被click了")
        self.input_pattern_type = self.PatternTypecomboBox.currentText()
        self.input_color_number = self.ColorSpinBox.value()
                
        if self.input_pattern_type == "Check":
            svg_name, color_block_path = generate_check_pattern(self.input_color_image, num=self.input_color_number)
            self.color_block_path = color_block_path
            self.display_gengrate_images(svg_name, color_block_path)
            
        elif self.input_pattern_type == "Motif":
            # if hasattr(self, "single_ga") and self.single_ga:  # 确保 SignleGA 已初始化
            #     next_gen_svg_names = self.single_ga.generate_next_iteration(self.selected_indices)
            #     self.display_gengrate_images(next_gen_svg_names)

            # elif hasattr(self, "multiple_ga") and self.multiple_ga:  # 确保 MultipleGA 已初始化
            #     next_gen_svg_names = self.multiple_ga.generate_next_iteration(self.selected_indices)
            #     self.display_gengrate_images(next_gen_svg_names)
            
            # 根据用户选择生成下一代
            if hasattr(self, "multiple_ga") and hasattr(self, "selected_indices"):
                next_svg_names = self.multiple_ga.generate_next_iteration(self.selected_indices)
                self.svg_names = next_svg_names  # 更新当前代的图案文件
                self.display_gengrate_images(self.svg_names, self.color_block_path)  # 显示生成的图案

            elif hasattr(self, "single_ga") and hasattr(self, "selected_indices"):
                next_svg_names = self.single_ga.generate_next_iteration(self.selected_indices)
                self.svg_names = next_svg_names  # 更新当前代的图案文件
                self.display_gengrate_images(self.svg_names, self.color_block_path)  # 显示生成的图案
                
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


    def display_gengrate_images(self, svg_names, color_pallete_name):
        """展示生成的 6 个图案"""
        # 确保 `svg_names` 是一个包含 6 个路径的列表
        if len(svg_names) != 6:
            print("Error: Please provide exactly 6 SVG file paths.")
            return

        # 展示图案的函数
        def display_svg(graphics_view, svg_name):
            if not os.path.exists(svg_name):  # 检查文件是否存在
                print(f"Error: File {svg_name} does not exist.")
                return
            
            svg_scene = QtWidgets.QGraphicsScene()
            svg_item = QtSvg.QGraphicsSvgItem(svg_name)
            svg_scene.addItem(svg_item)
            graphics_view.setScene(svg_scene)
            graphics_view.fitInView(svg_scene.sceneRect(), QtCore.Qt.KeepAspectRatioByExpanding)

        # 分别展示 6 个图案
        display_svg(self.graphicsView11, svg_names[0])  # 显示第 1 个图案
        display_svg(self.graphicsView12, svg_names[1])  # 显示第 2 个图案
        display_svg(self.graphicsView13, svg_names[2])  # 显示第 3 个图案
        display_svg(self.graphicsView21, svg_names[3])  # 显示第 4 个图案
        display_svg(self.graphicsView22, svg_names[4])  # 显示第 5 个图案
        display_svg(self.graphicsView23, svg_names[5])  # 显示第 6 个图案
        
        # Load and display the PNG
        png_scene = QtWidgets.QGraphicsScene()
        png_image = QtGui.QPixmap(color_pallete_name) 
        png_scene.addPixmap(png_image)
        self.ColorPaletteView.setScene(png_scene)
    

    def load_obj_model(self, filename):
        """Load and display an OBJ file."""
        if self.current_actor:
            self.vtk_renderer.RemoveActor(self.current_actor)

        reader = vtk.vtkOBJReader()
        reader.SetFileName(filename)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        self.current_actor = actor
        self.vtk_renderer.AddActor(self.current_actor)
        self.vtk_renderer.ResetCamera()
        self.ThreeDWidget.GetRenderWindow().Render()


    def load_obj(self):
        """Open file dialog to load a new OBJ file."""
        filename, _ = QFileDialog.getOpenFileName(None, "Open OBJ File", "/home/zoe/ResearchProjects/DesignGenerationVector/resources/3dModels", "OBJ Files (*.obj)")

        if filename:
            self.load_obj_model(filename)


    def change_texture(self):
        """Apply a texture to the current OBJ model."""
        if not self.current_actor:
            QtWidgets.QMessageBox.warning(None, "No Model", "Please load a model first.")
            return

        filename, _ = QFileDialog.getOpenFileName(None, "Open Texture File", "/home/zoe/ResearchProjects/DesignGenerationVector/data/temp/temp_save", "Image Files (*.png *.jpg *.bmp)")
        if filename:
            texture = vtk.vtkTexture()
            if filename.lower().endswith(".png"):
                reader = vtk.vtkPNGReader()
            elif filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
                reader = vtk.vtkJPEGReader()
            else:
                QtWidgets.QMessageBox.warning(None, "Unsupported Format", "Only PNG and JPG formats are supported.")
                return
            reader.SetFileName(filename)
            texture.SetInputConnection(reader.GetOutputPort())
            self.current_actor.SetTexture(texture)
            self.ThreeDWidget.GetRenderWindow().Render()


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


    def checkbox11_state_changed(self, state):
        if state == QtCore.Qt.Checked:
            self.selected_indices.append(0)  # 对应第 1 个图案
        else:
            if 0 in self.selected_indices:
                self.selected_indices.remove(0)

    def checkbox12_state_changed(self, state):
        if state == QtCore.Qt.Checked:
            self.selected_indices.append(1)  # 对应第 2 个图案
        else:
            if 1 in self.selected_indices:
                self.selected_indices.remove(1)

    def checkbox13_state_changed(self, state):
        if state == QtCore.Qt.Checked:
            self.selected_indices.append(2)  # 对应第 3 个图案
        else:
            if 2 in self.selected_indices:
                self.selected_indices.remove(2)

    def checkbox21_state_changed(self, state):
        if state == QtCore.Qt.Checked:
            self.selected_indices.append(3)  # 对应第 4 个图案
        else:
            if 3 in self.selected_indices:
                self.selected_indices.remove(3)

    def checkbox22_state_changed(self, state):
        if state == QtCore.Qt.Checked:
            self.selected_indices.append(4)  # 对应第 5 个图案
        else:
            if 4 in self.selected_indices:
                self.selected_indices.remove(4)

    def checkbox23_state_changed(self, state):
        if state == QtCore.Qt.Checked:
            self.selected_indices.append(5)  # 对应第 6 个图案
        else:
            if 5 in self.selected_indices:
                self.selected_indices.remove(5)
                
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
