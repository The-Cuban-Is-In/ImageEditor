from PIL import Image, ImageEnhance, ImageQt
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import sys
import os


class ImageEditor(qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        self.current_img = ['sewergogs.jpg']
        self.current_img_index = 0

        self.init_window()
        self.init_window_ui()
        self.show()

    def init_window(self):
        # Sets the window Geometry/title
        self.setGeometry(500, 50, 500, 800)
        self.setWindowTitle('Alter')
        self.setStyleSheet("""
            background: white;
            """)

    def init_window_ui(self):
        ##################TEMP##################
        ##################TEMP##################
        self.img = Image.open(self.current_img[self.current_img_index])
        self.pixmap = ImageQt.toqpixmap(self.img)
        self.scaled_img = self.pixmap.scaled(500, 800, qtc.Qt.KeepAspectRatio)
        ##################TEMP##################
        ##################TEMP##################

        # Sets up main layouts
        self.main_layout = qtw.QVBoxLayout()
        self.row_one_layout = qtw.QHBoxLayout()
        self.row_two_layout = qtw.QHBoxLayout()

        # sets up main picture label
        self.main_pic_label = qtw.QLabel(self)
        self.main_pic_label.setPixmap(self.scaled_img)
        self.main_pic_label.setStyleSheet("""
            border: 2px solid grey;
            """)

        # Sets up main buttons
        self.rotate_img_right = qtw.QPushButton('90R', clicked = lambda: self.rotate_img('R'))
        self.rotate_img_left = qtw.QPushButton('90L', clicked = lambda: self.rotate_img('L'))
        self.delete_img = qtw.QPushButton('Del', clicked = self.delete_current_img)
        self.edit_img = qtw.QPushButton('Edit', clicked = self.edit_options)

        # Sets widgets to layouts
        self.row_one_layout.addWidget(self.main_pic_label)
        self.row_two_layout.addWidget(self.delete_img)
        self.row_two_layout.addWidget(self.edit_img)
        self.row_two_layout.addWidget(self.rotate_img_left)
        self.row_two_layout.addWidget(self.rotate_img_right)
        


        # Sets Layouts to main layout
        self.main_layout.addLayout(self.row_one_layout)
        self.main_layout.addLayout(self.row_two_layout)
        self.setLayout(self.main_layout)

    def rotate_img(self, direction):
        if direction == 'L':
            self.img = self.img.rotate(90)
        else:
            self.img = self.img.rotate(-90)
        
        self.pixmap = ImageQt.toqpixmap(self.img)
        self.scaled_img = self.pixmap.scaled(500, 800, qtc.Qt.KeepAspectRatio)
        self.main_pic_label.setPixmap(self.scaled_img)

    def edit_options(self):
        pass

    def delete_current_img(self):
        pass


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main_window = ImageEditor()
    sys.exit(app.exec_())