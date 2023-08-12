# Third party modules
import tkinter, datetime, os
from PIL import Image, ImageTk
from ctypes import windll

# Project-specific modules
from gui import FloatingWindow
from database_manager import DatabaseManager

class Launcher():
    ''' Displays a login window and option to allow users to create an account. '''
    def __init__(self, width, height, path):
        self.width, self.height = width, height

        os_user = windll.user32
        self.x_off, self.y_off = os_user.GetSystemMetrics(0), os_user.GetSystemMetrics(1)

        self.root = tkinter.Tk()
        self.root.withdraw()
        self.root.resizable(False, False)
        self.window = FloatingWindow(self.root)
        self.window.geometry("{}x{}+{}+{}".format(self.width, self.height, int((self.x_off - self.width) / 2), int((self.y_off - self.height) / 2)))
        self.window.overrideredirect(True)

        self.exit_button_size = (30, 30)
        self.sign_in_button_size = (10, 1)
        self.create_account_button_size = (15, 1)
        self.exit_button_padding = 10
        self.exit_button_pressed_padding = 0
        self.entry_size = 25
        self.entry_label_padding = 30

        self.header_label_x, self.header_label_y = self.width / 2, 115
        self.entry_label_x, self.entry_label_y = self.width / 2 - 175, self.height / 2
        self.entry_x, self.entry_y = self.width / 2 - 60, self.height / 2 + 5
        self.login_header_x, self.login_header_y = self.width / 2, 125
        self.sign_in_button_x, self.sign_in_button_y = self.width / 2 + 169, self.height / 2 + 65
        self.error_label_x, self.error_label_y = self.width / 2, self.height / 2 + 100
        self.signup_label_x, self.signup_label_y = self.width - 150, self.height - 8
        self.create_account_button_x, self.create_account_button_y = self.width - 5, self.height - 5

        self.bg_colour = '#171717'
        self.highlight_bg_colour = '#2b2b2b'
        self.highlight_fg_colour = '#7612db'
        self.hover_bg_colour = '#3b3b3b'
        self.text_colour = '#ffffff'
        self.error_colour = '#ffffff'

        self.header_font = ('Montserrat ExtraLight', '35')
        self.entry_label_font = ('Montserrat Light', '16')
        self.entry_font = ('Montserrat Light', '10')
        self.sign_in_button_font = ('Montserrat Medium', '10')
        self.error_label_font = ('Montserrat Medium', '10')
        self.signup_label_font = ('Montserrat Light', '12')

        self.parent_dir = os.path.abspath(os.path.join(path, os.pardir))
        self.db_manager = DatabaseManager(r'{}/EngineData.db'.format(self.parent_dir))
        self._launcher_closed = False
        self.error_text = None
        self.account_created_text = None
        self.new_sign_in_button_canvas = None
        self.path = path

        self.construct_launcher()
        self.root.mainloop()

    def launcher_closed(self):
        return self._launcher_closed

    def destruct_launcher(self):
        self.root.destroy()

    def close_window(self, event):
        self.destruct_launcher()
        self.db_manager.close_database()
        self._launcher_closed = True
    
    def construct_launcher(self):
        self.entered_username = tkinter.StringVar()
        self.entered_password = tkinter.StringVar()

        self.canvas = tkinter.Canvas(self.window, width = self.width, height = self.height, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.button_canvas = tkinter.Canvas(self.canvas, width = self.exit_button_size[0], height = self.exit_button_size[1], bd=0, highlightthickness=0)
        self.button_canvas.place(x = self.width, y = 0, anchor = 'ne')

        bg_img = Image.open(r'{}/images/launcher_bg.png'.format(self.parent_dir))
        bg_top_corner_img = Image.open(r'{}/images/launcher_bg_topcorner.png'.format(self.parent_dir))
        bg_top_corner_hover_img = Image.open(r'{}/images/launcher_bg_topcorner_hover.png'.format(self.parent_dir))
        launcher_exit_img = Image.open(r'{}/images/exit.png'.format(self.parent_dir))
        self.bg_img = ImageTk.PhotoImage(bg_img)
        self.bg_top_corner_img = ImageTk.PhotoImage(bg_top_corner_img)
        self.bg_top_corner_hover_img = ImageTk.PhotoImage(bg_top_corner_hover_img)
        self.launcher_exit_img = ImageTk.PhotoImage(launcher_exit_img)
        self.username_entry = tkinter.Entry(self.window, textvariable = self.entered_username, width = self.entry_size, font = self.entry_font, bg = self.bg_colour, fg = self.text_colour, highlightcolor = self.highlight_fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.highlight_bg_colour)
        self.password_entry = tkinter.Entry(self.window, textvariable = self.entered_password, width = self.entry_size, font = self.entry_font, bg = self.bg_colour, fg = self.text_colour, highlightcolor = self.highlight_fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.highlight_bg_colour, show="●")
        self.sign_in_button = tkinter.Button(self.window, text = 'SIGN IN', width = self.sign_in_button_size[0], height = self.sign_in_button_size[1], font = self.sign_in_button_font, bg = self.bg_colour, fg = self.text_colour, activeforeground = self.highlight_fg_colour, bd = 0, activebackground = self.highlight_bg_colour, command = lambda: self.sign_in(self.entered_username.get(), self.entered_password.get()))
        self.create_account_button = tkinter.Button(self.window, text = 'CREATE ACCOUNT', width = self.create_account_button_size[0], height = self.create_account_button_size[1], font = self.sign_in_button_font, bg = self.bg_colour, fg = self.text_colour, activeforeground = self.highlight_fg_colour, bd = 0, activebackground = self.highlight_bg_colour, command = lambda: self.change_gui_to_create_account())

        self.canvas.create_image(self.width, 0, image = self.bg_img, anchor = 'ne')
        self.header = self.canvas.create_text(self.header_label_x, self.header_label_y, anchor = 'n', text = 'SIGN IN', font=self.header_font, fill = self.text_colour)
        self.canvas.create_text(self.entry_label_x, self.entry_label_y, anchor = 'nw', text = 'Username', font=self.entry_label_font, fill = self.text_colour)
        self.canvas.create_text(self.entry_label_x, self.entry_label_y + self.entry_label_padding, anchor = 'nw', text = 'Password', font=self.entry_label_font, fill = self.text_colour)
        self.create_account_text = self.canvas.create_text(self.signup_label_x, self.signup_label_y, anchor = 'se', text = 'Or create an account now.', font=self.signup_label_font, fill = self.text_colour)
        self.button_canvas.create_image(0, 0, anchor = 'nw', image = self.bg_top_corner_img)
        self.button_canvas.create_image(0, 0, anchor = 'nw', image = self.bg_top_corner_hover_img, tags = 'hover')
        self.button_canvas.create_image(0, 0, anchor = 'nw', image = self.launcher_exit_img, tags = 'exit_button')
        self.button_canvas.itemconfig('hover', state = 'hidden')
        self.canvas.create_window(self.entry_x, self.entry_y, anchor = 'nw', window = self.username_entry)
        self.canvas.create_window(self.entry_x, self.entry_y + self.entry_label_padding, anchor = 'nw', window = self.password_entry)
        self.sign_in_button_canvas = self.canvas.create_window(self.sign_in_button_x, self.sign_in_button_y, anchor = 'ne', window = self.sign_in_button)
        self.create_account_canvas = self.canvas.create_window(self.create_account_button_x, self.create_account_button_y, anchor = 'se', window = self.create_account_button)

        self.button_canvas.bind("<ButtonRelease-1>", self.close_window)
        self.button_canvas.bind("<Button-1>", self.pressed_exit_button)
        self.button_canvas.bind('<Enter>', self.hover_enter_exit_button)
        self.button_canvas.bind('<Leave>', self.hover_leave_exit_button)

        self.window.bind('<Return>', lambda event: self.check_sign_in_focus(self.window.focus_get()))

        self.window.bind('<Down>', self.initial_username_focus)
        self.window.bind('<Right>', self.initial_username_focus)
        self.window.bind('<Up>', self.initial_create_account_focus)
        self.window.bind('<Left>', self.initial_create_account_focus)

        self.username_entry.bind('<Down>', lambda event: self.password_entry.focus())
        self.password_entry.bind('<Down>', lambda event: self.sign_in_button.focus())
        self.sign_in_button.bind('<Down>', lambda event: self.create_account_button.focus())
        self.create_account_button.bind('<Down>', lambda event: self.username_entry.focus())
        self.create_account_button.bind('<Up>', lambda event: self.sign_in_button.focus())
        self.sign_in_button.bind('<Up>', lambda event: self.password_entry.focus())
        self.password_entry.bind('<Up>', lambda event: self.username_entry.focus())
        self.username_entry.bind('<Up>', lambda event: self.create_account_button.focus())


        self.username_entry.bind('<Right>', lambda event: self.password_entry.focus())
        self.password_entry.bind('<Right>', lambda event: self.sign_in_button.focus())
        self.sign_in_button.bind('<Right>', lambda event: self.create_account_button.focus())
        self.create_account_button.bind('<Right>', lambda event: self.username_entry.focus())
        self.create_account_button.bind('<Left>', lambda event: self.sign_in_button.focus())
        self.sign_in_button.bind('<Left>', lambda event: self.password_entry.focus())
        self.password_entry.bind('<Left>', lambda event: self.username_entry.focus())
        self.username_entry.bind('<Left>', lambda event: self.create_account_button.focus())

    def initial_username_focus(self, event):
        if self.window.focus_get() == None:
            self.username_entry.focus()
            self.window.bind('<Down>', lambda event: None)
            self.window.bind('<Right>', lambda event: None)

    def initial_create_account_focus(self, event):
        if self.window.focus_get() == None:
            self.create_account_button.focus()
            self.window.bind('<Up>', lambda event: None)
            self.window.bind('<Left>', lambda event: None)

    def check_sign_in_focus(self, focus):
        if focus == self.create_account_button:
            self.change_gui_to_create_account()
        else:
            self.sign_in(self.entered_username.get(), self.entered_password.get())

    def check_create_account_focus(self, focus):
        if focus == self.new_sign_in_button:
            self.change_gui_to_sign_in()
        else:
            self.create_account(self.entered_username.get(), self.entered_password.get())

    def pressed_exit_button(self, event):
        self.button_canvas.move('exit_button', self.exit_button_pressed_padding, self.exit_button_pressed_padding)

    def hover_enter_exit_button(self, event):
        self.button_canvas.itemconfig('hover', state = 'normal')

    def hover_leave_exit_button(self, event):
        self.button_canvas.itemconfig('hover', state = 'hidden')

    def reset_gui_to_sign_in(self):
        # Resets the gui to the original sign in screen, used when pressing escape or backspace on create account to go backwards
        self.window.bind('<Return>', lambda event: self.check_sign_in_focus(self.window.focus_get()))

        self.sign_in_button.bind('<Down>', lambda event: self.create_account_button.focus())
        self.create_account_button.bind('<Down>', lambda event: self.username_entry.focus())
        self.create_account_button.bind('<Up>', lambda event: self.sign_in_button.focus())
        self.username_entry.bind('<Up>', lambda event: self.create_account_button.focus())
        self.sign_in_button.bind('<Right>', lambda event: self.create_account_button.focus())
        self.create_account_button.bind('<Right>', lambda event: self.username_entry.focus())
        self.create_account_button.bind('<Left>', lambda event: self.sign_in_button.focus())
        self.username_entry.bind('<Left>', lambda event: self.create_account_button.focus())

        self.canvas.itemconfig(self.header, text = 'SIGN IN', font = self.header_font)
        self.canvas.itemconfig(self.account_created_text, state = 'hidden')
        self.sign_in_button.config(text = 'SIGN IN', width = self.sign_in_button_size[0], height = self.sign_in_button_size[1], command = lambda: self.sign_in(self.entered_username.get(), self.entered_password.get()))
        self.canvas.itemconfig(self.create_account_canvas, state = 'normal')
        self.canvas.itemconfig(self.create_account_text, state = 'normal')
        if self.new_sign_in_button_canvas != None:
            self.canvas.itemconfig(self.new_sign_in_button_canvas, state = 'hidden')


    def change_gui_to_create_account(self):
        # Changes the gui to create an account screen
        self.window.bind('<Escape>', lambda event: self.reset_gui_to_sign_in())
        self.window.bind('<BackSpace>', lambda event: self.reset_gui_to_sign_in())

        self.window.bind('<Return>', lambda event: self.create_account(self.entered_username.get(), self.entered_password.get()))

        self.sign_in_button.bind('<Down>', lambda event: self.username_entry.focus())
        self.sign_in_button.bind('<Right>', lambda event: self.username_entry.focus())
        self.username_entry.bind('<Up>', lambda event: self.sign_in_button.focus())
        self.username_entry.bind('<Left>', lambda event: self.sign_in_button.focus())

        self.canvas.itemconfig(self.header, text = 'CREATE ACCOUNT', font = self.header_font)
        self.canvas.itemconfig(self.create_account_canvas, state = 'hidden')
        self.canvas.itemconfig(self.create_account_text, state = 'hidden')
        self.sign_in_button.config(text = 'CREATE ACCOUNT', width = self.create_account_button_size[0], height = self.create_account_button_size[1], command = lambda: self.create_account(self.entered_username.get(), self.entered_password.get()))
        if self.error_text != None:
            self.canvas.delete(self.error_text)

    def change_gui_to_sign_in(self):
        # Changes the gui to sign in after creating an account
        self.window.bind('<Return>', lambda event: self.check_sign_in_focus(self.window.focus_get()))

        self.sign_in_button.bind('<Down>', lambda event: self.username_entry.focus())
        self.sign_in_button.bind('<Right>', lambda event: self.username_entry.focus())
        self.username_entry.bind('<Up>', lambda event: self.sign_in_button.focus())
        self.username_entry.bind('<Left>', lambda event: self.sign_in_button.focus())

        self.canvas.itemconfig(self.header, text = 'SIGN IN', font = self.header_font)
        self.canvas.itemconfig(self.account_created_text, state = 'hidden')
        self.canvas.itemconfig(self.new_sign_in_button_canvas, state = 'hidden')
        self.sign_in_button.config(text = 'SIGN IN', width = self.sign_in_button_size[0], height = self.sign_in_button_size[1], command = lambda: self.sign_in(self.entered_username.get(), self.entered_password.get()))

    def update_create_account_gui(self):
        if self.account_created_text == None:
            self.account_created_text = self.canvas.create_text(self.signup_label_x + 45, self.signup_label_y, anchor = 'se', text = 'Account sucessfully created. Sign in now.', font=self.signup_label_font, fill = self.text_colour)
            self.new_sign_in_button = tkinter.Button(self.window, text = 'SIGN IN', width = self.sign_in_button_size[0], height = self.sign_in_button_size[1], font = self.sign_in_button_font, bg = self.bg_colour, fg = self.text_colour, activeforeground = self.highlight_fg_colour, bd = 0, activebackground = self.highlight_bg_colour, command = lambda: self.change_gui_to_sign_in())
            self.new_sign_in_button_canvas = self.canvas.create_window(self.create_account_button_x, self.create_account_button_y, anchor = 'se', window = self.new_sign_in_button)

            self.window.bind('<Return>', lambda event: self.check_create_account_focus(self.window.focus_get()))

            self.sign_in_button.bind('<Down>', lambda event: self.new_sign_in_button.focus())
            self.new_sign_in_button.bind('<Down>', lambda event: self.username_entry.focus())
            self.sign_in_button.bind('<Right>', lambda event: self.new_sign_in_button.focus())
            self.new_sign_in_button.bind('<Right>', lambda event: self.username_entry.focus())

            self.username_entry.bind('<Up>', lambda event: self.new_sign_in_button.focus())
            self.new_sign_in_button.bind('<Up>', lambda event: self.sign_in_button.focus())
            self.username_entry.bind('<Left>', lambda event: self.new_sign_in_button.focus())
            self.new_sign_in_button.bind('<Left>', lambda event: self.sign_in_button.focus())

    def create_account(self, entered_username, entered_password):
        self.db_manager.add_user(entered_username, entered_password, datetime.datetime.now())
        self.update_create_account_gui()

    def sign_in(self, entered_username, entered_password):
        exists = self.db_manager.check_user_existance(entered_username, entered_password)
        if not exists:
            if self.error_text == None:
                self.error_text = self.canvas.create_text(self.error_label_x, self.error_label_y, anchor = 'n', text = 'Incorrect Username or Password', font=self.error_label_font, fill = self.error_colour)
        else:
            self.username = entered_username
            self.destruct_launcher()

    def get_username(self):
        return self.username
