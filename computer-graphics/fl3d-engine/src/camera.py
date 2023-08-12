# Third party modules
import pygame

class Camera():
    ''' An interface between pygame keyboard events and Engine3D's transformation functions. '''
    def __init__(self, display):
        # Maps the pygame keyboard events to a lambda function controlling a specific transformation if there are currently text boxes accepting keyboard keys as input.
        self.controls = {
            pygame.K_LEFT: (lambda self, engine: self.engine.translate(-display.translation_factor, 0, 0) if not self.text_boxes_accepting_input() else None),
            pygame.K_RIGHT: (lambda self, engine: self.engine.translate(display.translation_factor, 0, 0) if not self.text_boxes_accepting_input() else None),
            pygame.K_DOWN: (lambda self, engine: self.engine.translate(0, display.translation_factor, 0) if not self.text_boxes_accepting_input() else None),
            pygame.K_UP: (lambda self, engine: self.engine.translate(0, -display.translation_factor, 0) if not self.text_boxes_accepting_input() else None),
            pygame.K_EQUALS: (lambda self, engine: self.engine.scale(display.scaling_factor, display.scaling_factor, display.scaling_factor, display.gui.viewer_centre) if not self.text_boxes_accepting_input() else None),
            pygame.K_MINUS: (lambda self, engine: self.engine.scale(2 - display.scaling_factor, 2 - display.scaling_factor, 2 - display.scaling_factor, display.gui.viewer_centre) if not self.text_boxes_accepting_input() else None),
            pygame.K_q: (lambda self, engine: self.engine.rotate(display.rotation_factor, 0, 0, anchor = display.rotation_anchor) if not self.text_boxes_accepting_input() else None),
            pygame.K_w: (lambda self, engine: self.engine.rotate(-display.rotation_factor, 0, 0, anchor = display.rotation_anchor) if not self.text_boxes_accepting_input() else None),
            pygame.K_a: (lambda self, engine: self.engine.rotate(0, display.rotation_factor, 0, anchor = display.rotation_anchor) if not self.text_boxes_accepting_input() else None),
            pygame.K_s: (lambda self, engine: self.engine.rotate(0, -display.rotation_factor, 0, anchor = display.rotation_anchor) if not self.text_boxes_accepting_input() else None),
            pygame.K_z: (lambda self, engine: self.engine.rotate(0, 0, display.rotation_factor, anchor = display.rotation_anchor) if not self.text_boxes_accepting_input() else None),
            pygame.K_x: (lambda self, engine: self.engine.rotate(0, 0, -display.rotation_factor, anchor = display.rotation_anchor) if not self.text_boxes_accepting_input() else None)
        }