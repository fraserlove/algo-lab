# Third party modules
import sqlite3

# Project-specific modules
from structures import Matrix
from shapes import Cube, Quad, Plane, Polygon, Sphere, Line2D, Line3D
import data_handling

class DatabaseManager():
    ''' An interface to manage and execute querys on the SQLite3 Database. '''
    
    def __init__(self, db_name):
        print(db_name)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_database()

    def close_database(self):
        self.conn.close()

    def create_database(self):
        object_table = '''
            CREATE TABLE IF NOT EXISTS ObjectData (
                name TEXT PRIMARY KEY,
                colour TEXT,
                points TEXT,
                lines TEXT,
                surfaces TEXT,
                position TEXT,
                type TEXT,
                start_point TEXT,
                end_point TEXT,
                angle FLOAT,
                magnitude FLOAT,
                radius FLOAT,
                verts_res INTEGER,
                no_points INTEGER,
                length INTEGER,
                width INTEGER,
                height INTEGER
            )
            '''
        self.cursor.execute(object_table)
        print('SUCCESS: Database \'ObjectData\' built')

        users_table = '''
            CREATE TABLE IF NOT EXISTS UserData (
                username TEXT PRIMARY KEY,
                password TEXT,
                registered_time TEXT,
                login_time TEXT,
                total_logins INTEGER
            )
            '''
        self.cursor.execute(users_table)
        print('SUCCESS: Database \'UserData\' built')

        settings_table = '''
            CREATE TABLE IF NOT EXISTS UserSettings (
                username TEXT PRIMARY KEY,
                display_surfaces BOOLEAN,
                display_lines BOOLEAN,
                display_points BOOLEAN,
                debug_mode BOOLEAN,
                display_hud BOOLEAN,
                display_logo BOOLEAN,
                rotation_factor FLOAT,
                scaling_factor FLOAT,
                translation_factor FLOAT,
                movement_factor INTEGER,
                max_frame_rate INTEGER,
                max_render_distance FLOAT,
                min_render_distance FLOAT,
                lighting_factor FLOAT,
                point_radius INTEGER,

                FOREIGN KEY (username) REFERENCES UserData (username)
            )
        '''
        self.cursor.execute(settings_table)

        self.conn.commit()

    def save_user_settings(self, engine_client):
        ''' Inserts all user settings in the UserSettings table by fetching the relavant attributes from the EngineClient object. '''
        sql = 'INSERT OR REPLACE INTO UserSettings (username, display_surfaces, display_lines, display_points, debug_mode, display_hud, display_logo, rotation_factor, scaling_factor, translation_factor, movement_factor, max_frame_rate, max_render_distance, min_render_distance, lighting_factor, point_radius) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        self.cursor.execute(sql, [engine_client.login_sys.get_username(), engine_client.display_surfaces, engine_client.display_lines, engine_client.display_points, engine_client.debug_mode, engine_client.display_hud, \
            engine_client.display_logo, engine_client.rotation_factor, engine_client.scaling_factor, engine_client.translation_factor, engine_client.movement_factor, engine_client.max_frame_rate, engine_client.max_render_distance, \
            engine_client.min_render_distance, engine_client.lighting_factor, engine_client.point_radius])
        self.conn.commit()

    def load_user_settings(self, engine_client):
        ''' Loads user settings from the UserSettings table where the username entered into the Launcher object matches the username in the database. If no match is found, default settings are loaded. '''
        sql = 'SELECT * FROM UserSettings WHERE username = ?'
        self.cursor.execute(sql, [engine_client.login_sys.get_username()])
        row = self.cursor.fetchone()
        if row != None:
            return row[1:]
        else:
            return True, True, True, True, True, True, 0.1, 25.0, 1.1, 25, 1000, 10, 0.0001, 1.25, 2

    def save_objects(self, objects):
        ''' Inserts objects into the ObjectData table according to their type. '''
        for object_3d in objects.values():
            if object_3d.get_type() == 'Cube':
                sql = 'INSERT OR REPLACE INTO ObjectData (name, colour, points, lines, surfaces, position, type, length) VALUES (?,?,?,?,?,?,?,?)'
                self.cursor.execute(sql, [object_3d.name, object_3d.colour, str(data_handling.v_strip_2d_array(object_3d.points.access_matrix(), 3)), str(object_3d.lines), str(object_3d.surfaces), str(object_3d.get_position()), object_3d.get_type(), object_3d.get_size()])
            if object_3d.get_type() == 'Quad':
                sql = 'INSERT OR REPLACE INTO ObjectData (name, colour, points, lines, surfaces, position, type, length, width, height) VALUES (?,?,?,?,?,?,?,?,?,?)'
                self.cursor.execute(sql, [object_3d.name, object_3d.colour, str(data_handling.v_strip_2d_array(object_3d.points.access_matrix(), 3)), str(object_3d.lines), str(object_3d.surfaces), str(object_3d.get_position()), object_3d.get_type(), object_3d.get_length(), object_3d.get_width(), object_3d.get_height()])
            if object_3d.get_type() == 'Plane':
                sql = 'INSERT OR REPLACE INTO ObjectData (name, colour, points, lines, surfaces, position, type, length, width) VALUES (?,?,?,?,?,?,?,?,?)'
                self.cursor.execute(sql, [object_3d.name, object_3d.colour, str(data_handling.v_strip_2d_array(object_3d.points.access_matrix(), 3)), str(object_3d.lines), str(object_3d.surfaces), str(object_3d.get_position()), object_3d.get_type(), object_3d.get_length(), object_3d.get_width()])
            if object_3d.get_type() == 'Polygon':
                sql = 'INSERT OR REPLACE INTO ObjectData (name, colour, points, lines, surfaces, position, type, no_points, length) VALUES (?,?,?,?,?,?,?,?,?)'
                self.cursor.execute(sql, [object_3d.name, object_3d.colour, str(data_handling.v_strip_2d_array(object_3d.points.access_matrix(), 3)), str(object_3d.lines), str(object_3d.surfaces), str(object_3d.get_position()), object_3d.get_type(), object_3d.get_no_points(), object_3d.get_size()])
            if object_3d.get_type() == 'Sphere':
                sql = 'INSERT OR REPLACE INTO ObjectData (name, colour, points, lines, surfaces, position, type, radius, verts_res) VALUES (?,?,?,?,?,?,?,?,?)'
                self.cursor.execute(sql, [object_3d.name, object_3d.colour, str(data_handling.v_strip_2d_array(object_3d.points.access_matrix(), 3)), str(object_3d.lines), str(object_3d.surfaces), str(object_3d.get_position()), object_3d.get_type(), object_3d.get_radius(), object_3d.get_verts_res()])
            if object_3d.get_type() == 'Line2D':
                sql = 'INSERT OR REPLACE INTO ObjectData (name, colour, points, lines, surfaces, position, type, angle, magnitude) VALUES (?,?,?,?,?,?,?,?,?)'
                self.cursor.execute(sql, [object_3d.name, object_3d.colour, str(data_handling.v_strip_2d_array(object_3d.points.access_matrix(), 3)), str(object_3d.lines), str(object_3d.surfaces), str(object_3d.get_position()), object_3d.get_type(), object_3d.get_angle(), object_3d.get_magnitude()])
            if object_3d.get_type() == 'Line3D':
                sql = 'INSERT OR REPLACE INTO ObjectData (name, colour, points, lines, surfaces, position, type, start_point, end_point) VALUES (?,?,?,?,?,?,?,?,?)'
                self.cursor.execute(sql, [object_3d.name, object_3d.colour, str(data_handling.v_strip_2d_array(object_3d.points.access_matrix(), 3)), str(object_3d.lines), str(object_3d.surfaces), str(object_3d.get_position()), object_3d.get_type(), str(object_3d.get_start_point()), str(object_3d.get_end_point())])
        self.conn.commit()
        print('SUCCESS: Object data saved')

    def remove_save(self):
        ''' Removes all entries in the ObjectData table. '''
        sql = 'DELETE FROM ObjectData'
        self.cursor.execute(sql)

    def import_objects(self, engine):
        ''' Imports all objects stored in the ObjectData table according to their type. '''
        for name, colour, points, lines, surfaces, position, _type, *args in self.cursor.execute('SELECT * FROM ObjectData'):
            args = [attribute for attribute in args if attribute != None]
            if _type == 'Cube':
                object_3d = Cube(name, data_handling.string_to_float_array(position), *args, colour)
            if _type == 'Quad':
                object_3d = Quad(name, data_handling.string_to_float_array(position), *args, colour)
            if _type == 'Plane':
                object_3d = Plane(name, data_handling.string_to_float_array(position), *args, colour)
            if _type == 'Polygon':
                object_3d = Polygon(name, data_handling.string_to_float_array(position), *args, colour)
            if _type == 'Sphere':
                object_3d = Sphere(name, data_handling.string_to_float_array(position), *args, colour)
            if _type == 'Line2D':
                object_3d = Line2D(name, data_handling.string_to_float_array(position), *args, colour)
            if _type == 'Line3D':
                object_3d = Line3D(name, data_handling.string_to_float_array(position), data_handling.string_to_float_array(*args), colour)
            object_3d.add_points(Matrix(data_handling.string_to_2d_float_array(points, 3)))
            object_3d.add_lines(data_handling.string_to_2d_int_array(lines, 2))
            object_3d.add_surfaces(data_handling.string_to_2d_int_array(surfaces, 4))
            engine.add_object(object_3d)

    def add_user(self, username, password, registered_time):
        ''' Adds a new user to the UserData table from the provided username and password. '''
        sql = 'INSERT OR REPLACE INTO UserData (username, password, registered_time, login_time, total_logins) VALUES (?,?,?,?,?)'
        self.cursor.execute(sql, [username, password, registered_time, None, 0])
        self.conn.commit()
        print('SUCCESS: New user added')

    def update_login_time(self, username, login_time):
        ''' Updates the current login time of a user. '''
        sql = 'UPDATE UserData SET login_time = ?, total_logins = total_logins + 1 WHERE username = ?'
        self.cursor.execute(sql, [login_time, username])
        self.conn.commit()

    def query_field(self, select_field, query_field, query_value):
        ''' Queries a specific field for a value based on the value of another field. '''
        sql = 'SELECT '+ select_field +' FROM UserData WHERE ' + query_field +' = ?'
        self.cursor.execute(sql, [query_value])
        row = self.cursor.fetchone()
        if row != None:
            return row[0]

    def check_user_existance(self, entered_username, entered_password):
        ''' Checks if the entered username and password matches with a user in the UserData table. '''
        exists = False
        sql = 'SELECT username, COUNT(*) FROM UserData WHERE EXISTS (SELECT * FROM UserData WHERE username = ? AND password = ?)'
        for username, count in self.cursor.execute(sql, [entered_username, entered_password]):
            if count > 0:
                exists = True
        return exists