# -*- coding:utf-8 -*-
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # 设置主窗口
        self.frame = QtWidgets.QFrame()
        self.vl = QtWidgets.QVBoxLayout()

        # VTK 窗口小部件
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        # 按钮：更改 OBJ 文件
        self.change_obj_button = QtWidgets.QPushButton("Load OBJ File")
        self.change_obj_button.clicked.connect(self.load_obj)
        self.vl.addWidget(self.change_obj_button)

        # 按钮：更改纹理
        self.change_texture_button = QtWidgets.QPushButton("Change Texture")
        self.change_texture_button.clicked.connect(self.change_texture)
        self.vl.addWidget(self.change_texture_button)

        self.setCentralWidget(self.frame)
        self.frame.setLayout(self.vl)

        # 渲染器和渲染窗口
        self.renderer = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)

        # 渲染窗口交互器
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # 初始化 OBJ 加载器
        self.obj_reader = vtk.vtkOBJReader()

        # 初始纹理
        self.texture = vtk.vtkTexture()

        # 初始化映射器和演员
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()

        # 设置初始状态
        self.actor.SetMapper(self.mapper)
        self.actor.SetTexture(self.texture)

        # 添加演员到渲染器
        self.renderer.AddActor(self.actor)
        self.renderer.SetBackground(1, 1, 1)  # 背景颜色

        # 初始化交互器
        self.iren.Initialize()
        self.show()

    def load_obj(self):
        """加载新的 OBJ 文件"""
        obj_file, _ = QFileDialog.getOpenFileName(
            self, "Select OBJ File", "", "OBJ Files (*.obj)"
        )

        if obj_file:  # 如果选择了有效文件
            print(f"Loading OBJ file: {obj_file}")

            # 加载 OBJ 文件
            self.obj_reader.SetFileName(obj_file)
            self.obj_reader.Update()

            # 设置映射器的输入
            self.mapper.SetInputConnection(self.obj_reader.GetOutputPort())
        
            # 调整摄像机，使模型居中
            self.renderer.ResetCamera()

            # 重新渲染场景以显示新的模型
            self.vtkWidget.GetRenderWindow().Render()

    def change_texture(self):
        """更改 OBJ 模型的纹理"""
        # 打开文件对话框以选择新的纹理图像
        texture_file, _ = QFileDialog.getOpenFileName(
            self, "Select Texture Image", "", "Image Files (*.jpg *.png *.bmp)"
        )

        if texture_file:  # 如果选择了有效文件
            print(f"New texture selected: {texture_file}")

            # 加载新的纹理
            if texture_file.endswith(".jpg") or texture_file.endswith(".jpeg"):
                texture_reader = vtk.vtkJPEGReader()
            elif texture_file.endswith(".png"):
                texture_reader = vtk.vtkPNGReader()
            elif texture_file.endswith(".bmp"):
                texture_reader = vtk.vtkBMPReader()
            else:
                print("Unsupported texture file format!")
                return

            texture_reader.SetFileName(texture_file)
            texture_reader.Update()

            # 设置纹理
            self.texture.SetInputConnection(texture_reader.GetOutputPort())
            self.texture.InterpolateOn()  # 启用纹理插值（更平滑）

            # 重新渲染场景以应用更改
            self.vtkWidget.GetRenderWindow().Render()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())