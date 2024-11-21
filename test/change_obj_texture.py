import sys
from PyQt5 import QtWidgets
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        # Set up the main window
        self.frame = QtWidgets.QFrame()
        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
        
        self.setCentralWidget(self.frame)
        self.frame.setLayout(self.vl)

        # Create renderer and render window
        self.renderer = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)

        # Create render window interactor
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # Load the OBJ file
        obj_reader = vtk.vtkOBJReader()
        obj_reader.SetFileName("/home/zoe/ResearchProjects/DesignGenerationVector/resources/3dModels/Shirt.obj")
        
        # Load the texture image
        texture_reader = vtk.vtkJPEGReader()
        texture_reader.SetFileName("/home/zoe/ResearchProjects/DesignGenerationVector/resources/ColorReference/color_ref_0.jpg")

        # Create texture
        texture = vtk.vtkTexture()
        texture.SetInputConnection(texture_reader.GetOutputPort())

        # Create mapper and actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(obj_reader.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetTexture(texture)

        # Add the actor to the scene
        self.renderer.AddActor(actor)
        # self.renderer.SetBackground(0.1, 0.2, 0.3)  # Background color
        self.renderer.SetBackground(0, 0, 0)  # Background color

        self.iren.Initialize()
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())