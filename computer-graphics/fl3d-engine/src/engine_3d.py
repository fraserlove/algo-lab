# Third party modules
import time, copy

# Project-specific modules
import data_handling

class Engine3D():
    ''' Provides functionality used to translate, and manipulate 3D objects. '''
    def __init__(self, projection_type = 'orthographic', projection_anchor = (0, 0, 0, 0)):
        self.objects = {}
        self.translation_lines = None
        self._performing_operations = False
        self._last_operation_time = time.time()
        self.operation_delay = 0.4 # The minimum time between operations allowed to show the translation lines in seconds

        self.rendered_translation_lines = []
        self.rendered_points = [[]]

        self.projection_type = projection_type
        self.projection_anchor = projection_anchor
    
    def add_object(self, object_3d):
        self.objects[object_3d.name] = object_3d
        object_3d.project(self.projection_type, self.projection_anchor)

    def copy_object(self, object_3d, new_object_name):
        new_object = copy.copy(object_3d)
        new_object.set_name(new_object_name)
        self.objects[new_object_name] = new_object
        new_object.project(self.projection_type, self.projection_anchor)

    def set_translation_lines(self, translation_lines):
        self.translation_lines = translation_lines
        translation_lines.projected = translation_lines.points

    def translate(self, dx, dy, dz):
        self._performing_operations = True
        self._last_operation_time = time.time()

        for object_3d in self.objects.values():
            object_3d.translate((dx, dy, dz))
            object_3d.project(self.projection_type, self.projection_anchor)
            object_3d.update_position()

    def scale(self, kx, ky, kz, anchor = None):
        self._performing_operations = True
        self._last_operation_time = time.time()
        if anchor == None:
            anchor = self.entities_centre()

        for object_3d in self.objects.values():
            object_3d.scale((kx, ky, kz), anchor)
            object_3d.project(self.projection_type, self.projection_anchor)
            object_3d.update_position()

    def rotate(self, rx, ry, rz, anchor = None):
        self._performing_operations = True
        self._last_operation_time = time.time()
        if anchor == None:
            anchor = self.entities_centre()

        for object_3d in self.objects.values():
            object_3d.rotate((rx, ry, rz), anchor)
            object_3d.project(self.projection_type, self.projection_anchor)
            object_3d.update_position()
    
    def entities_centre(self, entities = None):
        centre = (0, 0, 0, 0)
        if entities == None:
            entities = self.objects.keys()

        total_x, total_y, total_z, no_points = 0, 0, 0, 0
        for object_3d in entities:
            total_x += self.objects[object_3d].sum_x()
            total_y += self.objects[object_3d].sum_y()
            total_z += self.objects[object_3d].sum_z()
            no_points += self.objects[object_3d].point_count()
        if no_points > 0:
           centre = (total_x / no_points, total_y / no_points, total_z / no_points, 0)
        return centre

    def surface_mean_y(self, surface):
        sum = 0
        for point in surface[1:]:
            sum += point[1]
        return data_handling.div_non_zero(sum, len(surface))

    def surface_mean_z(self, surface):
        sum = 0
        for point in surface[1:]:
            sum += point[2]
        return data_handling.div_non_zero(sum, len(surface))

    def order_surfaces(self, engine_client):
        ordered_surfaces = self.get_all_surfaces(engine_client).copy()
        
        for i in range(len(ordered_surfaces)):
            current = ordered_surfaces[i]
            index = i
            while index > 0 and self.surface_mean_z(ordered_surfaces[index-1]) > self.surface_mean_z(current):
                ordered_surfaces[index] = ordered_surfaces[index-1]
                index -= 1
            ordered_surfaces[index] = current
        return ordered_surfaces

    def get_surfaces(self, engine_client):
        ordered_surfaces = self.order_surfaces(engine_client)
        surfaces = []
        for ordered_surface in ordered_surfaces:
            points = [ordered_surface[0]]
            for point in ordered_surface[1:]:
                points.append(point[:2])
            surfaces.append(points)
        return surfaces

    def clear_all_objects(self):
        self.objects = {}
        self.clear_translation_lines()
        self.clear_rendered_points()

    def remove_object(self, object_name, engine_client):
        if engine_client.chosen_point != None:
            if engine_client.chosen_point[2].points.access_row(engine_client.chosen_point[3]) in self.objects[object_name].points.access_matrix():
                self.clear_translation_lines()
                self.clear_rendered_points()
        if engine_client.chosen_rotation_anchor != None:
            if len(self.objects) == 1: # If the object being deleted is the last object then remove the rotation point
                self.clear_translation_lines()
                self.clear_rendered_points()
        del self.objects[object_name]

    def get_all_surfaces(self, engine_client):
        all_surfaces = []
        for object_3d in self.objects.values():
            if object_3d.check_render_distance(engine_client.max_render_distance, engine_client.min_render_distance):
                if object_3d.is_visible(engine_client.gui.viewer_width, engine_client.gui.viewer_height):
                    for surface in object_3d.get_surfaces():
                        points = [object_3d.map_colour(surface, engine_client.lighting_factor)]
                        for point_idx in surface:
                            points.append(object_3d.get_points()[point_idx])
                        all_surfaces.append(points)
        return all_surfaces

    def clear_rendered_points(self):
        self.rendered_points = []

    def clear_translation_lines(self):
        self.translation_lines = None
    
    def get_translation_lines(self):
        return self.translation_lines

    def performing_operations(self):
        return self._performing_operations

    def update_operating_status(self, status):
        self._performing_operations = status

    def acceptable_operation_period(self):
        return True if time.time() - self._last_operation_time > self.operation_delay else False

    def update_objects_key(self, old_key, new_key):
        self.objects[new_key] = self.objects.pop(old_key)