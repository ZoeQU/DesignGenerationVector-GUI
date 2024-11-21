#!/usr/bin/env python
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(250, 380)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # # 3D view
        self.label3DView = QtWidgets.QLabel(self.centralwidget)
        self.label3DView.setGeometry(QtCore.QRect(20, 20, 200, 20))
        self.label3DView.setObjectName("label3DView")
        self.ThreeDWidget = QVTKRenderWindowInteractor(self.centralwidget)
        self.ThreeDWidget.setGeometry(QtCore.QRect(20, 40, 200, 290))
        self.ThreeDWidget.setObjectName("ThreeDWidget")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # VTK Renderer setup
        self.vtk_renderer = vtk.vtkRenderer()
        self.ThreeDWidget.GetRenderWindow().AddRenderer(self.vtk_renderer)
        self.iren = self.ThreeDWidget.GetRenderWindow().GetInteractor()

        self.load_obj_model("/home/zoe/ResearchProjects/DesignGenerationVector/resources/3dModels/Shirt.obj")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TestWindow"))
        self.label3DView.setText(_translate("MainWindow", "3D View"))

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# region
# filename = "/home/zoe/ResearchProjects/DesignGenerationVector/resources/3dModels/Shirt.obj"
#
# reader = vtk.vtkOBJReader()
# reader.SetFileName(filename)
#
# mapper = vtk.vtkPolyDataMapper()
#
# mapper.SetInputConnection(reader.GetOutputPort())
#
# actor = vtk.vtkActor()
# actor.SetMapper(mapper)
#
# # Create a rendering window and renderer
# ren = vtk.vtkRenderer()
# renWin = vtk.vtkRenderWindow()
# renWin.AddRenderer(ren)  # ren
#
# # Create a renderwindowinteractor
# iren = vtk.vtkRenderWindowInteractor()
# iren.SetRenderWindow(renWin)
#
# # Assign actor to the renderer
# ren.AddActor(actor)
#
# # Enable user interface interactor
# iren.Initialize()
# renWin.Render()
# iren.Start()

# endregion