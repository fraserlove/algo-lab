# Third party modules
import tkinter, os, time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ctypes import windll

# Project-specific modules
import data_handling
from shapes import Cube, Quad, Plane, Polygon, Sphere, Line2D, Line3D

class GUI():
    ''' Renders and updates the Tkinter GUI and the Matplotlib FPS graph. '''
    def __init__(self, engine_client, db_manager, width, height, path):
        self.engine_client = engine_client
        self.db_manager = db_manager
        self.path = path

        self.width, self.height = width, height
        os_user = windll.user32
        self.x_off, self.y_off = os_user.GetSystemMetrics(0), os_user.GetSystemMetrics(1)

        self.top_bar_width, self.top_bar_height = self.width, 25
        self.control_width, self.control_height = 250, self.height - self.top_bar_height
        self.fps_graph_width = 400
        self.details_width, self.details_height = self.width - self.control_width - self.fps_graph_width, 200
        self.viewer_width, self.viewer_height = self.width - self.control_width, self.height - self.details_height - self.top_bar_height
        self.fps_graph_height = self.details_height

        self.properties_window_width, self.properties_window_height = 200, 500

        self.viewer_centre = (self.viewer_width / 2, self.viewer_height / 2, 0, 0)

        self.parent_dir = os.path.abspath(os.path.join(path, os.pardir))
        self.root = tkinter.Tk()
        self.root.withdraw()
        self.root.resizable(False, False)
        self.window = FloatingWindow(self.root)
        self.window.geometry("{}x{}+{}+{}".format(self.width, self.height, int((self.x_off - self.width) / 2), int((self.y_off - self.height) / 2)))
        self.window.overrideredirect(True)
        self.window.title('FL3D Engine')
        self.window.iconbitmap(r'{}/images/ICON.ico'.format(self.parent_dir))

        self.controls_header_padding = 10
        self.controls_separator_padding = 50
        self.info_separator_padding = 750
        self.world_space_padding = 100
        self.add_object_padding = 300
        self.add_object_dimensions = (20, 8)
        self.world_space_dimensions = (25, 8)
        self.world_objects_list_box_height = 130
        self.separator_dimensions = (100, 1)
        self.label_padding = (25, 70)
        self.slider_padding = (140, 1)
        self.slider_offset = 25
        self.button_padding = self.label_padding[0] + 4, self.label_padding[1] + self.slider_offset * 5.5
        self.long_slider_offset = self.label_padding[0] + 4, self.label_padding[1] + self.slider_offset * 11.5
        self.long_slider_padding = 25 
        self.button_offset = 40
        self.exit_button_size = (30, 30)
        self.max_label_padding = 15
        self.min_label_padding = 15
        self.one_line_label_padding = 16
        self.one_line_value_padding = 32
        self.username_label_offset = 755
        self.info_header_padding = 710
        self.info_label_padding = (20, 20)
        self.add_object_button_x_offset = 213
        self.object_details_bg_padding = (120, 10)
        self.object_details_bg_size_x = 275

        self.translation_line_length = int(self.viewer_width / 50)
        self.translation_line_width = int(self.viewer_height / 100)

        self.previous_selected = None
        self.menu_open = False
        self.object_position_label = None

        self.bg_colour = '#171717'
        self.highlight_bg_colour = '#2b2b2b'
        self.hover_bg_colour = '#3b3b3b'
        self.fg_colour = '#9021ff'
        self.highlight_fg_colour = '#962cd4'
        self.hover_fg_colour = '#b44df0'
        self.window_title_colour = '#ababab'
        self.header_colour = '#ffffff'
        self.embeded_colour = '#333333'
        self.small_button_colour = '#232323'
        self.translation_lines_colour_x = (233, 118, 16)
        self.translation_lines_colour_y = (144, 33, 255)

        self.graph_colour = '#ffffff'
        self.max_min_graph_colour = '#474747'
        self.avg_graph_colour = '#9021ff'

        self.graph_line_width = 1.5
        self.max_min_line_width = 0.75
        self.avg_line_width = 0.75

        self.header_font = ('Montserrat SemiBold', '16')
        self.label_font = ('Montserrat Regular', '10')
        self.button_font = ('Montserrat Medium', '10')
        self.window_title_font = ('Montserrat Medium', '10')
        self.list_box_font = ('Montserrat Regular', '8')
        self.small_button_font = ('Montserrat Regular', '9')
        self.large_label_font = ('Montserrat Regular', '14')
        self.details_font = ('Montserrat Regular', '8')

        self.top_bar = tkinter.Frame(self.window, bg = self.bg_colour, width = self.top_bar_width, height = self.top_bar_height)
        self.top_bar.pack(side = 'top')
        self.control = tkinter.Frame(self.window, bg = self.bg_colour, width = self.control_width, height = self.control_height)
        self.control.pack(side = 'right')
        self.viewer = tkinter.Frame(self.window, width = self.viewer_width, height = self.viewer_height)
        self.viewer.pack(side = 'top')
        self.details = tkinter.Frame(self.window, bg = self.bg_colour, width = self.details_width, height = self.details_height)
        self.details.pack(side = 'right')
        self.fps_graph = tkinter.Frame(self.window, width = self.fps_graph_width, height = self.fps_graph_height)
        self.fps_graph.pack(side = 'left')
        self.maximise_window = True

        self.top_bar.bind("<Map>", self.engine_client.maximise_window) # Used to properly maximise and minimise the window

        self.fps_viewer = plt.Figure(figsize=(4,2), dpi=100)
        self.fps_plot = self.fps_viewer.add_subplot(111)
        self.fps_viewer.subplots_adjust(bottom = 0.1, top = 0.9, right = 1.05, left= 0)
        self.fps_viewer.set_facecolor(self.bg_colour)
        self.fps_plot.set_facecolor(self.bg_colour)
        self.fps_plot.axis('off')

        chart_type = FigureCanvasTkAgg(self.fps_viewer, self.fps_graph)
        chart_type.get_tk_widget().pack()

        os.environ['SDL_VIDEODRIVER'] = 'windib'
        os.environ['SDL_WINDOWID'] = str(self.viewer.winfo_id()) # Used to embed pygame window in tkinter

        self.GWL_EXSTYLE=-20
        self.WS_EX_APPWINDOW=0x00040000
        self.WS_EX_TOOLWINDOW=0x00000080 # Used to show icon in task bar when in default window mode

        self.window.create_grip(self.top_bar)
        self.construct_gui()

    def set_appwindow(self):
        hwnd = windll.user32.GetParent(self.window.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, self.GWL_EXSTYLE)
        style = style & ~self.WS_EX_TOOLWINDOW
        style = style | self.WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, self.GWL_EXSTYLE, style)
        self.window.withdraw()
        self.window.after(10, lambda: self.window.deiconify())

    def construct_gui(self):
        self.construct_top_bar()
        self.construct_control_panel()
        self.construct_details_panel()
        self.construct_fps_graph_labels()

    def destruct_gui(self):
        self.root.quit()
        plt.close()

    def hover_enter_exit_button(self, event):
        self.exit_button['bg'] = self.hover_bg_colour

    def hover_leave_exit_button(self, event):
        self.exit_button['bg'] = self.bg_colour

    def hover_enter_close_button(self, event):
        self.close_button['bg'] = self.hover_bg_colour

    def hover_leave_close_button(self, event):
        self.close_button['bg'] = self.bg_colour

    def hover_enter_button(self, event, button):
        button['bg'] = self.hover_fg_colour

    def hover_leave_button(self, event, button):
        button['bg'] = self.fg_colour

    def construct_top_bar(self):

        self.top_bar_button_padding = 10

        exit_img = Image.open(r'{}/images/exit.png'.format(self.parent_dir))
        self.exit_img = ImageTk.PhotoImage(exit_img)
        self.exit_button = tkinter.Button(self.top_bar, text = "Exit", width = self.exit_button_size[0], height = self.exit_button_size[1], command = self.engine_client.close_window, borderwidth=0, bd = -2, bg = self.bg_colour, activebackground=self.highlight_bg_colour)
        self.exit_button.config(image = self.exit_img)
        self.exit_button.image = self.exit_img
        self.exit_button.place(x = self.width - self.exit_button_size[0], y = -3, anchor = 'nw')

        close_img = Image.open(r'{}/images/close.png'.format(self.parent_dir))
        self.close_img = ImageTk.PhotoImage(close_img)
        self.close_button = tkinter.Button(self.top_bar, text = "Close", width = self.exit_button_size[0], height = self.exit_button_size[1], command = self.engine_client.minimise_window, borderwidth=0, bd = -2, bg = self.bg_colour, activebackground=self.highlight_bg_colour)
        self.close_button.config(image = self.close_img)
        self.close_button.place(x = self.width - self.exit_button_size[0] * 2 - self.top_bar_button_padding, y = -3, anchor = 'nw')

        self.window_title = tkinter.Label(self.top_bar, text='FL3D Rendering Engine', bg=self.bg_colour, fg=self.window_title_colour, font=self.window_title_font)
        self.window_title.place(x = self.width / 2, y = 0, anchor = 'n')
        self.window.create_grip(self.window_title)

        self.exit_button.bind('<Enter>', self.hover_enter_exit_button)
        self.exit_button.bind('<Leave>', self.hover_leave_exit_button)
        self.close_button.bind('<Enter>', self.hover_enter_close_button)
        self.close_button.bind('<Leave>', self.hover_leave_close_button)

    def construct_control_panel(self):

        controls_header = tkinter.Label(self.control, text='ENGINE SETTINGS', bg=self.bg_colour, fg=self.header_colour, font=self.header_font)
        controls_header.place(x = self.control_width / 2, y = self.controls_header_padding, anchor = 'n')

        controls_separator_canvas = tkinter.Canvas(self.control, width = self.separator_dimensions[0], height = self.separator_dimensions[1], bg = self.bg_colour, bd = 0, highlightthickness=0)
        controls_separator_canvas.place(x = (self.control_width - self.separator_dimensions[0]) / 2, y = self.controls_separator_padding)
        controls_separator = controls_separator_canvas.create_line(0, 0, self.separator_dimensions[0], 0, fill = self.fg_colour)

        info_header = tkinter.Label(self.control, text='USER INFO', bg=self.bg_colour, fg=self.header_colour, font=self.header_font)
        info_header.place(x = self.control_width / 2, y = self.info_header_padding, anchor = 'n')

        info_separator_canvas = tkinter.Canvas(self.control, width = self.separator_dimensions[0], height = self.separator_dimensions[1], bg = self.bg_colour, bd = 0, highlightthickness=0)
        info_separator_canvas.place(x = (self.control_width - self.separator_dimensions[0]) / 2, y = self.info_separator_padding)
        info_separator = info_separator_canvas.create_line(0, 0, self.separator_dimensions[0], 0, fill = self.fg_colour)

        self.construct_binary_sliders()
        self.construct_buttons()
        self.construct_linear_sliders()
        self.construct_info()

    def construct_details_panel(self):
        add_object_label = tkinter.Label(self.details, text='Add Object', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        add_object_label.place(x = self.details_width - self.add_object_padding, y = 5, anchor = 'n')

        objects = ['Line2D', 'Line3D', 'Cube', 'Quad', 'Plane', 'Polygon', 'Sphere']
        self.add_object_lb = tkinter.Listbox(self.details, relief = 'flat', width = self.world_space_dimensions[0], height = self.world_space_dimensions[1], bg=self.small_button_colour, bd=0, borderwidth=0, highlightthickness=0, fg = 'white', activestyle = 'none', selectbackground = self.embeded_colour, font = self.list_box_font)
        for new_object in objects:
            self.add_object_lb.insert(tkinter.END, new_object)
        self.add_object_lb.place(x = self.details_width - self.add_object_padding, y = 30, anchor = 'n', height = self.world_objects_list_box_height)
        self.add_object_button = tkinter.Button(self.details, text="Add Object", fg="white", bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= lambda: self.open_object_properties_window(self.add_object_lb), font=self.button_font)
        self.add_object_button.place(x= self.details_width - self.add_object_button_x_offset, y = self.details_height - 10, anchor = 'se', height = 22)
        self.add_object_lb.bind('<Double-Button-1>', self.check_if_selected_object)

        self.add_object_button.bind('<Enter>', lambda event: self.hover_enter_button(event, self.add_object_button))
        self.add_object_button.bind('<Leave>', lambda event: self.hover_leave_button(event, self.add_object_button))

        world_space_label = tkinter.Label(self.details, text='World Space', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        world_space_label.place(x = self.details_width - self.world_space_padding, y = 5, anchor = 'n')

        self.world_objects_scrollbar = tkinter.Scrollbar(self.details, orient = tkinter.VERTICAL, width = 11)
        self.world_objects_lb = tkinter.Listbox(self.details, yscrollcommand = self.world_objects_scrollbar.set, relief = 'flat', width = self.world_space_dimensions[0], height = self.world_space_dimensions[1], bg=self.small_button_colour, bd=0, borderwidth=0, highlightthickness=0, fg = 'white', activestyle = 'none', selectbackground = self.embeded_colour, font = self.list_box_font)
        self.world_objects_scrollbar.config(command = self.world_objects_lb.yview)
        self.delete_world_object_button = tkinter.Button(self.details, text="Delete Object", fg="white", bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.delete_world_object, font=self.button_font)
        self.edit_world_object_button = tkinter.Button(self.details, text="Edit Object", fg="white", bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.edit_world_object, font=self.button_font)
        self.copy_world_object_button = tkinter.Button(self.details, text="Copy Object", fg="white", bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.copy_world_object, font=self.button_font)

        self.delete_world_object_button.bind('<Enter>', lambda event: self.hover_enter_button(event, self.delete_world_object_button))
        self.delete_world_object_button.bind('<Leave>', lambda event: self.hover_leave_button(event, self.delete_world_object_button))

        self.edit_world_object_button.bind('<Enter>', lambda event: self.hover_enter_button(event, self.edit_world_object_button))
        self.edit_world_object_button.bind('<Leave>', lambda event: self.hover_leave_button(event, self.edit_world_object_button))

        self.copy_world_object_button.bind('<Enter>', lambda event: self.hover_enter_button(event, self.copy_world_object_button))
        self.copy_world_object_button.bind('<Leave>', lambda event: self.hover_leave_button(event, self.copy_world_object_button))

        self.window.bind('<ButtonPress-1>', self.deselect_box)
        self.window.bind('<ButtonRelease-1>', self.check_object_details)
        self.delete_world_object_button.bind('<ButtonPress-1>', self.delete_world_object) # Extra binding needed otherwise button doenst run command as the deselect_box is ran first
        self.edit_world_object_button.bind('<ButtonPress-1>', self.edit_world_object) # Extra binding needed otherwise button doenst run command as the deselect_box is ran first
        self.copy_world_object_button.bind('<ButtonPress-1>', self.copy_world_object) # Extra binding needed otherwise button doenst run command as the deselect_box is ran first
        
        self.draw_object_details()

    def update_object_details(self):
        # If the object_position_label has been rendered before and if an item is selected in the world_space listbox
        if self.object_position_label != None and len(self.world_objects_lb.curselection()) > 0:
            # Updates the position of the current object being detailed so it displays the current value after motion
            active_object = self.world_objects_lb.get(tkinter.ACTIVE)
            self.object_position.set('Position\t\t({:.0f}, {:.0f}, {:.0f})'.format(*self.engine_client.engine.objects[active_object].get_position()))
            self.object_centre.set('Centre\t\t({:.0f}, {:.0f}, {:.0f})'.format(*self.engine_client.engine.objects[active_object].find_centre()))

    def show_object_details(self):
        # Shows the details for a specific object when the user clicks in the listbox
        active_object = self.world_objects_lb.get(tkinter.ACTIVE)
        if active_object != '':

            self.object_position = tkinter.StringVar(value = 'Position\t\t({:.0f}, {:.0f}, {:.0f})'.format(*self.engine_client.engine.objects[active_object].get_position()))
            self.object_centre = tkinter.StringVar(value = 'Centre\t\t({:.0f}, {:.0f}, {:.0f})'.format(*self.engine_client.engine.objects[active_object].find_centre()))

            self.object_details = tkinter.Frame(self.details, width = self.object_details_bg_size_x, height = self.details_height - self.object_details_bg_padding[1] * 2, bd = 0, bg = self.small_button_colour)
            self.object_details.place(x = self.object_details_bg_padding[0], y = self.object_details_bg_padding[1], anchor = 'nw')

            object_type = self.engine_client.engine.objects[active_object].get_type()
            object_colour = self.engine_client.engine.objects[active_object].get_colour()
            no_verts = str(self.engine_client.engine.objects[active_object].point_count())
            no_edges = str(self.engine_client.engine.objects[active_object].line_count())
            no_surfaces = str(self.engine_client.engine.objects[active_object].surface_count())

            object_name_label = tkinter.Label(self.object_details, text = active_object, bg = self.small_button_colour, fg=self.header_colour, font=self.large_label_font)
            object_name_label.place(x = 5, y = -5, anchor = 'nw')

            object_type_label = tkinter.Label(self.object_details, text = 'Instance of ' + object_type, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
            object_type_label.place(x = 5, y = 21, anchor = 'nw', height = 15)

            object_colour_label = tkinter.Label(self.object_details, text = 'Colour\t\t' + object_colour.capitalize(), bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
            object_colour_label.place(x = 5, y = 42, anchor = 'nw', height = 15)

            object_centre_label = tkinter.Label(self.object_details, textvariable = self.object_centre, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
            object_centre_label.place(x = 5, y = 57, anchor = 'nw', height = 15)

            self.object_position_label = tkinter.Label(self.object_details, textvariable = self.object_position, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
            self.object_position_label.place(x = 5, y = 72, anchor = 'nw', height = 15)

            no_verts_label = tkinter.Label(self.object_details, text = 'Vertices\t\t' + no_verts, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
            no_verts_label.place(x = 5, y = 87, anchor = 'nw', height = 15)

            no_edges_label = tkinter.Label(self.object_details, text = 'Edges\t\t' + no_edges, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
            no_edges_label.place(x = 5, y = 102, anchor = 'nw', height = 15)

            no_surfaces_label = tkinter.Label(self.object_details, text = 'Surfaces\t\t' + no_surfaces, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
            no_surfaces_label.place(x = 5, y = 117, anchor = 'nw', height = 15)

            if isinstance(self.engine_client.engine.objects[active_object], Line3D):
                start_point = '({:.0f}, {:.0f}, {:.0f})'.format(*self.engine_client.engine.objects[active_object].get_start_point())
                end_point = '({:.0f}, {:.0f}, {:.0f})'.format(*self.engine_client.engine.objects[active_object].get_end_point())

                start_point_label = tkinter.Label(self.object_details, text = 'Start Point\t\t' + start_point, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
                start_point_label.place(x = 5, y = 132, anchor = 'nw', height = 15)
                end_point_label = tkinter.Label(self.object_details, text = 'End Point\t\t' + end_point, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
                end_point_label.place(x = 5, y = 147, anchor = 'nw', height = 15)

            if isinstance(self.engine_client.engine.objects[active_object], Line2D):
                angle = str(self.engine_client.engine.objects[active_object].get_angle())
                magnitude = str(self.engine_client.engine.objects[active_object].get_magnitude())

                angle_label = tkinter.Label(self.object_details, text = 'Angle (degrees)\t' + angle, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
                angle_label.place(x = 5, y = 132, anchor = 'nw', height = 15)
                magnitude_label = tkinter.Label(self.object_details, text = 'Magnitude\t' + magnitude, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
                magnitude_label.place(x = 5, y = 147, anchor = 'nw', height = 15)

            if isinstance(self.engine_client.engine.objects[active_object], Sphere):
                radius = str(self.engine_client.engine.objects[active_object].get_radius())
                verts_res = str(self.engine_client.engine.objects[active_object].get_verts_res())

                radius_label = tkinter.Label(self.object_details, text = 'Radius\t\t' + radius, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
                radius_label.place(x = 5, y = 132, anchor = 'nw', height = 15)
                verts_res_label = tkinter.Label(self.object_details, text = 'Vertices Resolution\t' + verts_res, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
                verts_res_label.place(x = 5, y = 147, anchor = 'nw', height = 15)

            if isinstance(self.engine_client.engine.objects[active_object], Polygon):
                no_points = str(self.engine_client.engine.objects[active_object].get_no_points())
                size = str(self.engine_client.engine.objects[active_object].get_size())

                no_points_label = tkinter.Label(self.object_details, text = 'Vertices\t\t' + no_points, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
                no_points_label.place(x = 5, y = 132, anchor = 'nw', height = 15)
                size_label = tkinter.Label(self.object_details, text = 'Size\t\t' + size, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
                size_label.place(x = 5, y = 147, anchor = 'nw', height = 15)

            if isinstance(self.engine_client.engine.objects[active_object], Plane):
                length = str(self.engine_client.engine.objects[active_object].get_length())
                width = str(self.engine_client.engine.objects[active_object].get_width())

                length_label = tkinter.Label(self.object_details, text = 'Length\t\t' + length, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
                length_label.place(x = 5, y = 132, anchor = 'nw', height = 15)
                width_label = tkinter.Label(self.object_details, text = 'Width\t\t' + width, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
                width_label.place(x = 5, y = 147, anchor = 'nw', height = 15)

            if isinstance(self.engine_client.engine.objects[active_object], Quad):
                length = str(self.engine_client.engine.objects[active_object].get_length())
                width = str(self.engine_client.engine.objects[active_object].get_width())
                height = str(self.engine_client.engine.objects[active_object].get_height())

                length_label = tkinter.Label(self.object_details, text = 'Length\t\t' + length, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
                length_label.place(x = 5, y = 132, anchor = 'nw', height = 15)
                width_label = tkinter.Label(self.object_details, text = 'Width\t\t' + width, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
                width_label.place(x = 5, y = 147, anchor = 'nw', height = 15)
                height_label = tkinter.Label(self.object_details, text = 'Height\t\t' + height, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
                height_label.place(x = 5, y = 162, anchor = 'nw', height = 15)

            if isinstance(self.engine_client.engine.objects[active_object], Cube):
                size = str(self.engine_client.engine.objects[active_object].get_size())

                size_label = tkinter.Label(self.object_details, text = 'Size\t\t' + size, bg = self.small_button_colour, fg=self.window_title_colour, font=self.details_font)
                size_label.place(x = 5, y = 132, anchor = 'nw', height = 15)

    def check_object_details(self, event):
        # If the any items in the list box are selected, render the object details, else keep the listbox blank
        if len(self.world_objects_lb.curselection()) > 0:
            self.show_object_details()
        else:
            self.draw_object_details() # Used to draw over previous details of a deleted object

    def draw_object_details(self):
        # Renders the object details background
        self.object_details = tkinter.Frame(self.details, width = self.object_details_bg_size_x, height = self.details_height - self.object_details_bg_padding[1] * 2, bd = 0, bg = self.small_button_colour)
        self.object_details.place(x = self.object_details_bg_padding[0], y = self.object_details_bg_padding[1], anchor = 'nw')

    def delete_world_object(self, event = None):
        self.engine_client.engine.remove_object(self.world_objects_lb.get(tkinter.ACTIVE), self.engine_client)
        self.world_objects_lb.delete(tkinter.ACTIVE)
        self.draw_object_details() # Used to draw over previous details of a deleted object
    
    def deselect_box(self, event):
        if self.world_objects_lb.curselection() == self.previous_selected:
            self.world_objects_lb.selection_clear(0, tkinter.END)
        self.previous_selected = self.world_objects_lb.curselection()

    def check_if_selected_object(self, event):
        if self.selected_exists(self.add_object_lb):
            self.open_object_properties_window(self.add_object_lb)

    def menu_timeout(self):
        self.object_colour.set('')
        self.properties_window.update()

    def open_menu(self, event):
        if not self.menu_open:
            self.object_colour_options['menu'].tk_popup(self.properties_window.winfo_x() + 8, self.properties_window.winfo_y() + 125)
            self.menu_open = True
        else:
            self.menu_open = False

    def close_menu(self, event):
        self.menu_open = False

    def find_centre(self):
        self.position_x.set(self.viewer_width / 2)
        self.position_y.set(self.viewer_height / 2)
        self.position_z.set(0)

    def copy_world_object(self, event = None):
        self.properties_window = FloatingWindow(self.root, bg = self.bg_colour)
        self.properties_window.geometry("{}x{}+{}+{}".format(self.properties_window_width, 120, int((self.x_off - self.properties_window_width) / 2), int((self.y_off - self.properties_window_height) / 2)))
        self.properties_window.overrideredirect(True)
        self.properties_window.attributes('-topmost', True)
        self.properties_window.create_grip(self.properties_window)

        properties_exit_button = tkinter.Button(self.properties_window, image = self.exit_img, width = self.exit_button_size[0], height = self.exit_button_size[1], command = self.properties_window.destroy, borderwidth=0, bd = -2, bg = self.bg_colour, activebackground=self.highlight_bg_colour)
        properties_exit_button.place(x = self.properties_window_width - self.exit_button_size[0], y = -3, anchor = 'nw')

        object_name = self.world_objects_lb.get(tkinter.ACTIVE)
        object_type =  self.engine_client.engine.objects[object_name].get_type()

        self.properties_window_label = tkinter.Label(self.properties_window, text = 'Copy' + object_name, bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        self.properties_window_label.place(x = 5, y = 0, anchor = 'nw')

        self.object_name = tkinter.StringVar(value = object_name + ' copy')

        object_name_label = tkinter.Label(self.properties_window, text = 'Object Name', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        object_name_label.place(x = 5, y = 30, anchor = 'nw')
        object_name_entry = tkinter.Entry(self.properties_window, textvariable = self.object_name, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
        object_name_entry.place(x = 8, y = 55, anchor = 'nw', height = 18, width = 182)

        copy_button = tkinter.Button(self.properties_window, text="Create " + object_type, fg=self.header_colour, bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= lambda: self.copy_object(object_name, self.object_name.get()), font=self.button_font)
        copy_button.place(x = 190, y = 85, anchor = 'ne', height = 22)

        copy_button.bind('<Enter>', lambda event: self.hover_enter_button(event, copy_button))
        copy_button.bind('<Leave>', lambda event: self.hover_leave_button(event, copy_button))

    def copy_object(self, object_name, new_object_name):
        self.engine_client.engine.copy_object(self.engine_client.engine.objects[object_name], new_object_name)
        self.properties_window.destroy()

    def edit_world_object(self, event = None):
        self.open_object_properties_window(self.world_objects_lb)
        object_name = self.world_objects_lb.get(tkinter.ACTIVE)
        object_3d = self.engine_client.engine.objects[object_name]

        self.properties_window_label.place_forget()
        self.properties_window_label.config(text = object_name + ' Properties')
        self.properties_window_label.place(x = 5, y = 0, anchor = 'nw')

        self.object_name.set(value = object_name)
        self.object_colour.set(value = object_3d.get_colour())
        self.position_x.set(object_3d.get_position()[0])
        self.position_y.set(object_3d.get_position()[1])
        self.position_z.set(object_3d.get_position()[2])

        object_type = object_3d.get_type()

        if object_type == 'Cube':
            self.cube_size.set(object_3d.get_size())

            self.create_button.place_forget()
            self.create_button.config(text = 'Edit \'{}\''.format(object_name), command = lambda: self.update_cube_details(object_name))
            self.create_button.place(x = 190, y = 235, anchor = 'ne', height = 22)

        if object_type == 'Quad':
            self.quad_length.set(object_3d.get_length())
            self.quad_width.set(object_3d.get_width())
            self.quad_height.set(object_3d.get_height())

            self.create_button.place_forget()
            self.create_button.config(text = 'Edit \'{}\''.format(object_name), command =  lambda: self.update_quad_details(object_name))
            self.create_button.place(x = 190, y = 335, anchor = 'ne', height = 22)

        if object_type == 'Plane':
            self.plane_length.set(object_3d.get_length())
            self.plane_width.set(object_3d.get_width())

            self.create_button.place_forget()
            self.create_button.config(text = 'Edit \'{}\''.format(object_name), command =  lambda: self.update_plane_details(object_name))
            self.create_button.place(x = 190, y = 285, anchor = 'ne', height = 22)

        if object_type == 'Polygon':
            self.polygon_no_points.set(object_3d.get_no_points())
            self.polygon_size.set(object_3d.get_size())

            self.create_button.place_forget()
            self.create_button.config(text = 'Edit \'{}\''.format(object_name), command =  lambda: self.update_polygon_details(object_name))
            self.create_button.place(x = 190, y = 285, anchor = 'ne', height = 22)

        if object_type == 'Sphere':
            self.sphere_no_points.set(object_3d.get_verts_res())
            self.sphere_size.set(object_3d.get_radius())

            self.create_button.place_forget()
            self.create_button.config(text = 'Edit \'{}\''.format(object_name), command =  lambda: self.update_sphere_details(object_name))
            self.create_button.place(x = 190, y = 285, anchor = 'ne', height = 22)
        
        if object_type == 'Line2D':
            self.line2D_angle.set(object_3d.get_angle())
            self.line2D_magnitude.set(object_3d.get_magnitude())

            self.create_button.place_forget()
            self.create_button.config(text = 'Edit \'{}\''.format(object_name), command =  lambda: self.update_line2D_details(object_name))
            self.create_button.place(x = 190, y = 285, anchor = 'ne', height = 22)
        
        if object_type == 'Line3D':
            self.position2_x.set(object_3d.get_end_point()[0])
            self.position2_y.set(object_3d.get_end_point()[1])
            self.position2_z.set(object_3d.get_end_point()[2])

            self.create_button.place_forget()
            self.create_button.config(text = 'Edit \'{}\''.format(object_name), command = lambda object_name: self.update_line3D_details(object_name))
            self.create_button.place(x = 190, y = 235, anchor = 'ne', height = 22)

        self.create_button.bind('<Enter>', lambda event: self.hover_enter_button(event, self.create_button))
        self.create_button.bind('<Leave>', lambda event: self.hover_leave_button(event, self.create_button))

    def open_object_properties_window(self, listbox):
        self.properties_window = FloatingWindow(self.root, bg = self.bg_colour)
        self.properties_window.geometry("{}x{}+{}+{}".format(self.properties_window_width, self.properties_window_height, int((self.x_off - self.properties_window_width) / 2), int((self.y_off - self.properties_window_height) / 2)))
        self.properties_window.overrideredirect(True)
        self.properties_window.attributes('-topmost', True)
        self.properties_window.create_grip(self.properties_window)

        properties_exit_button = tkinter.Button(self.properties_window, image = self.exit_img, width = self.exit_button_size[0], height = self.exit_button_size[1], command = self.properties_window.destroy, borderwidth=0, bd = -2, bg = self.bg_colour, activebackground=self.highlight_bg_colour)
        properties_exit_button.place(x = self.properties_window_width - self.exit_button_size[0], y = -3, anchor = 'nw')

        # If the listbox is for world objects then the object type has to be fetched from the get_type() method for the object
        # else the object type can be found directly from the listbox
        try:
            object_type =  self.engine_client.engine.objects[listbox.get(tkinter.ACTIVE)].get_type()
        except:
            object_type = listbox.get(tkinter.ACTIVE)

        self.properties_window_label = tkinter.Label(self.properties_window, text = object_type + ' Properties', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        self.properties_window_label.place(x = 5, y = 0, anchor = 'nw')

        colours = ['red', 'magenta', 'green', 'blue', 'yellow', 'cyan', 'grey']

        self.object_name = tkinter.StringVar(value = object_type)
        self.object_colour = tkinter.StringVar(value = 'Select Colour')
        self.position_x, self.position_y, self.position_z = tkinter.DoubleVar(), tkinter.DoubleVar(), tkinter.DoubleVar()

        object_name_label = tkinter.Label(self.properties_window, text = 'Object Name', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        object_name_label.place(x = 5, y = 30, anchor = 'nw')
        object_name_entry = tkinter.Entry(self.properties_window, textvariable = self.object_name, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
        object_name_entry.place(x = 8, y = 55, anchor = 'nw', height = 18, width = 182)

        down_img = Image.open(r'{}\images\down.png'.format(self.parent_dir))
        self.down_img = ImageTk.PhotoImage(down_img)
        object_colour_label = tkinter.Label(self.properties_window, text = 'Object Colour', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        object_colour_label.place(x = 5, y = 80, anchor = 'nw')
        self.object_colour_options = tkinter.OptionMenu(self.properties_window, self.object_colour, *colours, command = self.close_menu)
        self.object_colour_options.configure(indicatoron=0, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour, activebackground = self.small_button_colour, activeforeground = self.window_title_colour)
        self.object_colour_options['menu'].config(bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, bd = 0)
        self.object_colour_options.place(x = 8, y = 105, anchor = 'nw', height = 18, width = 155)
        self.down_label = tkinter.Label(self.properties_window, image = self.down_img, width = 20, height = 20, borderwidth=0, bd = -2, bg = self.bg_colour, activebackground=self.highlight_bg_colour)
        self.down_label.place(x = 170, y = 105, anchor = 'nw')
        self.down_label.bind('<ButtonPress-1>', self.open_menu)
        self.object_colour_options.bind('<ButtonPress-1>', self.open_menu)

        object_position_label = tkinter.Label(self.properties_window, text = 'Position', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        object_position_label.place(x = 5, y = 130, anchor = 'nw')
        object_x_label = tkinter.Label(self.properties_window, text = 'X', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        object_x_label.place(x = 5, y = 152, anchor = 'nw')
        object_x_entry = tkinter.Entry(self.properties_window, textvariable = self.position_x, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
        object_x_entry.place(x = 20, y = 155, anchor = 'nw', height = 18, width = 45)

        object_y_label = tkinter.Label(self.properties_window, text = 'Y', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        object_y_label.place(x = 67, y = 152, anchor = 'nw')
        object_y_entry = tkinter.Entry(self.properties_window, textvariable = self.position_y, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
        object_y_entry.place(x = 82, y = 155, anchor = 'nw', height = 18, width = 45)

        object_z_label = tkinter.Label(self.properties_window, text = 'Z', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        object_z_label.place(x = 130, y = 152, anchor = 'nw')
        object_z_entry = tkinter.Entry(self.properties_window, textvariable = self.position_z, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
        object_z_entry.place(x = 145, y = 155, anchor = 'nw', height = 18, width = 45)

        object_centre_position_button = tkinter.Button(self.properties_window, text='Centre', fg=self.window_title_colour, bg= self.bg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.bg_colour, activeforeground=self.header_colour, command= self.find_centre, font=self.list_box_font)
        object_centre_position_button.place(x = 192, y = 135, anchor = 'ne', height = 13, width = 40)

        if object_type == 'Cube':
            self.cube_size = tkinter.StringVar(value = 0)
            cube_size_label = tkinter.Label(self.properties_window, text = 'Size', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            cube_size_label.place(x = 5, y = 180, anchor = 'nw')
            cube_size_entry = tkinter.Entry(self.properties_window, textvariable = self.cube_size, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            cube_size_entry.place(x = 8, y = 205, anchor = 'nw', height = 18, width = 182)

            self.create_button = tkinter.Button(self.properties_window, text="Create " + object_type, fg=self.header_colour, bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.create_cube, font=self.button_font)
            self.create_button.place(x = 190, y = 235, anchor = 'ne', height = 22)
            self.properties_window.geometry("{}x{}".format(self.properties_window_width, 270))

        if object_type == 'Quad':
            self.quad_length, self.quad_width, self.quad_height = tkinter.StringVar(value = 0), tkinter.StringVar(value = 0), tkinter.StringVar(value = 0)
            quad_length_label = tkinter.Label(self.properties_window, text = 'Length', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            quad_length_label.place(x = 5, y = 180, anchor = 'nw')
            quad_length_entry = tkinter.Entry(self.properties_window, textvariable = self.quad_length, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            quad_length_entry.place(x = 8, y = 205, anchor = 'nw', height = 18, width = 182)
            quad_width_label = tkinter.Label(self.properties_window, text = 'Width', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            quad_width_label.place(x = 5, y = 230, anchor = 'nw')
            quad_width_entry = tkinter.Entry(self.properties_window, textvariable = self.quad_width, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            quad_width_entry.place(x = 8, y = 255, anchor = 'nw', height = 18, width = 182)
            quad_height_label = tkinter.Label(self.properties_window, text = 'Height', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            quad_height_label.place(x = 5, y = 280, anchor = 'nw')
            quad_height_entry = tkinter.Entry(self.properties_window, textvariable = self.quad_height, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            quad_height_entry.place(x = 8, y = 305, anchor = 'nw', height = 18, width = 182)

            self.create_button = tkinter.Button(self.properties_window, text="Create " + object_type, fg=self.header_colour, bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.create_quad, font=self.button_font)
            self.create_button.place(x = 190, y = 335, anchor = 'ne', height = 22)
            self.properties_window.geometry("{}x{}".format(self.properties_window_width, 370))

        if object_type == 'Plane':
            self.plane_length, self.plane_width = tkinter.StringVar(value = 0), tkinter.StringVar(value = 0)
            plane_length_label = tkinter.Label(self.properties_window, text = 'Length', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            plane_length_label.place(x = 5, y = 180, anchor = 'nw')
            plane_length_entry = tkinter.Entry(self.properties_window, textvariable = self.plane_length, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            plane_length_entry.place(x = 8, y = 205, anchor = 'nw', height = 18, width = 182)
            plane_width_label = tkinter.Label(self.properties_window, text = 'Width', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            plane_width_label.place(x = 5, y = 230, anchor = 'nw')
            plane_width_entry = tkinter.Entry(self.properties_window, textvariable = self.plane_width, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            plane_width_entry.place(x = 8, y = 255, anchor = 'nw', height = 18, width = 182)

            self.create_button = tkinter.Button(self.properties_window, text="Create " + object_type, fg=self.header_colour, bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.create_plane, font=self.button_font)
            self.create_button.place(x = 190, y = 285, anchor = 'ne', height = 22)
            self.properties_window.geometry("{}x{}".format(self.properties_window_width, 320))

        if object_type == 'Polygon':
            self.polygon_size, self.polygon_no_points = tkinter.StringVar(value = 0), tkinter.StringVar(value = 0)
            polygon_size_label = tkinter.Label(self.properties_window, text = 'Size', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            polygon_size_label.place(x = 5, y = 180, anchor = 'nw')
            polygon_size_entry = tkinter.Entry(self.properties_window, textvariable = self.polygon_size, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            polygon_size_entry.place(x = 8, y = 205, anchor = 'nw', height = 18, width = 182)

            polygon_no_points_label = tkinter.Label(self.properties_window, text = 'Number of Vertices', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            polygon_no_points_label.place(x = 5, y = 230, anchor = 'nw')
            polygon_no_points_entry = tkinter.Entry(self.properties_window, textvariable = self.polygon_no_points, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            polygon_no_points_entry.place(x = 8, y = 255, anchor = 'nw', height = 18, width = 182)

            self.create_button = tkinter.Button(self.properties_window, text="Create " + object_type, fg=self.header_colour, bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.create_polygon, font=self.button_font)
            self.create_button.place(x = 190, y = 285, anchor = 'ne', height = 22)
            self.properties_window.geometry("{}x{}".format(self.properties_window_width, 320))

        if object_type == 'Sphere':
            self.sphere_size, self.sphere_no_points = tkinter.StringVar(value = 0), tkinter.StringVar(value = 0)
            sphere_size_label = tkinter.Label(self.properties_window, text = 'Radius', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            sphere_size_label.place(x = 5, y = 180, anchor = 'nw')
            sphere_size_entry = tkinter.Entry(self.properties_window, textvariable = self.sphere_size, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            sphere_size_entry.place(x = 8, y = 205, anchor = 'nw', height = 18, width = 182)

            sphere_no_points_label = tkinter.Label(self.properties_window, text = 'Vertices Resolution', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            sphere_no_points_label.place(x = 5, y = 230, anchor = 'nw')
            sphere_no_points_entry = tkinter.Entry(self.properties_window, textvariable = self.sphere_no_points, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            sphere_no_points_entry.place(x = 8, y = 255, anchor = 'nw', height = 18, width = 182)

            self.create_button = tkinter.Button(self.properties_window, text="Create " + object_type, fg=self.header_colour, bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.create_sphere, font=self.button_font)
            self.create_button.place(x = 190, y = 285, anchor = 'ne', height = 22)
            self.properties_window.geometry("{}x{}".format(self.properties_window_width, 320))

        if object_type == 'Line2D':
            self.line2D_angle, self.line2D_magnitude = tkinter.DoubleVar(), tkinter.StringVar(value = 0)
            line2D_angle_label = tkinter.Label(self.properties_window, text = 'Angle (degrees)', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            line2D_angle_label.place(x = 5, y = 180, anchor = 'nw')
            line2D_angle_entry = tkinter.Entry(self.properties_window, textvariable = self.line2D_angle, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            line2D_angle_entry.place(x = 8, y = 205, anchor = 'nw', height = 18, width = 182)

            line2D_magnitude_label = tkinter.Label(self.properties_window, text = 'Magnitude', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            line2D_magnitude_label.place(x = 5, y = 230, anchor = 'nw')
            line2D_magnitude_entry = tkinter.Entry(self.properties_window, textvariable = self.line2D_magnitude, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            line2D_magnitude_entry.place(x = 8, y = 255, anchor = 'nw', height = 18, width = 182)

            self.create_button = tkinter.Button(self.properties_window, text="Create " + object_type, fg=self.header_colour, bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.create_line2D, font=self.button_font)
            self.create_button.place(x = 190, y = 285, anchor = 'ne', height = 22)
            self.properties_window.geometry("{}x{}".format(self.properties_window_width, 320))

        if object_type == 'Line3D':
            self.position2_x, self.position2_y, self.position2_z = tkinter.DoubleVar(), tkinter.DoubleVar(), tkinter.DoubleVar()
            object_position_label.config(text = 'First Point Position')

            object_position2_label = tkinter.Label(self.properties_window, text = 'Second Point Position', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            object_position2_label.place(x = 5, y = 180, anchor = 'nw')
            object_x_label = tkinter.Label(self.properties_window, text = 'X', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            object_x_label.place(x = 5, y = 202, anchor = 'nw')
            object_x_entry = tkinter.Entry(self.properties_window, textvariable = self.position2_x, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            object_x_entry.place(x = 20, y = 205, anchor = 'nw', height = 18, width = 45)

            object_y_label = tkinter.Label(self.properties_window, text = 'Y', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            object_y_label.place(x = 67, y = 202, anchor = 'nw')
            object_y_entry = tkinter.Entry(self.properties_window, textvariable = self.position2_y, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            object_y_entry.place(x = 82, y = 205, anchor = 'nw', height = 18, width = 45)

            object_z_label = tkinter.Label(self.properties_window, text = 'Z', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
            object_z_label.place(x = 130, y = 202, anchor = 'nw')
            object_z_entry = tkinter.Entry(self.properties_window, textvariable = self.position2_z, bg=self.small_button_colour, fg=self.window_title_colour, font=self.list_box_font, highlightcolor = self.fg_colour, bd = 0, highlightthickness = '1', highlightbackground = self.embeded_colour)
            object_z_entry.place(x = 145, y = 205, anchor = 'nw', height = 18, width = 45)

            self.create_button = tkinter.Button(self.properties_window, text="Create " + object_type, fg=self.header_colour, bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.create_line3D, font=self.button_font)
            self.create_button.place(x = 190, y = 235, anchor = 'ne', height = 22)
            self.properties_window.geometry("{}x{}".format(self.properties_window_width, 270))

        self.create_button.bind('<Enter>', lambda event: self.hover_enter_button(event, self.create_button))
        self.create_button.bind('<Leave>', lambda event: self.hover_leave_button(event, self.create_button))

    def create_cube(self):
        position = self.position_x.get(), self.position_y.get(), self.position_z.get()
        self.engine_client.engine.add_object(Cube(self.object_name.get(), position, int(self.cube_size.get()), self.object_colour.get()))
        self.properties_window.destroy()

    def create_quad(self):
        position = self.position_x.get(), self.position_y.get(), self.position_z.get()
        self.engine_client.engine.add_object(Quad(self.object_name.get(), position, int(self.quad_length.get()), int(self.quad_width.get()), int(self.quad_height.get()), self.object_colour.get()))
        self.properties_window.destroy()

    def create_plane(self):
        position = self.position_x.get(), self.position_y.get(), self.position_z.get()
        self.engine_client.engine.add_object(Plane(self.object_name.get(), position, int(self.plane_length.get()), int(self.plane_width.get()), self.object_colour.get()))
        self.properties_window.destroy()

    def create_polygon(self):
        position = self.position_x.get(), self.position_y.get(), self.position_z.get()
        self.engine_client.engine.add_object(Polygon(self.object_name.get(), position, int(self.polygon_size.get()), int(self.polygon_no_points.get()), self.object_colour.get()))
        self.properties_window.destroy()

    def create_sphere(self):
        position = self.position_x.get(), self.position_y.get(), self.position_z.get()
        self.engine_client.engine.add_object(Sphere(self.object_name.get(), position, int(self.sphere_size.get()), int(self.sphere_no_points.get()), self.object_colour.get()))
        self.properties_window.destroy()

    def create_line2D(self):
        position = self.position_x.get(), self.position_y.get(), self.position_z.get()
        self.engine_client.engine.add_object(Line2D(self.object_name.get(), position, self.line2D_angle.get(), int(self.line2D_magnitude.get()), self.object_colour.get()))
        self.properties_window.destroy()

    def create_line3D(self):
        position = self.position_x.get(), self.position_y.get(), self.position_z.get()
        positon2 = self.position2_x.get(), self.position2_y.get(), self.position2_z.get()
        self.engine_client.engine.add_object(Line3D(self.object_name.get(), position, positon2, self.object_colour.get()))
        self.properties_window.destroy()

    def update_cube_details(self, object_name):
        object_3d = self.engine_client.engine.objects[object_name]
        object_3d.set_position((self.position_x.get(), self.position_y.get(), self.position_z.get()))
        object_3d.set_colour(self.object_colour.get())

        old_name = object_3d.get_name()
        new_name = self.object_name.get()
        object_3d.set_name(new_name)
        # Object dictionary is updated so that the new name replaces the old key
        self.engine_client.engine.update_objects_key(old_name, new_name)
        self.world_objects_lb.delete(tkinter.ACTIVE)
        self.world_objects_lb.insert(tkinter.ACTIVE, new_name)

        object_3d.set_size(int(self.cube_size.get()))

        self.properties_window.destroy()

    def update_quad_details(self, object_name):
        object_3d = self.engine_client.engine.objects[object_name]
        object_3d.set_position((self.position_x.get(), self.position_y.get(), self.position_z.get()))
        object_3d.set_colour(self.object_colour.get())

        old_name = object_3d.get_name()
        new_name = self.object_name.get()
        object_3d.set_name(new_name)
        # Object dictionary is updated so that the new name replaces the old key
        self.engine_client.engine.update_objects_key(old_name, new_name)
        self.world_objects_lb.delete(tkinter.ACTIVE)
        self.world_objects_lb.insert(tkinter.ACTIVE, new_name)

        object_3d.set_length(int(self.quad_length.get()))
        object_3d.set_width(int(self.quad_width.get()))
        object_3d.set_height(int(self.quad_height.get()))

        self.properties_window.destroy()

    def update_plane_details(self, object_name):
        object_3d = self.engine_client.engine.objects[object_name]
        object_3d.set_position((self.position_x.get(), self.position_y.get(), self.position_z.get()))
        object_3d.set_colour(self.object_colour.get())

        old_name = object_3d.get_name()
        new_name = self.object_name.get()
        object_3d.set_name(new_name)
        # Object dictionary is updated so that the new name replaces the old key
        self.engine_client.engine.update_objects_key(old_name, new_name)
        self.world_objects_lb.delete(tkinter.ACTIVE)
        self.world_objects_lb.insert(tkinter.ACTIVE, new_name)

        object_3d.set_length(int(self.plane_length.get()))
        object_3d.set_width(int(self.plane_width.get()))

        self.properties_window.destroy()

    def update_polygon_details(self, object_name):
        object_3d = self.engine_client.engine.objects[object_name]
        object_3d.set_position((self.position_x.get(), self.position_y.get(), self.position_z.get()))
        object_3d.set_colour(self.object_colour.get())

        old_name = object_3d.get_name()
        new_name = self.object_name.get()
        object_3d.set_name(new_name)
        # Object dictionary is updated so that the new name replaces the old key
        self.engine_client.engine.update_objects_key(old_name, new_name)
        self.world_objects_lb.delete(tkinter.ACTIVE)
        self.world_objects_lb.insert(tkinter.ACTIVE, new_name)

        object_3d.set_no_points(int(self.polygon_no_points.get()))
        object_3d.set_size(int(self.polygon_size.get()))

        self.properties_window.destroy()

    def update_sphere_details(self, object_name):
        object_3d = self.engine_client.engine.objects[object_name]
        object_3d.set_position((self.position_x.get(), self.position_y.get(), self.position_z.get()))
        object_3d.set_colour(self.object_colour.get())

        old_name = object_3d.get_name()
        new_name = self.object_name.get()
        object_3d.set_name(new_name)
        # Object dictionary is updated so that the new name replaces the old key
        self.engine_client.engine.update_objects_key(old_name, new_name)
        self.world_objects_lb.delete(tkinter.ACTIVE)
        self.world_objects_lb.insert(tkinter.ACTIVE, new_name)

        object_3d.set_radius(int(self.sphere_size.get()))
        object_3d.set_verts_res(int(self.sphere_no_points.get()))
        self.properties_window.destroy()

    def update_line2D_details(self, object_name):
        object_3d = self.engine_client.engine.objects[object_name]
        object_3d.set_position((self.position_x.get(), self.position_y.get(), self.position_z.get()))
        object_3d.set_colour(self.object_colour.get())

        old_name = object_3d.get_name()
        new_name = self.object_name.get()
        object_3d.set_name(new_name)
        # Object dictionary is updated so that the new name replaces the old key
        self.engine_client.engine.update_objects_key(old_name, new_name)
        self.world_objects_lb.delete(tkinter.ACTIVE)
        self.world_objects_lb.insert(tkinter.ACTIVE, new_name)

        object_3d.set_angle(int(self.line2D_angle.get()))
        object_3d.set_magnitude(int(self.line2D_magnitude.get()))

        self.properties_window.destroy()

    def update_line3D_details(self, object_name):
        object_3d = self.engine_client.engine.objects[object_name]
        object_3d.set_position((self.position_x.get(), self.position_y.get(), self.position_z.get()))
        object_3d.set_colour(self.object_colour.get())

        old_name = object_3d.get_name()
        new_name = self.object_name.get()
        object_3d.set_name(new_name)
        # Object dictionary is updated so that the new name replaces the old key
        self.engine_client.engine.update_objects_key(old_name, new_name)
        self.world_objects_lb.delete(tkinter.ACTIVE)
        self.world_objects_lb.insert(tkinter.ACTIVE, new_name)

        object_3d.set_start_point((self.position_x.get(), self.position_y.get(), self.position_z.get()))
        object_3d.set_end_point((self.position2_x.get(), self.position2_y.get(), self.position2_z.get()))

        self.properties_window.destroy()

    def selected_exists(self, list_box):
        selected = False
        if len(list_box.curselection()) > 0:
            selected = True
        return selected

    def update_world_objects(self):
        object_names = self.engine_client.engine.objects.keys()
        for i, object_name in enumerate(object_names):
            if i >= self.world_objects_lb.size():
                self.world_objects_lb.insert(tkinter.END, object_name)
        self.world_objects_lb.place(x = self.details_width - self.world_space_padding, y = 30, anchor = 'n', height = self.world_objects_list_box_height)
        if self.world_objects_lb.size() > self.world_space_dimensions[1]:
            self.world_objects_scrollbar.place(x = self.details_width - 7, y = 30, anchor = 'n', height = self.world_objects_list_box_height)

        # If there are no more objects left in the world to delete / edit or if an object has not been selected, remove delete_world_object_button from the tkinter window
        if self.world_objects_lb.size() > 0 and self.selected_exists(self.world_objects_lb):  
            self.delete_world_object_button.place(x= self.object_details_bg_size_x + self.object_details_bg_padding[0] + 5, y = 10, anchor = 'nw', height = 22)
            self.edit_world_object_button.place(x= self.object_details_bg_size_x + self.object_details_bg_padding[0] + 5, y = 40, anchor = 'nw', height = 22)
            self.copy_world_object_button.place(x= self.object_details_bg_size_x + self.object_details_bg_padding[0] + 5, y = 70, anchor = 'nw', height = 22)
        else:
            self.delete_world_object_button.place_forget()
            self.edit_world_object_button.place_forget()
            self.copy_world_object_button.place_forget()

    def construct_fps_graph_labels(self):
        self.max_fps_label = tkinter.Label(self.details, text='Max FPS: {}'.format(0), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        self.max_fps_label.place(x = 0, y = self.max_label_padding, anchor = 'nw')
        self.min_fps_label = tkinter.Label(self.details, text='Min FPS: {}'.format(0), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        self.min_fps_label.place(x = 0, y = self.details_height - self.min_label_padding, anchor = 'sw')
        self.avg_fps_label = tkinter.Label(self.details, text='Mean FPS: {}'.format(0), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        self.avg_fps_label.place(x = 0, y = self.details_height / 2, anchor = 'w')

    def construct_binary_sliders(self):
        display_surfaces_label = tkinter.Label(self.control, text='Display Surfaces', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        display_surfaces_label.place(x = self.label_padding[0], y = self.label_padding[1], anchor = 'w')
        self.display_surfaces_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=50, width=15, sliderlength=15, from_=0, to=1, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_display_surfaces)
        self.display_surfaces_slider.set(self.engine_client.display_surfaces)
        self.display_surfaces_slider.place(x=self.label_padding[0] + self.slider_padding[0], y = self.label_padding[1] + self.slider_padding[1], anchor = 'w')

        display_lines_label = tkinter.Label(self.control, text='Display Lines', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        display_lines_label.place(x = self.label_padding[0], y = self.label_padding[1] + self.slider_offset, anchor = 'w')
        self.display_lines_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=50, width=15, sliderlength=15, from_=0, to=1, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_display_lines)
        self.display_lines_slider.set(self.engine_client.display_lines)
        self.display_lines_slider.place(x=self.label_padding[0] + self.slider_padding[0], y = self.label_padding[1] + self.slider_padding[1] + self.slider_offset, anchor = 'w')

        display_points_label = tkinter.Label(self.control, text='Display Points', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        display_points_label.place(x = self.label_padding[0], y = self.label_padding[1] + self.slider_offset * 2, anchor = 'w')
        self.display_points_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=50, width=15, sliderlength=15, from_=0, to=1, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_display_points)
        self.display_points_slider.set(self.engine_client.display_points)
        self.display_points_slider.place(x=self.label_padding[0] + self.slider_padding[0], y = self.label_padding[1] + self.slider_padding[1] + self.slider_offset * 2, anchor = 'w')

        debug_mode_label = tkinter.Label(self.control, text='Debug Mode', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        debug_mode_label.place(x = self.label_padding[0], y = self.label_padding[1] + self.slider_offset * 3, anchor = 'w')
        self.debug_mode_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=50, width=15, sliderlength=15, from_=0, to=1, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_debug_mode)
        self.debug_mode_slider.set(self.engine_client.debug_mode)
        self.debug_mode_slider.place(x=self.label_padding[0] + self.slider_padding[0], y = self.label_padding[1] + self.slider_padding[1] + self.slider_offset * 3, anchor = 'w')

        display_hud_label = tkinter.Label(self.control, text='Display HUD', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        display_hud_label.place(x = self.label_padding[0], y = self.label_padding[1] + self.slider_offset * 4, anchor = 'w')
        self.display_hud_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=50, width=15, sliderlength=15, from_=0, to=1, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_display_hud)
        self.display_hud_slider.set(self.engine_client.display_hud)
        self.display_hud_slider.place(x=self.label_padding[0] + self.slider_padding[0], y = self.label_padding[1] + self.slider_padding[1] + self.slider_offset * 4, anchor = 'w')

        display_logo_label = tkinter.Label(self.control, text='Display Logo', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        display_logo_label.place(x = self.label_padding[0], y = self.label_padding[1] + self.slider_offset * 5, anchor = 'w')
        self.display_logo_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=50, width=15, sliderlength=15, from_=0, to=1, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_display_logo)
        self.display_logo_slider.set(self.engine_client.display_logo)
        self.display_logo_slider.place(x=self.label_padding[0] + self.slider_padding[0], y = self.label_padding[1] + self.slider_padding[1] + self.slider_offset * 5, anchor = 'w')

    def construct_buttons(self):
        self.save_objects_button = tkinter.Button(self.control, text="Save World", fg="white", bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.save_objects, font=self.small_button_font)
        self.save_objects_button.place(x= 20, y = self.button_padding[1] + self.button_offset * 0.5, anchor = 'nw', height = 25)

        self.import_objects_button = tkinter.Button(self.control, text="Import World", fg="white", bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.import_objects, font=self.small_button_font)
        self.import_objects_button.place(x= self.control_width - 20, y = self.button_padding[1] + self.button_offset * 0.5, anchor = 'ne', height = 25)

        self.reset_fps_button = tkinter.Button(self.control, text="Reset FPS", fg="white", bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.engine_client.reset_fps_graph, font=self.small_button_font)   
        self.reset_fps_button.place(x= 20, y = self.button_padding[1] + self.button_offset * 1.5, anchor = 'nw', height = 25)

        self.reset_anchor_button = tkinter.Button(self.control, text="Reset Anchor", fg="white", bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.engine_client.reset_rotation_anchor, font=self.small_button_font)   
        self.reset_anchor_button.place(x= self.control_width - 20, y = self.button_padding[1] + self.button_offset * 1.5, anchor = 'ne', height = 25)

        self.clear_worldspace_button = tkinter.Button(self.control, text="Clear World", fg="white", bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.clear_worldspace, font=self.small_button_font)
        self.clear_worldspace_button.place(x= 20, y = self.button_padding[1] + self.button_offset * 2.5, anchor = 'nw', height = 25)

        self.delete_worldspace_button = tkinter.Button(self.control, text="Delete Save", fg="white", bg= self.fg_colour, borderwidth=0, height = 1, width = 12, activebackground=self.highlight_fg_colour, activeforeground="white", command= self.delete_world, font=self.small_button_font)
        self.delete_worldspace_button.place(x= self.control_width - 20, y = self.button_padding[1] + self.button_offset * 2.5, anchor = 'ne', height = 25)

        self.import_objects_button.bind('<Enter>', lambda event: self.hover_enter_button(event, self.import_objects_button))
        self.import_objects_button.bind('<Leave>', lambda event: self.hover_leave_button(event, self.import_objects_button))

        self.save_objects_button.bind('<Enter>', lambda event: self.hover_enter_button(event, self.save_objects_button))
        self.save_objects_button.bind('<Leave>', lambda event: self.hover_leave_button(event, self.save_objects_button))

        self.reset_fps_button.bind('<Enter>', lambda event: self.hover_enter_button(event, self.reset_fps_button))
        self.reset_fps_button.bind('<Leave>', lambda event: self.hover_leave_button(event, self.reset_fps_button))

        self.reset_anchor_button.bind('<Enter>', lambda event: self.hover_enter_button(event, self.reset_anchor_button))
        self.reset_anchor_button.bind('<Leave>', lambda event: self.hover_leave_button(event, self.reset_anchor_button))

        self.clear_worldspace_button.bind('<Enter>', lambda event: self.hover_enter_button(event, self.clear_worldspace_button))
        self.clear_worldspace_button.bind('<Leave>', lambda event: self.hover_leave_button(event, self.clear_worldspace_button))

        self.delete_worldspace_button.bind('<Enter>', lambda event: self.hover_enter_button(event, self.delete_worldspace_button))
        self.delete_worldspace_button.bind('<Leave>', lambda event: self.hover_leave_button(event, self.delete_worldspace_button))

    def construct_linear_sliders(self):
        rotation_factor_label = tkinter.Label(self.control, text='Rotation Factor', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        rotation_factor_label.place(x = self.label_padding[0], y = self.label_padding[1] + self.slider_offset * 13 - self.one_line_label_padding, anchor = 'w')
        self.rotation_factor_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=185, width=10, sliderlength=10, from_= 1, to= 100, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_rotation_factor)
        self.rotation_factor_slider.set(self.engine_client.rotation_factor * 100)
        self.rotation_factor_slider.place(x=self.long_slider_offset[0], y = self.label_padding[1] + self.slider_padding[1] + self.slider_offset * 13, anchor = 'w')
        self.rotation_factor_value = tkinter.Label(self.control, text='{0:.2f}'.format(self.rotation_factor_slider.get()), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        self.rotation_factor_value.place(x = self.control_width - self.one_line_value_padding, y = self.label_padding[1] + self.slider_offset * 13 - self.one_line_label_padding, anchor = 'e')

        scaling_factor_label = tkinter.Label(self.control, text='Scaling Factor', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        scaling_factor_label.place(x = self.label_padding[0], y = self.label_padding[1] + self.slider_offset * 14.5 - self.one_line_label_padding, anchor = 'w')
        self.scaling_factor_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=185, width=10, sliderlength=10, from_= 101, to= 150, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_scaling_factor)
        self.scaling_factor_slider.set(self.engine_client.scaling_factor * 100)
        self.scaling_factor_slider.place(x=self.long_slider_offset[0], y = self.label_padding[1] + self.slider_padding[1] + self.slider_offset * 14.5, anchor = 'w')
        self.scaling_factor_value = tkinter.Label(self.control, text='{0:.2f}'.format(self.scaling_factor_slider.get()), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        self.scaling_factor_value.place(x = self.control_width - self.one_line_value_padding, y = self.label_padding[1] + self.slider_offset * 14.5 - self.one_line_label_padding, anchor = 'e')

        translation_factor_label = tkinter.Label(self.control, text='Translation Factor', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        translation_factor_label.place(x = self.label_padding[0], y = self.label_padding[1] + self.slider_offset * 16 - self.one_line_label_padding, anchor = 'w')
        self.translation_factor_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=185, width=10, sliderlength=10, from_= 1, to= 100, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_translation_factor)
        self.translation_factor_slider.set(self.engine_client.translation_factor)
        self.translation_factor_slider.place(x=self.long_slider_offset[0], y = self.label_padding[1] + self.slider_padding[1] + self.slider_offset * 16, anchor = 'w')
        self.translation_factor_value = tkinter.Label(self.control, text='{0:.2f}'.format(self.translation_factor_slider.get()), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        self.translation_factor_value.place(x = self.control_width - self.one_line_value_padding, y = self.label_padding[1] + self.slider_offset * 16 - self.one_line_label_padding, anchor = 'e')

        movement_factor_label = tkinter.Label(self.control, text='Movement Factor', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        movement_factor_label.place(x = self.label_padding[0], y = self.label_padding[1] + self.slider_offset * 17.5 - self.one_line_label_padding, anchor = 'w')
        self.movement_factor_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=185, width=10, sliderlength=10, from_= 1, to= 200, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_movement_factor)
        self.movement_factor_slider.set(self.engine_client.movement_factor)
        self.movement_factor_slider.place(x=self.long_slider_offset[0], y = self.label_padding[1] + self.slider_padding[1] + self.slider_offset * 17.5, anchor = 'w')
        self.movement_factor_value = tkinter.Label(self.control, text='{0:.2f}'.format(self.movement_factor_slider.get()), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        self.movement_factor_value.place(x = self.control_width - self.one_line_value_padding, y = self.label_padding[1] + self.slider_offset * 17.5 - self.one_line_label_padding, anchor = 'e')

        max_frame_rate_label = tkinter.Label(self.control, text='Max Frame Rate', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        max_frame_rate_label.place(x = self.label_padding[0], y = self.label_padding[1] + self.slider_offset * 19 - self.one_line_label_padding, anchor = 'w')
        self.max_frame_rate_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=185, width=10, sliderlength=10, from_= 1, to= 1000, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_max_frame_rate)
        self.max_frame_rate_slider.set(self.engine_client.max_frame_rate)
        self.max_frame_rate_slider.place(x=self.long_slider_offset[0], y = self.label_padding[1] + self.slider_padding[1] + self.slider_offset * 19, anchor = 'w')
        self.max_frame_rate_value = tkinter.Label(self.control, text='{0:.2f}'.format(self.max_frame_rate_slider.get()), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        self.max_frame_rate_value.place(x = self.control_width - self.one_line_value_padding, y = self.label_padding[1] + self.slider_offset * 19 - self.one_line_label_padding, anchor = 'e')

        max_render_distance_label = tkinter.Label(self.control, text='Max Render Distance', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        max_render_distance_label.place(x = self.label_padding[0], y = self.label_padding[1] + self.slider_offset * 20.5 - self.one_line_label_padding, anchor = 'w')
        self.max_render_distance_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=185, width=10, sliderlength=10, from_= 0, to= 25, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_max_render_distance)
        self.max_render_distance_slider.set(self.engine_client.max_render_distance)
        self.max_render_distance_slider.place(x=self.long_slider_offset[0], y = self.label_padding[1] + self.slider_padding[1] + self.slider_offset * 20.5, anchor = 'w')
        self.max_render_distance_value = tkinter.Label(self.control, text='{0:.2f}'.format(self.max_render_distance_slider.get()), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        self.max_render_distance_value.place(x = self.control_width - self.one_line_value_padding, y = self.label_padding[1] + self.slider_offset * 20.5 - self.one_line_label_padding, anchor = 'e')

        min_render_distance_label = tkinter.Label(self.control, text='Min Render Distance', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        min_render_distance_label.place(x = self.label_padding[0], y = self.label_padding[1] + self.slider_offset * 22 - self.one_line_label_padding, anchor = 'w')
        self.min_render_distance_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=185, width=10, sliderlength=10, from_= 100, to= 1, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_min_render_distance)
        self.min_render_distance_slider.set(data_handling.div_non_zero(1, (self.engine_client.min_render_distance * 1000)))
        self.min_render_distance_slider.place(x=self.long_slider_offset[0], y = self.label_padding[1] + self.slider_padding[1] + self.slider_offset * 22, anchor = 'w')
        self.min_render_distance_value = tkinter.Label(self.control, text='{0:.2f}'.format(self.min_render_distance_slider.get()), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        self.min_render_distance_value.place(x = self.control_width - self.one_line_value_padding, y = self.label_padding[1] + self.slider_offset * 22 - self.one_line_label_padding, anchor = 'e')

        lighting_factor_label = tkinter.Label(self.control, text='Lighting Factor', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        lighting_factor_label.place(x = self.label_padding[0], y = self.label_padding[1] + self.slider_offset * 23.5 - self.one_line_label_padding, anchor = 'w')
        self.lighting_factor_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=185, width=10, sliderlength=10, from_= 0, to= 250, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_lighting_factor)
        self.lighting_factor_slider.set(self.engine_client.lighting_factor * 100)
        self.lighting_factor_slider.place(x=self.long_slider_offset[0], y = self.label_padding[1] + self.slider_padding[1] + self.slider_offset * 23.5, anchor = 'w')
        self.lighting_factor_value = tkinter.Label(self.control, text='{0:.2f}'.format(self.lighting_factor_slider.get()), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        self.lighting_factor_value.place(x = self.control_width - self.one_line_value_padding, y = self.label_padding[1] + self.slider_offset * 23.5 - self.one_line_label_padding, anchor = 'e')

        point_radius_label = tkinter.Label(self.control, text='Point Radius', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        point_radius_label.place(x = self.label_padding[0], y = self.label_padding[1] + self.slider_offset * 25 - self.one_line_label_padding, anchor = 'w')
        self.point_radius_slider = tkinter.Scale(self.control, orient=tkinter.HORIZONTAL, length=185, width=10, sliderlength=10, from_= 1, to= 10, bg=self.fg_colour, bd=0, borderwidth=0, activebackground=self.highlight_fg_colour, highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor=self.embeded_colour, command = self.update_point_radius)
        self.point_radius_slider.set(self.engine_client.point_radius)
        self.point_radius_slider.place(x=self.long_slider_offset[0], y = self.label_padding[1] + self.slider_padding[1] + self.slider_offset * 25, anchor = 'w')
        self.point_radius_value = tkinter.Label(self.control, text='{0:.2f}'.format(self.point_radius_slider.get()), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        self.point_radius_value.place(x = self.control_width - self.one_line_value_padding, y = self.label_padding[1] + self.slider_offset * 25 - self.one_line_label_padding, anchor = 'e')

    def construct_info(self):
        info_string = '\nTotal Logins: ' + str(self.db_manager.query_field('total_logins', 'username', self.engine_client.login_sys.get_username()))
        username_label = tkinter.Label(self.control, text= 'User ID', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        username_label.place(x = 0 + self.info_label_padding[0], y = self.username_label_offset, anchor = 'nw')
        username_value_label = tkinter.Label(self.control, text= str(self.engine_client.login_sys.get_username()), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        username_value_label.place(x = self.control_width - self.info_label_padding[0], y = self.username_label_offset, anchor = 'ne')

        registered_label = tkinter.Label(self.control, text= 'Registered', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        registered_label.place(x = 0 + self.info_label_padding[0], y = self.username_label_offset + 1 * self.info_label_padding[1], anchor = 'nw')
        registered_value_label = tkinter.Label(self.control, text= self.db_manager.query_field('registered_time', 'username', self.engine_client.login_sys.get_username())[:-7], bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        registered_value_label.place(x = self.control_width - self.info_label_padding[0], y = 1 * self.username_label_offset + self.info_label_padding[1], anchor = 'ne')

        last_label = tkinter.Label(self.control, text= 'Last Login', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        last_label.place(x = 0 + self.info_label_padding[0], y = self.username_label_offset + 2 * self.info_label_padding[1], anchor = 'nw')
        last_value_label = tkinter.Label(self.control, text= self.check_if_previous_login(), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        last_value_label.place(x = self.control_width - self.info_label_padding[0], y = self.username_label_offset + 2 * self.info_label_padding[1], anchor = 'ne')

        total_logins_label = tkinter.Label(self.control, text= 'Total Logins', bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        total_logins_label.place(x = 0 + self.info_label_padding[0], y = self.username_label_offset + 3 * self.info_label_padding[1], anchor = 'nw')
        total_logins_value_label = tkinter.Label(self.control, text= str(self.db_manager.query_field('total_logins', 'username', self.engine_client.login_sys.get_username())), bg=self.bg_colour, fg=self.window_title_colour, font=self.label_font)
        total_logins_value_label.place(x = self.control_width - self.info_label_padding[0], y = self.username_label_offset + 3 * self.info_label_padding[1], anchor = 'ne')

    def check_if_previous_login(self):
        result = self.db_manager.query_field('login_time', 'username', self.engine_client.login_sys.get_username())
        if result == None:
            return 'No Previous Login'
        else:
            return result[:-7]

    def animate_fps_graph(self):
        fps_animation = animation.FuncAnimation(self.fps_viewer, self.update_fps_graph, interval = self.engine_client.fps_graph_interval)
        return fps_animation

    def update_fps_graph(self, x):
        fps = self.engine_client.clock.get_fps()
        if fps > 0:
            self.engine_client.time_array.append(time.time() - self.engine_client.start_time)
            self.engine_client.fps_array.append(fps)
        if len(self.engine_client.fps_array) > self.engine_client.fps_array_max_length:
            self.engine_client.fps_array = self.engine_client.fps_array[1:]
            self.engine_client.time_array = self.engine_client.time_array[1:]
        if len(self.engine_client.fps_array) > 0:
            min_fps = min(self.engine_client.fps_array)
            max_fps = max(self.engine_client.fps_array)
            avg_fps = sum(self.engine_client.fps_array) / len(self.engine_client.fps_array)
            self.fps_plot.cla()
            # Time array is changed so that only the first and last points are plotted to improve efficiency
            self.fps_plot.plot(self.engine_client.time_array, self.engine_client.fps_array, color = self.graph_colour, linewidth = self.graph_line_width / 2)
            self.fps_plot.plot((self.engine_client.time_array[0], self.engine_client.time_array[-1]), (min_fps, min_fps), color = self.max_min_graph_colour, linewidth = self.max_min_line_width)
            self.fps_plot.plot((self.engine_client.time_array[0], self.engine_client.time_array[-1]), (max_fps, max_fps), color = self.max_min_graph_colour, linewidth = self.max_min_line_width)
            self.fps_plot.plot((self.engine_client.time_array[0], self.engine_client.time_array[-1]), (avg_fps, avg_fps), color = self.avg_graph_colour, linewidth = self.avg_line_width)
            self.max_fps_label.config(text='Max FPS: {}'.format(round(max_fps,2)))
            self.min_fps_label.config(text='Min FPS: {}'.format(round(min_fps,2)))
            self.avg_fps_label.config(text='Mean FPS: {}'.format(round(avg_fps,2)))
            self.avg_fps_label.place(y = int(self.max_label_padding + 12 + (data_handling.div_non_zero(max_fps - avg_fps, (max_fps - min_fps) * 1.30) * 190)))
            self.fps_plot.axis('off')

    def update_display_surfaces(self, value):
        if value == '1':
            self.engine_client.display_surfaces = True 
        elif value == '0':
            self.engine_client.display_surfaces = False

    def update_display_lines(self, value):
        if value == '1':
            self.engine_client.display_lines = True 
        elif value == '0':
            self.engine_client.display_lines = False
    
    def update_display_points(self, value):
        if value == '1':
            self.engine_client.display_points = True 
        elif value == '0':
            self.engine_client.display_points = False

    def update_debug_mode(self, value):
        if value == '1':
            self.engine_client.debug_mode = True 
        elif value == '0':
            self.engine_client.debug_mode = False
    
    def update_display_hud(self, value):
        if value == '1':
            self.engine_client.display_hud = True
        elif value == '0':
            self.engine_client.display_hud = False

    def update_display_logo(self, value):
        if value == '1':
            self.engine_client.display_logo = True
        elif value == '0':
            self.engine_client.display_logo = False
    
    def save_objects(self):
        self.engine_client.db_manager.save_objects(self.engine_client.engine.objects)

    def import_objects(self):
        self.engine_client.db_manager.import_objects(self.engine_client.engine)

    def delete_world(self):
        self.db_manager.remove_save()

    def clear_worldspace(self):
        self.engine_client.engine.clear_all_objects()
        self.world_objects_lb.delete(0, tkinter.END)
        self.draw_object_details() # Used to draw over previous details of a deleted object

    def update_rotation_factor(self, value):
        self.engine_client.rotation_factor = int(value) / 100
        self.rotation_factor_value.config(text = '{0:.2f}'.format(self.engine_client.rotation_factor))

    def update_scaling_factor(self, value):
        self.engine_client.scaling_factor = int(value) / 100
        self.scaling_factor_value.config(text = '{0:.2f}'.format(self.engine_client.scaling_factor))

    def update_translation_factor(self, value):
        self.engine_client.translation_factor = int(value)
        self.translation_factor_value.config(text = '{0:.2f}'.format(self.engine_client.translation_factor))

    def update_movement_factor(self, value):
        self.engine_client.movement_factor = int(value)
        self.movement_factor_value.config(text = '{0:.2f}'.format(self.engine_client.movement_factor))
        pygame.key.set_repeat(1, self.engine_client.movement_factor)

    def update_max_frame_rate(self, value):
        self.engine_client.max_frame_rate = int(value)
        self.max_frame_rate_value.config(text = '{0:.2f}'.format(self.engine_client.max_frame_rate))

    def update_max_render_distance(self, value):
        self.engine_client.max_render_distance = int(value)
        self.max_render_distance_value.config(text = '{0:.2f}'.format(self.engine_client.max_render_distance))

    def update_min_render_distance(self, value):
        self.engine_client.min_render_distance = data_handling.div_non_zero(1, (int(value) * 1000))
        self.min_render_distance_value.config(text = '{0:.2f}'.format(self.engine_client.min_render_distance * 1000))

    def update_lighting_factor(self, value):
        self.engine_client.lighting_factor = int(value) / 100
        self.lighting_factor_value.config(text = '{0:.2f}'.format(self.engine_client.lighting_factor))

    def update_point_radius(self, value):
        self.engine_client.point_radius = int(value)
        self.point_radius_value.config(text = '{0:.2f}'.format(self.engine_client.point_radius))

class FloatingWindow(tkinter.Toplevel):
    ''' A subclass of the Tkinter Toplevel class to allow for dragging the window across the display. '''
    def __init__(self, *args, **kwargs):
        tkinter.Toplevel.__init__(self, *args, **kwargs)

    def create_grip(self, frame):
        frame.bind("<ButtonPress-1>", self.start_motion)
        frame.bind("<ButtonRelease-1>", self.end_motion)
        frame.bind("<B1-Motion>", self.in_motion)

    def start_motion(self, event):
        self.x = event.x
        self.y = event.y

    def end_motion(self, event):
        self.x = None
        self.y = None

    def in_motion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+{}+{}".format(x, y))

class CoordinateInput():
    ''' A set of three input boxes and corresponding labels to allow for the user to enter coordinates the engine. '''
    def __init__(self, x, y, z, point, engine, viewer):
        self.input_boxes = []
        self.input_box_y_padding = 20
        self.input_box_text = [x, y, z]
        self.axis = ['X', 'Y', 'Z']
        self.engine = engine
        self.viewer = viewer

        for i in range(3):
            self.input_boxes.append(InputBox(x, y + self.input_box_y_padding * i, point, '{0:.2f}'.format(self.input_box_text[i]), self, i, self.axis[i]))

    def access_input_boxes(self):
        return self.input_boxes

    def accepting_input(self):
        user_input = False
        for input_box in self.input_boxes:
            if input_box.active == True:
                user_input = True
        return user_input

    def update_points(self, index):
        for i, input_box in enumerate(self.input_boxes):
            new_row = input_box.point[2].points.access_row(input_box.point[3])
            new_row[i] = float(input_box.text)
            input_box.point[2].points.set_row(input_box.point[3], new_row)
            input_box.point[2].project(self.engine.projection_type, self.engine.projection_anchor)
            input_box.text = str(new_row[i])

    def reposition_boxes(self, x, y):
        for i, input_box in enumerate(self.input_boxes):
            input_box.reposition(x, y + self.input_box_y_padding * i)

class InputBox():
    ''' A text box that allows for user input within the engine itself. '''
    def __init__(self, x, y, point, text, coordinate_input, index, axis):
        self.width, self.height = 30, 15
        self.text_box_padding = (25, 9)
        self.label_padding = (10, 10)
        self.label_position = x + self.label_padding[0], y + self.label_padding[1]
        self.rect = pygame.Rect(x + self.text_box_padding[0], y + self.text_box_padding[1], self.width, self.height)
        self.text_box_active_colour = (144, 33, 255)
        self.text_box_inactive_colour = (128, 128, 128)
        self.text_box_text_colour = (255, 255, 255)
        self.input_speed = 10
        self.accepted_characters = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ',', ' ')
        self.text_box_font = pygame.font.Font('./fonts/Montserrat-Medium.ttf', 10)
        self.label_font = pygame.font.Font('./fonts/Montserrat-SemiBold.ttf', 10)
        self.point = point
        self.coordinate_input = coordinate_input
        self.index = index
        self.axis = axis
        self.max_length = 7

        self.rect_colour = self.text_box_inactive_colour
        self.text_colour = self.text_box_inactive_colour
        self.text = text
        self.txt_surface = self.text_box_font.render(text, True, self.rect_colour)
        self.active = False

        self.label = self.label_font.render(self.axis, True, self.text_colour)

    def handle_event(self, event, movement_factor):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                #self.active = not self.active
                self.active = not self.active
            else:
                self.active = False
            self.rect_colour = self.text_box_active_colour if self.active else self.text_box_inactive_colour
            self.text_colour = self.text_box_text_colour if self.active else self.text_box_inactive_colour

            self.txt_surface = self.text_box_font.render(self.text, True, self.text_colour)
            self.label = self.label_font.render(self.axis, True, self.text_colour)

        if event.type == pygame.KEYDOWN:
            if self.active:
                pygame.key.set_repeat(1, self.input_speed)
                if event.key == pygame.K_RETURN:
                    self.coordinate_input.update_points(self.index)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode in self.accepted_characters and len(self.text) < self.max_length:
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.text_box_font.render(self.text, True, self.text_colour)
                self.label = self.label_font.render(self.axis, True, self.text_colour)
                pygame.key.set_repeat(1, movement_factor)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 3, self.rect.y + 1))
        screen.blit(self.label, self.label_position)
        # Blit the rect.
        pygame.draw.rect(screen, self.rect_colour, self.rect, 1)

    def resize(self):
        # Resize the box if the text is too long.
        width = max(self.width, self.txt_surface.get_width() + 8)
        self.rect.w = width

    def reposition(self, x, y):
        self.rect = pygame.Rect(x + self.text_box_padding[0], y + self.text_box_padding[1], self.width, self.height)
        self.label_position = x + self.label_padding[0], y + self.label_padding[1]

class ResponsiveText:
    def __init__(self, x, y, text):
        self.width, self.height = 30, 15
        self.label_padding = (10, 10)
        self.label_position = x + self.label_padding[0], y + self.label_padding[1]
        self.text_colour = (255, 255, 255)
        self.label_font = pygame.font.Font('./fonts/Montserrat-SemiBold.ttf', 10)
        self.label = self.label_font.render(text, True, self.text_colour)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.label, self.label_position)
        # Blit the rect.

    def reposition(self, x, y):
        self.label_position = x + self.label_padding[0], y + self.label_padding[1]