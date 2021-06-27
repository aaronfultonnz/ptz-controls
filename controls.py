import os, sys, subprocess
import configparser
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QApplication
from lib.CameraControl import CameraControl
from lib.pyinstaller_helper import resource_path, user_path


class CameraControls(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.host = ''
        self.port = 80
        self.username = 'admin'
        self.password = ''
        self.camera = None
        self.app_name = 'Camera Control'

        self.zoom_speed = 50
        self.move_speed = 50
        self.settings_filename = user_path(self.app_name, 'settings.ini')

        self.load_settings()

        self.setWindowTitle("Camera Control")
        self.setWindowIcon(QIcon(resource_path(os.path.join('assets', 'favicon.ico'))))

        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon(resource_path(os.path.join('assets', 'settings.png'))))
        self.settings_button.setIconSize(QSize(25, 24))

        self.up_button = QPushButton()
        self.up_button.setIcon(QIcon(resource_path(os.path.join('assets', 'up.png'))))
        self.up_button.setIconSize(QSize(24, 24))

        self.down_button = QPushButton()
        self.down_button.setIcon(QIcon(resource_path(os.path.join('assets', 'down.png'))))
        self.down_button.setIconSize(QSize(24, 24))

        self.left_button = QPushButton()
        self.left_button.setIcon(QIcon(resource_path(os.path.join('assets', 'left.png'))))
        self.left_button.setIconSize(QSize(24, 24))

        self.right_button = QPushButton()
        self.right_button.setIcon(QIcon(resource_path(os.path.join('assets', 'right.png'))))
        self.right_button.setIconSize(QSize(24, 24))

        self.zoom_in_button = QPushButton()
        self.zoom_in_button.setIcon(QIcon(resource_path(os.path.join('assets', 'plus.png'))))
        self.zoom_in_button.setIconSize(QSize(24, 24))

        self.zoom_out_button = QPushButton()
        self.zoom_out_button.setIcon(QIcon(resource_path(os.path.join('assets', 'minus.png'))))
        self.zoom_out_button.setIconSize(QSize(24, 24))

        self.message = QLabel()
        self.message.setAlignment(Qt.AlignCenter)

        self.main_layout = QGridLayout()

        self.main_layout.addWidget(self.settings_button, 1, 0, 1, 1)
        self.main_layout.addWidget(self.zoom_in_button, 2, 0, 1, 1)
        self.main_layout.addWidget(self.zoom_out_button, 3, 0, 1, 1)

        self.main_layout.addWidget(self.up_button, 1, 3, 1, 1)
        self.main_layout.addWidget(self.down_button, 3, 3, 1, 1)
        self.main_layout.addWidget(self.left_button, 2, 2, 1, 1)
        self.main_layout.addWidget(self.right_button, 2, 4, 1, 1)

        self.main_layout.addWidget(self.message, 4, 0, 1, 5)

        self.settings_button.pressed.connect(self.open_settings)
        self.up_button.pressed.connect(self.move_up)
        self.up_button.released.connect(self.stop_move)
        self.down_button.pressed.connect(self.move_down)
        self.down_button.released.connect(self.stop_move)
        self.left_button.pressed.connect(self.move_left)
        self.left_button.released.connect(self.stop_move)
        self.right_button.pressed.connect(self.move_right)
        self.right_button.released.connect(self.stop_move)

        self.zoom_in_button.pressed.connect(self.zoom_in)
        self.zoom_in_button.released.connect(self.stop_move)
        self.zoom_out_button.pressed.connect(self.zoom_out)
        self.zoom_out_button.released.connect(self.stop_move)

        self.setLayout(self.main_layout)

    def connect_to_camera(self):
        try:
            self.camera = CameraControl(host=self.host, port=self.port, username=self.username, password=self.password)
            self.camera.setup()
        except Exception as err:
            self.message.setText('Could not connect to the camera')
            self.disable_all()

    def move_left(self):
        self.camera.move(-1 * round(self.move_speed / 100, 1), 0)

    def move_right(self):
        self.camera.move(round(self.move_speed / 100, 1), 0)

    def move_up(self):
        self.camera.move(0, round(self.move_speed / 100, 1))

    def move_down(self):
        self.camera.move(0, -1 * round(self.move_speed / 100, 1))

    def stop_move(self):
        self.camera.stop()

    def zoom_in(self):
        self.camera.zoom(round(self.zoom_speed / 100, 1))

    def zoom_out(self):
        self.camera.zoom(round(-1 * self.zoom_speed / 100, 1))

    def disable_all(self):
        self.up_button.setEnabled(False)
        self.down_button.setEnabled(False)
        self.left_button.setEnabled(False)
        self.right_button.setEnabled(False)
        self.zoom_in_button.setEnabled(False)
        self.zoom_out_button.setEnabled(False)

    def default_settings(self):
        parser = configparser.ConfigParser()
        config_file = open(self.settings_filename, 'w')
        config_file.write('# Restart the program after changing settings\n')
        parser.add_section('Camera')
        parser.set('Camera', 'host', '192.168.x.x')
        parser.set('Camera', 'port', '80')
        parser.set('Camera', 'username', 'admin')
        parser.set('Camera', 'password', '')
        parser.write(config_file)
        config_file.close()

    def open_settings(self):
        if sys.platform == "win32":
            os.startfile(self.settings_filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, self.settings_filename])

    def load_settings(self):
        if not os.path.isfile(self.settings_filename):
            self.default_settings()

        config = configparser.ConfigParser()
        config.read(self.settings_filename)
        self.host = config.get('Camera', 'host')
        self.port = config.get('Camera', 'port')
        self.username = config.get('Camera', 'username')
        self.password = config.get('Camera', 'password')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cc = CameraControls()
    cc.show()
    cc.connect_to_camera()
    sys.exit(app.exec_())
