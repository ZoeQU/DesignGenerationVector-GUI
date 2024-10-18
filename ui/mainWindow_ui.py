# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QLabel,
    QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy,
    QSlider, QSpinBox, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(746, 444)
        icon = QIcon()
        icon.addFile(u"ui/qu_icon_16x16.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.DownloadButton = QPushButton(self.centralwidget)
        self.DownloadButton.setObjectName(u"DownloadButton")
        self.DownloadButton.setGeometry(QRect(410, 400, 199, 23))
        self.ThreeDView = QLabel(self.centralwidget)
        self.ThreeDView.setObjectName(u"ThreeDView")
        self.ThreeDView.setGeometry(QRect(530, 40, 50, 15))
        self.ThreeDWidget = QOpenGLWidget(self.centralwidget)
        self.ThreeDWidget.setObjectName(u"ThreeDWidget")
        self.ThreeDWidget.setGeometry(QRect(520, 60, 199, 291))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ThreeDWidget.sizePolicy().hasHeightForWidth())
        self.ThreeDWidget.setSizePolicy(sizePolicy)
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(320, 60, 189, 291))
        self.TwoDView_2 = QLabel(self.centralwidget)
        self.TwoDView_2.setObjectName(u"TwoDView_2")
        self.TwoDView_2.setGeometry(QRect(330, 40, 50, 15))
        self.DesignElementView = QGraphicsView(self.centralwidget)
        self.DesignElementView.setObjectName(u"DesignElementView")
        self.DesignElementView.setGeometry(QRect(30, 120, 251, 91))
        self.ColorReferenceImage = QPlainTextEdit(self.centralwidget)
        self.ColorReferenceImage.setObjectName(u"ColorReferenceImage")
        self.ColorReferenceImage.setGeometry(QRect(30, 220, 165, 20))
        self.LoadColorReferenceImage = QPushButton(self.centralwidget)
        self.LoadColorReferenceImage.setObjectName(u"LoadColorReferenceImage")
        self.LoadColorReferenceImage.setGeometry(QRect(200, 220, 80, 20))
        self.LoadDesignElement = QPushButton(self.centralwidget)
        self.LoadDesignElement.setObjectName(u"LoadDesignElement")
        self.LoadDesignElement.setGeometry(QRect(200, 90, 80, 20))
        self.DesignEllement = QPlainTextEdit(self.centralwidget)
        self.DesignEllement.setObjectName(u"DesignEllement")
        self.DesignEllement.setGeometry(QRect(30, 90, 165, 20))
        self.ColorPaletteView = QGraphicsView(self.centralwidget)
        self.ColorPaletteView.setObjectName(u"ColorPaletteView")
        self.ColorPaletteView.setGeometry(QRect(162, 250, 127, 129))
        self.ColorRefView = QGraphicsView(self.centralwidget)
        self.ColorRefView.setObjectName(u"ColorRefView")
        self.ColorRefView.setGeometry(QRect(30, 250, 126, 129))
        self.ReGenerateButton = QPushButton(self.centralwidget)
        self.ReGenerateButton.setObjectName(u"ReGenerateButton")
        self.ReGenerateButton.setGeometry(QRect(169, 400, 82, 23))
        self.GenerateButton = QPushButton(self.centralwidget)
        self.GenerateButton.setObjectName(u"GenerateButton")
        self.GenerateButton.setGeometry(QRect(80, 400, 83, 23))
        self.ScaleScrollBar = QSlider(self.centralwidget)
        self.ScaleScrollBar.setObjectName(u"ScaleScrollBar")
        self.ScaleScrollBar.setGeometry(QRect(389, 370, 109, 15))
        self.ScaleScrollBar.setOrientation(Qt.Horizontal)
        self.Rotate = QLabel(self.centralwidget)
        self.Rotate.setObjectName(u"Rotate")
        self.Rotate.setGeometry(QRect(524, 370, 40, 15))
        self.RotateScrollBar = QSlider(self.centralwidget)
        self.RotateScrollBar.setObjectName(u"RotateScrollBar")
        self.RotateScrollBar.setGeometry(QRect(570, 370, 109, 15))
        self.RotateScrollBar.setOrientation(Qt.Horizontal)
        self.Scale = QLabel(self.centralwidget)
        self.Scale.setObjectName(u"Scale")
        self.Scale.setGeometry(QRect(350, 370, 33, 15))
        self.NumColor = QLabel(self.centralwidget)
        self.NumColor.setObjectName(u"NumColor")
        self.NumColor.setGeometry(QRect(30, 49, 127, 24))
        self.PatternTypecomboBox = QComboBox(self.centralwidget)
        self.PatternTypecomboBox.addItem("")
        self.PatternTypecomboBox.addItem("")
        self.PatternTypecomboBox.addItem("")
        self.PatternTypecomboBox.setObjectName(u"PatternTypecomboBox")
        self.PatternTypecomboBox.setGeometry(QRect(163, 20, 126, 23))
        self.ColorSpinBox = QSpinBox(self.centralwidget)
        self.ColorSpinBox.setObjectName(u"ColorSpinBox")
        self.ColorSpinBox.setGeometry(QRect(163, 49, 126, 24))
        self.ColorSpinBox.setValue(3)
        self.ColorSpinBox.setDisplayIntegerBase(10)
        self.PatternType = QLabel(self.centralwidget)
        self.PatternType.setObjectName(u"PatternType")
        self.PatternType.setGeometry(QRect(30, 20, 127, 23))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.DownloadButton.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.ThreeDView.setText(QCoreApplication.translate("MainWindow", u"3D View", None))
        self.TwoDView_2.setText(QCoreApplication.translate("MainWindow", u"2D View", None))
        self.ColorReferenceImage.setPlainText(QCoreApplication.translate("MainWindow", u"Color Reference Image", None))
        self.LoadColorReferenceImage.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.LoadDesignElement.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.DesignEllement.setPlainText(QCoreApplication.translate("MainWindow", u"Design Element", None))
        self.ReGenerateButton.setText(QCoreApplication.translate("MainWindow", u"ReGenerate", None))
        self.GenerateButton.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.Rotate.setText(QCoreApplication.translate("MainWindow", u"Rotate", None))
        self.Scale.setText(QCoreApplication.translate("MainWindow", u"Scale", None))
        self.NumColor.setText(QCoreApplication.translate("MainWindow", u"Number of Color:", None))
        self.PatternTypecomboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Motif", None))
        self.PatternTypecomboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Check", None))
        self.PatternTypecomboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Stripe", None))

        self.PatternType.setText(QCoreApplication.translate("MainWindow", u"Pattern Type:", None))
    # retranslateUi

