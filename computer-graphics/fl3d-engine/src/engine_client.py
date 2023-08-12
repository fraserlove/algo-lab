# Third party modules
import sys, os, time, datetime
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pathlib import Path
import pygame

# Project-specific modules
from engine_3d import Engine3D
from shapes import GUILines
from database_manager import DatabaseManager
from camera import Camera
from gui import GUI, CoordinateInput, ResponsiveText
from launcher import Launcher
import data_handling

class EngineClient():
    ''' Updates and controls the Engine and GUI Objects to display the running engine. '''
    def __init__(self, width, height, login_sys, path):

        self.line_colour = (255, 255, 255)
        self.point_colour = (255, 255, 255)
        self.bg_colour = (35, 35, 35)
        self.fps_colour = (255, 255, 255)
        self.relative_line_colour = (118, 18, 219)

        self.displacement_arrows = 0
        
        self.fps_array, self.time_array = [], []
        self.fps_array_max_length = 500
        self.fps_graph_interval = 500
        self.start_time = time.time()

        # Initialising all variables used with chosen point and chosen rotation anchor to None
        self.chosen_point, self.chosen_rotation_anchor, self.input_boxes, self.responsive_text = None, None, None, None
        self.clickable_radius = 5 # The radius at which a point can be clicked beyond its shown radius
        self.translating, self.translating_x, self.translating_y = False, False, False
        self.use_custom_rotation_anchor, self.running = False, True

        self.login_sys = login_sys        
        path = os.getcwd()
        self.parent_dir = os.path.join(path, os.pardir)
        Path(r'{}/data'.format(self.parent_dir)).mkdir(parents=True, exist_ok=True)
        Path(r'{}/data/EngineData.db'.format(self.parent_dir)).touch(exist_ok=True)
        self.db_manager = DatabaseManager(r'{}/EngineData.db'.format(self.parent_dir))


        # lighting_factor: Controls the contrast of colour in objects, higher means more contrast
        self.display_surfaces, self.display_lines, self.display_points, \
        self.debug_mode, self.display_hud, self.display_logo, \
        self.rotation_factor, self.scaling_factor, self.translation_factor, \
        self.movement_factor, self.max_frame_rate, self.max_render_distance, \
        self.min_render_distance, self.lighting_factor , self.point_radius = self.db_manager.load_user_settings(self)

        self.camera = Camera(self)
        self.gui = GUI(self, self.db_manager, width, height, path)
        self.engine = Engine3D('orthographic', self.gui.viewer_centre)

        pygame.init()
        self.viewer = pygame.display.set_mode((self.gui.viewer_width, self.gui.viewer_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(r'{}/fonts/Montserrat-SemiBold.ttf'.format(self.parent_dir), 16)
        pygame.key.set_repeat(1, self.movement_factor)
        self.logo = pygame.image.load(r'{}/images/fl3d_small.png'.format(self.parent_dir))
        self.logo_size = (197, 70)

    def reset_rotation_anchor(self):
        self.rotation_anchor = self.engine.entities_centre()

    def reset_fps_graph(self):
        self.fps_array, self.time_array = [], []

    def save_world(self):
        self.db_manager.save_objects(self.engine.objects)

    def remove_world(self):
        self.db_manager.remove_save()

    def debug_display(self, object_3d):
        pygame.draw.circle(self.viewer, (255, 0, 0), (int(object_3d.points.access_index(0, 0)), int(object_3d.points.access_index(0, 1))), self.point_radius, 0)
        pygame.draw.circle(self.viewer, (0, 255, 0), (int(object_3d.find_centre()[0]), int(object_3d.find_centre()[1])), self.point_radius, 0)
        pygame.draw.circle(self.viewer, (0, 0, 255), (int(self.rotation_anchor[0]), int(self.rotation_anchor[1])), self.point_radius, 0)
    
    def close_window(self):
        self.gui.destruct_gui()
        self.running_fps = False
        self.running = False
        self.db_manager.update_login_time(self.login_sys.username, datetime.datetime.now())
        self.db_manager.save_user_settings(self)
        self.db_manager.close_database()
        pygame.quit()

    def minimise_window(self):
        self.gui.window.update_idletasks()
        self.gui.window.overrideredirect(False)
        self.gui.window.state('iconic')
        self.gui.maximise_window = True

    def maximise_window(self, event):
        self.gui.window.update_idletasks()
        self.gui.window.overrideredirect(True)
        if self.gui.maximise_window:
            self.gui.set_appwindow()
            self.gui.maximise_window = False

    def run(self):
        fps_animation = self.gui.animate_fps_graph()
        while self.running:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x) # Ran every update to make sure that cursor stays on pygame cursor when in engine

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in self.camera.controls: 
                        self.camera.controls[event.key](self, self.engine)
                        self.gui.update_object_details()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_translation_lines(pygame.mouse.get_pos())
                    self.translating = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.translating_x, self.translating_y = False, False
                    self.translating = False
                elif event.type == pygame.MOUSEMOTION:
                    self.check_translation(pygame.mouse.get_pos())
                    self.check_rotation_anchor(pygame.mouse.get_pos())
                if self.input_boxes != None:
                    for input_box in self.input_boxes.access_input_boxes():
                        input_box.handle_event(event, self.movement_factor)

            if not self.use_custom_rotation_anchor:
                self.rotation_anchor = self.engine.entities_centre(self.engine.objects)

            self.render_objects()
            self.gui.update_world_objects()
            pygame.display.flip()
            self.clock.tick(self.max_frame_rate)
            self.engine.update_operating_status(False)
            if self.running:
                self.gui.root.update()

    def check_translation_lines(self, mouse_position):
        for rendered_point in self.engine.rendered_points:
            if self.check_object_radius(rendered_point[0], mouse_position):
                self.chosen_rotation_anchor, self.responsive_text = None, None
                self.engine.clear_translation_lines()
                translation_lines = GUILines(rendered_point[1], self.gui.translation_line_length)
                self.engine.set_translation_lines(translation_lines)
                if rendered_point == self.chosen_point:
                    self.engine.clear_translation_lines()
                    self.chosen_point, self.input_boxes = None, None
                else:
                    self.chosen_point = rendered_point
                    self.input_boxes = CoordinateInput(*rendered_point[1][:3], rendered_point, self.engine, self.viewer)
                break

        if self.check_point_radius(self.rotation_anchor, mouse_position):
            self.chosen_point, self.input_boxes = None, None
            if self.rotation_anchor == self.chosen_rotation_anchor:
                self.engine.clear_translation_lines()
                self.chosen_rotation_anchor, self.responsive_text = None, None
            else:
                self.chosen_rotation_anchor = self.rotation_anchor
                self.engine.clear_translation_lines()
                translation_lines = GUILines(self.rotation_anchor[:3], self.gui.translation_line_length)
                self.engine.set_translation_lines(translation_lines)
                self.responsive_text = ResponsiveText(*self.rotation_anchor[:2], 'Rotation Anchor')

    def check_point_radius(self, point, mouse_position):
        click_in_radius = False
        for x_position in range(mouse_position[0] - self.clickable_radius, mouse_position[0] + self.clickable_radius):
            for y_position in range(mouse_position[1] - self.clickable_radius, mouse_position[1] + self.clickable_radius):
                if int(point[0]) == x_position and int(point[1]) == y_position:
                    click_in_radius = True
        return click_in_radius

    def check_object_radius(self, pygame_object, mouse_position):
        click_in_radius = False
        for x_position in range(mouse_position[0] - self.clickable_radius, mouse_position[0] + self.clickable_radius):
            for y_position in range(mouse_position[1] - self.clickable_radius, mouse_position[1] + self.clickable_radius):
                if pygame_object.collidepoint((x_position, y_position)):
                    click_in_radius = True
        return click_in_radius
    
    def check_translation(self, mouse_position):
        if len(self.engine.rendered_translation_lines) > 0 and self.translating and self.chosen_point != None:
            if self.check_object_radius(self.engine.rendered_translation_lines[0], mouse_position) and self.translating_x == False and self.translating_y == False:
                self.translating_x = True
                self.translating_y = False
            if self.check_object_radius(self.engine.rendered_translation_lines[1], mouse_position) and self.translating_y == False and self.translating_x == False:
                self.translating_y = True
                self.translating_x = False

            if self.translating_x:
                current_row = self.chosen_point[2].points.access_row(self.chosen_point[3])
                new_row = mouse_position[0] - self.gui.translation_line_length / 2, current_row[1], current_row[2], current_row[3]
                self.chosen_point[2].points.set_row(self.chosen_point[3], new_row)
                self.chosen_point[2].project(self.engine.projection_type, self.engine.projection_anchor)
                translation_lines = GUILines(self.chosen_point[2].projected.access_row(self.chosen_point[3]), self.gui.translation_line_length)
                self.engine.set_translation_lines(translation_lines)

            if self.translating_y:
                current_row = self.chosen_point[2].points.access_row(self.chosen_point[3])
                new_row = current_row[0], mouse_position[1] - self.gui.translation_line_length / 2, current_row[2], current_row[3]
                self.chosen_point[2].points.set_row(self.chosen_point[3], new_row)
                self.chosen_point[2].project(self.engine.projection_type, self.engine.projection_anchor)
                translation_lines = GUILines(self.chosen_point[2].projected.access_row(self.chosen_point[3]), self.gui.translation_line_length)
                self.engine.set_translation_lines(translation_lines)

            self.input_boxes = CoordinateInput(*self.chosen_point[2].projected.access_row(self.chosen_point[3])[:3], self.chosen_point, self.engine, self.viewer)

    def check_rotation_anchor(self, mouse_position):
        if len(self.engine.rendered_translation_lines) > 0 and self.translating and self.chosen_point == None:
            if self.check_object_radius(self.engine.rendered_translation_lines[0], mouse_position) and self.translating_x == False and self.translating_y == False:
                self.translating_x = True
                self.translating_y = False
                self.use_custom_rotation_anchor = True
            if self.check_object_radius(self.engine.rendered_translation_lines[1], mouse_position) and self.translating_y == False and self.translating_x == False:
                self.translating_y = True
                self.translating_x = False
                self.use_custom_rotation_anchor = True

            if self.translating_x:
                current_row = self.rotation_anchor
                # New row z rotation has to still use centre of objects z position since only x and y can be specified by the translation lines
                new_row = mouse_position[0] - self.gui.translation_line_length / 2, current_row[1], self.engine.entities_centre(self.engine.objects)[2], 0
                self.rotation_anchor = new_row
                translation_lines = GUILines(self.rotation_anchor, self.gui.translation_line_length)
                self.engine.set_translation_lines(translation_lines)

            if self.translating_y:
                current_row = self.rotation_anchor
                new_row = current_row[0], mouse_position[1] - self.gui.translation_line_length / 2, self.engine.entities_centre(self.engine.objects)[2], 0
                self.rotation_anchor = new_row
                translation_lines = GUILines(self.rotation_anchor, self.gui.translation_line_length)
                self.engine.set_translation_lines(translation_lines)

            self.responsive_text = ResponsiveText(*self.rotation_anchor[:2], 'Rotation Anchor')

    def text_boxes_accepting_input(self):
        accepting_input = False
        if self.input_boxes != None:
            if self.input_boxes.accepting_input():
                accepting_input = True
        return accepting_input
    
    def render_objects(self):
        self.viewer.fill(self.bg_colour)
        self.engine.clear_rendered_points()
        if self.display_surfaces:
            for surface in self.engine.get_surfaces(self):
                colour, surface = surface[0], surface[1:]
                pygame.draw.polygon(self.viewer, colour, data_handling.convert_to_int_2d_array(surface))

        for object_3d in self.engine.objects.values():
            if object_3d.is_visible(self.gui.viewer_width, self.gui.viewer_height):
                if self.display_lines:
                    for point_1, point_2 in object_3d.lines:
                        pygame.draw.aaline(self.viewer, self.line_colour, object_3d.projected.access_row(point_1)[:2], object_3d.projected.access_row(point_2)[:2])

                if self.display_points:
                    for i, point in enumerate(object_3d.projected):
                        rendered_point = pygame.draw.circle(self.viewer, self.point_colour, (int(point[0]), int(point[1])), self.point_radius, 0)
                        self.engine.rendered_points.append([rendered_point, point, object_3d, i])
            else:
                self.render_relative_lines(object_3d)

            if self.debug_mode:
                self.debug_display(object_3d)

        if self.display_hud:
            fps = self.font.render('FPS: '+ str(int(self.clock.get_fps())), True, self.fps_colour)
            self.viewer.blit(fps, (10, 10))
            view = self.font.render('ORTHOGRAPHIC VIEW', True, self.fps_colour)
            self.viewer.blit(view, (self.gui.viewer_width - 200, 10))

        if self.display_logo:
            self.viewer.blit(self.logo, (self.gui.viewer_width - self.logo_size[0], self.gui.viewer_height - self.logo_size[1]))

        if self.engine.get_translation_lines() != None and not self.engine.performing_operations() and self.engine.acceptable_operation_period():
            if self.engine.get_translation_lines().is_visible(self.gui.viewer_width, self.gui.viewer_height):
                self.update_translation_system()
                self.render_translation_lines()
                self.render_input_boxes_and_text()

    def update_translation_system(self):
        if self.chosen_point != None:
            self.chosen_point[2].points.set_row(self.chosen_point[3], self.chosen_point[2].points.access_row(self.chosen_point[3]))
            self.chosen_point[2].project(self.engine.projection_type, self.engine.projection_anchor)
            translation_lines = GUILines(self.chosen_point[2].projected.access_row(self.chosen_point[3]), self.gui.translation_line_length)
            self.engine.set_translation_lines(translation_lines)
            self.input_boxes.reposition_boxes(*self.chosen_point[2].projected.access_row(self.chosen_point[3])[:2])

    def render_translation_lines(self):
        translation_lines = self.engine.get_translation_lines()
        x_line = pygame.draw.line(self.viewer, self.gui.translation_lines_colour_x, data_handling.convert_to_int_array(translation_lines.projected.access_row(0)[:2]), data_handling.convert_to_int_array(translation_lines.projected.access_row(1)[:2]), self.gui.translation_line_width)
        y_line = pygame.draw.line(self.viewer, self.gui.translation_lines_colour_y, data_handling.convert_to_int_array(translation_lines.projected.access_row(0)[:2]), data_handling.convert_to_int_array(translation_lines.projected.access_row(2)[:2]), self.gui.translation_line_width)
        rendered_point = pygame.draw.circle(self.viewer, self.point_colour, data_handling.convert_to_int_array(translation_lines.projected.access_row(0)[:2]), self.point_radius, 0)
        self.engine.rendered_translation_lines = [x_line, y_line]

    def render_input_boxes_and_text(self):
        if self.input_boxes != None:
            for input_box in self.input_boxes.access_input_boxes():
                input_box.resize()
                input_box.draw(self.viewer)
                
        if self.responsive_text != None:
            self.responsive_text.draw(self.viewer)

    def render_relative_lines(self, object_3d):
       for direction in object_3d.viewer_relativity(self.gui.viewer_width, self.gui.viewer_height):
            if direction == 'W':
                pygame.draw.line(self.viewer, self.relative_line_colour, (0,0), (0,self.gui.viewer_height), 5)
            if direction == 'E':
                pygame.draw.line(self.viewer, self.relative_line_colour, (self.gui.viewer_width,0), (self.gui.viewer_width,self.gui.viewer_height), 5)
            if direction == 'N':
                pygame.draw.line(self.viewer, self.relative_line_colour, (0,0), (self.gui.viewer_width,0), 5)
            if direction == 'S':
                pygame.draw.line(self.viewer, self.relative_line_colour, (0,self.gui.viewer_height), (self.gui.viewer_width,self.gui.viewer_height), 5)

def initialise(width, height):
    path = os.path.dirname(os.path.abspath(__file__))
    login_sys = Launcher(800, 400, path)
    if not login_sys.launcher_closed():
        display = EngineClient(width, height, login_sys, path)
        display.run()

if __name__ == '__main__':
    initialise(1600, 900)