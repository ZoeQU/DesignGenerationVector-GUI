# -*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QSlider
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# from generator import generateMotif, generateCheck, generateStripe

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("Pattern Generator")
        self.setGeometry(100, 100, 800, 600)

        # 创建标签和下拉框
        self.keyword_label = QLabel("Pattern type:", self)
        self.keyword_label.move(75, 50)
        self.keyword_combobox = QComboBox(self)
        self.keyword_combobox.addItems(["motif", "stripe", "check"])
        self.keyword_combobox.move(150, 50)
        # self.keyword_combobox.currentTextChanged.connect(self.update_image)

        # 创建拖拽图片框
        self.small_image_label = QLabel(self)
        # self.small_image_label.setPixmap(QPixmap("small_image.png"))
        self.small_image_label.setGeometry(75, 100, 150, 150)
        self.small_image_label.setScaledContents(True)
        self.small_image_label.setAcceptDrops(True)
        self.small_image_label.setStyleSheet('border: 2px dashed gray')
        # Add a text label to the image label
        self.small_image_label_text = QLabel("Drag and drop design element here", self.small_image_label)
        self.small_image_label_text.setAlignment(Qt.AlignCenter)
        self.small_image_label_text.setGeometry(0, 0, 150, 150)
        self.small_image_label_text.setWordWrap(True)

        self.big_image_label = QLabel(self)
        self.big_image_label.setGeometry(75, 275, 200, 200)
        self.big_image_label.setScaledContents(True)
        self.big_image_label.setAcceptDrops(True)
        self.big_image_label.setStyleSheet('border: 2px dashed gray')
        # Add a text label to the image label
        self.big_image_label_text = QLabel("Drag and drop color reference image here", self.big_image_label)
        self.big_image_label_text.setAlignment(Qt.AlignCenter)
        self.big_image_label_text.setGeometry(0, 0, 200, 200)
        self.big_image_label_text.setWordWrap(True)

        # 创建生成图片框
        self.generated_image_label = QLabel(self)
        self.generated_image_label.setGeometry(325, 100, 380, 380)
        self.generated_image_label.setScaledContents(True)
        self.generated_image_label.setStyleSheet('border: 2px dashed gray')
        # Add a text label to the image label
        self.generated_image_label_text = QLabel("Generated image here", self.generated_image_label)
        self.generated_image_label_text.setAlignment(Qt.AlignCenter)
        self.generated_image_label_text.setGeometry(0, 0, 380, 380)

        # 创建生成,下载和重新生成按钮
        self.generate_button = QPushButton("Generate", self)
        self.generate_button.setGeometry(335, 500, 100, 50)
        self.generate_button.clicked.connect(self.generate_image)

        self.download_button = QPushButton("Download", self)
        self.download_button.setGeometry(465, 500, 100, 50)
        self.download_button.clicked.connect(self.download_image)

        self.regenerate_button = QPushButton("Regenerate", self)
        self.regenerate_button.setGeometry(595, 500, 100, 50)
        self.regenerate_button.clicked.connect(self.regenerate_image)

        # 创建可拖拽滑块
        self.slider1 = QSlider(Qt.Horizontal, self)
        self.slider1.setGeometry(85, 485, 190, 20)
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(100)
        self.slider1.setValue(50)
        self.slider1_label = QLabel("Scale", self)
        self.slider1_label.move(37, 480)

        self.slider2 = QSlider(Qt.Horizontal, self)
        self.slider2.setGeometry(85, 510, 190, 20)
        self.slider2.setMinimum(0)
        self.slider2.setMaximum(100)
        self.slider2.setValue(50)
        self.slider2_label = QLabel("Rotate", self)  # 修正为 slider2_label
        self.slider2_label.move(37, 505)

    # def update_image(self):
    #     # 根据下拉框的选项更新拖拽图片框
    #     keyword = self.keyword_combobox.currentText()
    #     if keyword == "motif":
    #         self.small_image_label.setPixmap(QPixmap("small_motif_image.png"))
    #         self.big_image_label.setPixmap(QPixmap("big_motif_image.png"))
    #         self.generated_image_label.setPixmap(QPixmap("big_motif_image.png"))
    #     elif keyword == "stripe":
    #         self.big_image_label.setPixmap(QPixmap("small_stripe_image.png"))
    #         self.generated_image_label.setPixmap(QPixmap("big_stripe_image.png"))
    #     else:
    #         self.big_image_label.setPixmap(QPixmap("small_check_image.png"))
    #         self.generated_image_label.setPixmap(QPixmap("big_check_image.png"))

    def download_image(self):
        # TODO: 实现下载图片的逻辑
        print("downloaded")

    def generate_image(self):
        # 在这里实现生成图片的功能，根据下拉选项框的值生成不同的图片
        pattern = self.keyword_combobox.currentText()
        if pattern == 'motif':
            # image = generateMotif()  # 调用生成motif图案的函数
            pass
        elif pattern == 'check':
            # image = generateCheck()  # 调用生成check图案的函数
            pass
        elif pattern == 'stripe':
            # image = generateStripe()  # 调用生成stripe图案的函数
            pass
        else:
            print("Out of generation range.")
            return

    def regenerate_image(self):
        # TODO: 实现renew图片的逻辑
        pass
        print("wait a moment")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())