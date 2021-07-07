"""
Perlin Noise Flow Field

Created 13/08/19
Updated 07/07/21
Developed by Fraser Love

A particle flow field using perlin noise to create a vector array to update particle
position, velocity and acceleration. The program is not meant to be ran in real-time. An image of each
frame is saved under images/ and can be combined to produce a video separately.
"""
import noise, os, math, particle, sys, time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Display Variables
dimensions = (1920, 1080)
scale = 10  # Resolution, the lower the value the greater the number of vectors in the simulation
cols = dimensions[0] // scale
rows = dimensions[1] // scale
particle_count = 100000  # Number of particles in the flow field
particle_radius = 1  # Radius of particles to display
show_vectors = False  # If 'true' draws the vectors in the flow field
show_particles = True  # If 'true' draws the particles in the flow field

# Perlin Noise Variables
noise_res = 0.01  # Controls the resolution of the perlin noise
octaves = 1  # Controls the roughness of the perlin noise
height = 1  # Coefficient of the height of perlin noise
z_increment = 0.01  # Controls how quick the perlin noise changes

class Display:
    """ Object to control the display with pygame """
    def __init__(self):
        self.display = pygame.display.set_mode(dimensions)
        self.particles = []
        self.z_off = 0
        self.start_time = time.time()
        self.setup()

    def setup(self):
        """ Setting up display and adding particles to particles array """
        pygame.display.set_caption("Perlin Noise Flow Field")
        self.add_particles(particle_count)
        self.run()

    def add_particles(self, amount):
        for i in range(amount):
            self.particles.append(particle.Particle())

    def perlin_noise(self):
        """ Creating 3D perlin noise and storing it as a vector in an array called flowfield """
        y_off = 0
        self.flowfield = []
        for y in range(rows):
            x_off = 0
            for x in range(cols):
                perlin = noise.pnoise3(x_off,y_off,self.z_off,octaves) * math.pi * 2 * height
                vector = particle.Vector(perlin)
                self.flowfield.append(vector)
                if show_vectors:
                    pygame.draw.aaline(self.display, (140,140,140), (x*scale, y*scale), ((x+vector.display_x)*scale, (y+vector.display_y)*scale), 1)
                x_off += noise_res
            y_off += noise_res
        self.z_off += z_increment

    def draw_particles(self):
        """ Updating particle kinematics and displaying particles on screen """
        for particle in self.particles:
            particle.update()
            particle.follow(self.flowfield)
            if show_particles:
                pygame.draw.rect(self.display, "white", (int(particle.pos.x), int(particle.pos.y), particle_radius, particle_radius))

    def run(self):
        """ Main program loop controling updating display, flowfield and particles """
        os.makedirs("images/", exist_ok=True)
        step = 1
        while True:
            pygame.display.set_caption('Perlin Noise Flow Field     Step: {}     Time: {}'.format(str(step), round(time.time() - self.start_time, 2)))
            self.display.fill("black")
            self.perlin_noise()
            self.draw_particles()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit();
            pygame.display.update()
            pygame.image.save(self.display, "images/{}.jpg".format(step))
            step += 1

if __name__ == "__main__":
    pygame.init()
    window = Display()
