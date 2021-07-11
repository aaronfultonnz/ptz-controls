import os, sys, subprocess
import configparser
from lib.CameraControl import CameraControl
from lib.pyinstaller_helper import resource_path, user_path
from tkinter import Button, PhotoImage,Label, Tk
from onvif.exceptions import ONVIFError


class CameraControls():
    def __init__(self):

        self.name = ''
        self.host = ''
        self.port = 80
        self.username = 'admin'
        self.password = ''
        self.camera = None
        self.app_name = 'Camera Control'

        self.zoom_speed = 50
        self.move_speed = 50
        self.settings_filename = user_path(self.app_name, 'settings.ini')


        root = Tk()
        root.title("Camera Control")
        root.geometry("250x250")
        root.iconbitmap(resource_path(os.path.join('assets', 'favicon.ico')))

        self.name = Label(root, text=self.name,anchor="center")
        self.name.grid(row=0,column=0, columnspan=5)


        settings_photo = PhotoImage(file=resource_path(os.path.join('assets', 'settings.png')))
        self.settings_button = Button(root, image=settings_photo, height=24, width=24)
        self.settings_button.bind("<ButtonPress>", self.open_settings)
        self.settings_button.bind("<ButtonRelease>", self.open_settings)
        self.settings_button.grid(row=1,column=0, padx=5,pady=5 ,ipadx=5,ipady=5)

        up_photo = PhotoImage(file=resource_path(os.path.join('assets', 'up.png')))
        self.up_button = Button(root, image=up_photo, height=24, width=24)
        self.up_button.bind("<ButtonPress>", self.move_up)
        self.up_button.bind("<ButtonRelease>", self.move_up)
        self.up_button.grid(row=1,column=3, padx=5,pady=5 ,ipadx=5,ipady=5)

        down_photo = PhotoImage(file=resource_path(os.path.join('assets', 'down.png')))
        self.down_button = Button(root, image=down_photo, height=24, width=24)
        self.down_button.bind("<ButtonPress>", self.move_down)
        self.down_button.bind("<ButtonRelease>", self.move_down)
        self.down_button.grid(row=3,column=3, padx=5,pady=5 ,ipadx=5,ipady=5)

        left_photo = PhotoImage(file=resource_path(os.path.join('assets', 'left.png')))
        self.left_button = Button(root, image=left_photo, height=24, width=24)
        self.left_button.bind("<ButtonPress>", self.move_left)
        self.left_button.bind("<ButtonRelease>", self.move_left)
        self.left_button.grid(row=2,column=2, padx=5,pady=5 ,ipadx=5,ipady=5)

        right_photo = PhotoImage(file=resource_path(os.path.join('assets', 'right.png')))
        self.right_button = Button(root, image=right_photo, height=24, width=24)
        self.right_button.bind("<ButtonPress>", self.move_right)
        self.right_button.bind("<ButtonRelease>", self.stop_move)
        self.right_button.grid(row=2,column=4, padx=5,pady=5 ,ipadx=5,ipady=5)

        plus_photo = PhotoImage(file=resource_path(os.path.join('assets', 'plus.png')))
        self.zoom_in_button = Button(root, image=plus_photo, height=24, width=24)
        self.zoom_in_button.bind("<ButtonPress>", self.zoom_in)
        self.zoom_in_button.bind("<ButtonRelease>", self.stop_move)
        self.zoom_in_button.grid(row=2,column=0, padx=5,pady=5 ,ipadx=5,ipady=5)

        minus_photo = PhotoImage(file=resource_path(os.path.join('assets', 'minus.png')))
        self.zoom_out_button = Button(root, image=minus_photo, height=24, width=24)
        self.zoom_out_button.bind("<ButtonPress>", self.zoom_out)
        self.zoom_out_button.bind("<ButtonRelease>", self.stop_move)
        self.zoom_out_button.grid(row=3,column=0, padx=5,pady=5 ,ipadx=5,ipady=5)

        self.message = Label(root, text="",anchor="center")
        self.message.grid(row=4,column=0, columnspan=5)

        try:
            self.load_settings()
            self.connect_to_camera()

        except ONVIFError:
            self.message.configure(text=f'Error: Cannot connect to {self.name}')
            self.disable_all()
        except Exception as err:
            self.message.configure(text=f'Error: {err}')
            self.disable_all()

        root.mainloop()

    def connect_to_camera(self):
        self.camera = CameraControl(host=self.host, port=self.port, username=self.username, password=self.password)
        self.camera.setup()

    def move_left(self, evt):
        self.camera.move(-1 * round(self.move_speed / 100, 1), 0)

    def move_right(self, evt):
        self.camera.move(round(self.move_speed / 100, 1), 0)

    def move_up(self, evt):
        self.camera.move(0, round(self.move_speed / 100, 1))

    def move_down(self, evt):
        self.camera.move(0, -1 * round(self.move_speed / 100, 1))

    def stop_move(self, evt):
        self.camera.stop()

    def zoom_in(self, evt):
        self.camera.zoom(round(self.zoom_speed / 100, 1))

    def zoom_out(self, evt):
        self.camera.zoom(round(-1 * self.zoom_speed / 100, 1))

    def disable_all(self):
        self.up_button.configure(state="disabled")
        self.down_button.configure(state="disabled")
        self.left_button.configure(state="disabled")
        self.right_button.configure(state="disabled")
        self.zoom_in_button.configure(state="disabled")
        self.zoom_out_button.configure(state="disabled")

    def default_settings(self):
        parser = configparser.ConfigParser()
        config_file = open(self.settings_filename, 'w')
        config_file.write('# Restart the program after changing settings\n')
        parser.add_section('Camera 1')
        parser.set('Camera 1', 'name', 'Camera 1')
        parser.set('Camera 1', 'host', '192.168.x.x')
        parser.set('Camera 1', 'port', '80')
        parser.set('Camera 1', 'username', 'admin')
        parser.set('Camera 1', 'password', '')
        parser.write(config_file)
        config_file.close()

    def open_settings(self, evt):
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
        self.name = config.get('Camera 1', 'name')
        self.host = config.get('Camera 1', 'host')
        self.port = config.get('Camera 1', 'port')
        self.username = config.get('Camera 1', 'username')
        self.password = config.get('Camera 1', 'password')


if __name__ == '__main__':
    cc = CameraControls()
