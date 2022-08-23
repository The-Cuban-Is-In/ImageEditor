from ast import Delete
from PIL import Image, ImageEnhance, ImageQt, ImageFilter
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import sys
import os


class ImageEditor(qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        self.current_img = ['dark-image.jpg']
        self.current_img_index = 0
        self.bw_on_off = 0  # onoff for black/white
        self.em_on_off = 0  # onoff for emboss
        self.sm_on_off = 0  # onoff for smooth

        self.init_window()
        self.init_main_ui()
        self.show()

    def init_window(self):
        # Sets the window Geometry/title
        self.setGeometry(500, 50, 500, 800)
        self.setWindowTitle('Alter')
        self.setStyleSheet("""
            QWidget {background: black;}
            QPushButton {
                        color: white;
                        background-color: rgba(0, 0, 0, 0)
                        }
            """)

    def init_main_ui(self):
        ##################TEMP##################
        ##################TEMP##################
        self.origional_img = Image.open(self.current_img[self.current_img_index])
        self.img = self.origional_img
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
        self.rotate_img_right = qtw.QPushButton(clicked = lambda: self.rotate_img('R'))
        self.rotate_img_right.setIcon(qtg.QIcon(os.path.join('icons', 'rotate-right.png'))) 

        self.rotate_img_left = qtw.QPushButton(clicked = lambda: self.rotate_img('L'))
        self.rotate_img_left.setIcon(qtg.QIcon(os.path.join('icons', 'rotate-left.png')))

        self.edit_img = qtw.QPushButton(clicked = self.edit_options)
        self.edit_img.setIcon(qtg.QIcon(os.path.join('icons', 'edit-icon.png')))

        self.save_img_btn = qtw.QPushButton()
        self.save_img_btn.setIcon(qtg.QIcon(os.path.join('icons', 'save-icon.png')))

        # Sets widgets to layouts
        self.row_one_layout.addWidget(self.main_pic_label)
        self.row_two_layout.addWidget(self.rotate_img_left)
        self.row_two_layout.addWidget(self.edit_img)
        self.row_two_layout.addWidget(self.save_img_btn)
        self.row_two_layout.addWidget(self.rotate_img_right)

        # Sets Layouts to main layout
        self.main_layout.addLayout(self.row_one_layout)
        self.main_layout.addLayout(self.row_two_layout)
        self.setLayout(self.main_layout)
    
    def hide_home_options(self):
        self.rotate_img_left.hide()
        self.rotate_img_right.hide()
        self.edit_img.hide()
        self.save_img_btn.hide()
    
    def show_home_options(self):
        self.rotate_img_left.show()
        self.rotate_img_right.show()
        self.edit_img.show()
        self.save_img_btn.show()

    def rotate_img(self, direction):
        if direction == 'L':
            self.img = self.img.rotate(90)
        else:
            self.img = self.img.rotate(-90)
        
        self.pixmap = ImageQt.toqpixmap(self.img)
        self.scaled_img = self.pixmap.scaled(500, 800, qtc.Qt.KeepAspectRatio)
        self.main_pic_label.setPixmap(self.scaled_img)
    
    def edit_options(self):
        self.hide_home_options()

        # create new buttons (back, brighten, crop, grey scale)
        self.back_btn = qtw.QPushButton(clicked = self.return_home)
        self.back_btn.setIcon(qtg.QIcon(os.path.join('icons', 'back-icon.png')))

        self.brightness_btn = qtw.QPushButton(clicked = self.brighten_options)
        self.brightness_btn.setIcon(qtg.QIcon(os.path.join('icons', 'brightness-icon.png')))

        self.crop_btn = qtw.QPushButton(clicked = self.crop_options)
        self.crop_btn.setIcon(qtg.QIcon(os.path.join('icons', 'crop-icon.png')))

        self.filter_btn = qtw.QPushButton(clicked = self.filter_options)
        self.filter_btn.setIcon(qtg.QIcon(os.path.join('icons', 'filter-icon.png')))

        # add new buttons to layout
        self.row_two_layout.addWidget(self.back_btn)
        self.row_two_layout.addWidget(self.brightness_btn)
        self.row_two_layout.addWidget(self.crop_btn)
        self.row_two_layout.addWidget(self.filter_btn)
    
    def hide_edit_options(self):
        self.back_btn.hide()
        self.brightness_btn.hide()
        self.crop_btn.hide()
        self.filter_btn.hide()

    def show_edit_options(self):
        self.back_btn.show()
        self.brightness_btn.show()
        self.crop_btn.show()
        self.filter_btn.show()

    def return_home(self):
        self.hide_edit_options()
        self.show_home_options()

    def brighten_options(self):
        self.hide_edit_options()

        self.back_to_edit = qtw.QPushButton(clicked = self.return_edit)
        self.back_to_edit.setIcon(qtg.QIcon(os.path.join('icons', 'back-icon.png')))

        self.bright_slider = qtw.QSlider(qtc.Qt.Horizontal)
        self.bright_slider.setMaximum(10)
        self.bright_slider.setMinimum(0)
        self.bright_slider.setValue(2)
        self.bright_slider.setTickPosition(qtw.QSlider.TicksBothSides)
        self.bright_slider.valueChanged.connect(self.bright_img)
   
        self.row_two_layout.addWidget(self.back_to_edit)
        self.row_two_layout.addWidget(self.bright_slider)

    def remove_bright_options(self):
        self.row_two_layout.removeWidget(self.back_to_edit)
        del self.back_to_edit
        self.row_two_layout.removeWidget(self.bright_slider)
        del self.bright_slider

    def bright_img(self):
        enhancer = ImageEnhance.Brightness(self.img)
        factor = self.bright_slider.value() - 0.5
        img_output = enhancer.enhance(factor)
        self.pixmap = ImageQt.toqpixmap(img_output)
        self.scaled_img = self.pixmap.scaled(500, 800, qtc.Qt.KeepAspectRatio)
        self.main_pic_label.setPixmap(self.scaled_img)

    def crop_options(self):
        self.hide_edit_options()

    def filter_options(self):
        self.hide_edit_options()

        self.back_to_edit = qtw.QPushButton(clicked = self.return_edit)
        self.back_to_edit.setIcon(qtg.QIcon(os.path.join('icons', 'back-icon.png')))

        self.black_white_btn = qtw.QPushButton('Black & White', 
            clicked = self.black_white_img)
        self.black_white_btn.setStyleSheet("""
            border: 2px solid white;
            border-radius: 10px
            """)

        self.emboss_btn = qtw.QPushButton('Emboss',
            clicked = self.emboss_img)
        self.emboss_btn.setStyleSheet("""
            border: 2px solid white;
            border-radius: 50px
            """)
            
        self.smooth_btn = qtw.QPushButton('Smooth',
            clicked = self.smooth_img)
        self.smooth_btn.setStyleSheet("""
            border: 2px solid white;
            border-radius: 50px
            """)

        self.row_two_layout.addWidget(self.back_to_edit)
        self.row_two_layout.addWidget(self.black_white_btn)
        self.row_two_layout.addWidget(self.emboss_btn)
        self.row_two_layout.addWidget(self.smooth_btn)
    
    def black_white_img(self):
        self.em_on_off = 0
        self.sm_on_off = 0

        if self.bw_on_off == 0:
            self.temp = self.img
            self.temp = self.temp.convert('L')
            self.pixmap = ImageQt.toqpixmap(self.temp)
            self.bw_on_off = 1
        else:
            self.pixmap = ImageQt.toqpixmap(self.img)
            self.bw_on_off = 0

        self.scaled_img = self.pixmap.scaled(500, 800, qtc.Qt.KeepAspectRatio)
        self.main_pic_label.setPixmap(self.scaled_img)

    def emboss_img(self):
        self.bw_on_off = 0
        self.sm_on_off = 0

        if self.em_on_off == 0:
            self.temp = self.img
            self.temp = self.temp.filter(ImageFilter.EMBOSS)
            self.pixmap = ImageQt.toqpixmap(self.temp)
            self.em_on_off = 1
        else:
            self.pixmap = ImageQt.toqpixmap(self.img)
            self.em_on_off = 0
        
        self.scaled_img = self.pixmap.scaled(500, 800, qtc.Qt.KeepAspectRatio)
        self.main_pic_label.setPixmap(self.scaled_img)

    def smooth_img(self):
        self.bw_on_off = 0
        self.em_on_off = 0

        if self.sm_on_off == 0:
            self.temp = self.img
            self.temp = self.temp.filter(ImageFilter.SMOOTH)
            self.pixmap = ImageQt.toqpixmap(self.temp)
            self.sm_on_off = 1
        else:
            self.pixmap = ImageQt.toqpixmap(self.img)
            self.sm_on_off = 0
        
        self.scaled_img = self.pixmap.scaled(500, 800, qtc.Qt.KeepAspectRatio)
        self.main_pic_label.setPixmap(self.scaled_img)
    
    def remove_filter_options(self):
        self.row_two_layout.removeWidget(self.smooth_btn)
        del self.smooth_btn
        self.row_two_layout.removeWidget(self.emboss_btn)
        del self.emboss_btn
        self.row_two_layout.removeWidget(self.black_white_btn)
        del self.black_white_btn
        self.row_two_layout.removeWidget(self.back_to_edit)
        del self.back_to_edit
               
    
    
    def return_edit(self):
        try:
            self.remove_bright_options()
        except:
            pass

        try:
            self.img = self.temp
            self.remove_filter_options()   
        except:
            pass
            
        self.show_edit_options()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main_window = ImageEditor()
    sys.exit(app.exec_())