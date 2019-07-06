#!/usr/bin/python3

import pygame
import random
import copy

black = (0, 0, 0)
white = (255, 255, 255)
red = (155, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
sand = (204, 204, 0)

st_font = None

class FluxState:
    EMPTY_PARTICLE = 0
    STATIC_PARTICLE = 1
    HEAVY_PARTICLE = 2
    FLOATY_PARTICLE = 3

    def __init__(self, width, height, timescale):
        self.width = width
        self.height = height
        self.particle_map = {}
        self.timescale = timescale

    # loc is an x, y tuple
    def add_particle(self, type, loc):
        self.assert_loc(loc)
        if type == self.EMPTY_PARTICLE and (loc in self.particle_map):
            self.particle_map.pop(loc)
        else:
            self.particle_map[loc] = type

    def add_particle_rect(self, ptype, corner, width, height):
        for x in range(corner[0], corner[0] + width):
            for y in range(corner[1], corner[1] + height):
                if self.check_loc((x, y)):
                    self.add_particle(ptype, (x, y))

    def remove_particle(self, loc):
        self.assert_loc(loc)
        old = self.particle_map.get(loc, self.EMPTY_PARTICLE)
        self.add_particle(self.EMPTY_PARTICLE, loc)
        return old

    def move_particle(self, src, dst):
        self.assert_loc(src)
        self.assert_loc(dst)
        add_particle(remove_particle(src), dst)

    def check_loc(self, loc):
        return loc[0] >= 0 and loc[0] < self.width and loc[1] >= 0 and loc[1] < self.height

    def assert_loc(self, loc):
        assert self.check_loc(loc), "loc {} out of bounds".format(loc)


# return False to quit
def handle_pygame_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

# game state
def update_world(state):
    old_particles = copy.deepcopy(state.particle_map)
    new_particles = {}

    def loc_empty(loc):
        valid = state.check_loc(loc)
        not_exist = not ((loc in old_particles) or (loc in new_particles))
        return valid and not_exist

    def move_particle(loc, loc2):
        new_particles[loc2] = old_particles[loc]
        old_particles.pop(loc)

    for ogloc, ptype in state.particle_map.items():
        new_loc = ogloc

        if ptype == FluxState.STATIC_PARTICLE:
            move_particle(ogloc, new_loc)
        else:
            leftright = random.randint(-1, 1)

            above_loc = (ogloc[0], ogloc[1] - 1)
            below_loc = (ogloc[0], ogloc[1] + 1)

            if ptype == FluxState.HEAVY_PARTICLE and loc_empty(below_loc):
                new_loc = below_loc
            elif ptype == FluxState.FLOATY_PARTICLE and loc_empty(above_loc):
                new_loc = above_loc

            left_loc = (new_loc[0] - 1, new_loc[1])
            right_loc = (new_loc[0] + 1, new_loc[1])

            if leftright == -1 and loc_empty(left_loc):
                new_loc = left_loc
            elif leftright == 1 and loc_empty(right_loc):
                new_loc = right_loc

            move_particle(ogloc, new_loc)

    state.particle_map = new_particles

    return

def render(state, flux_display, fps):
    particle_colors = {
        FluxState.EMPTY_PARTICLE : black,
        FluxState.STATIC_PARTICLE : white,
        FluxState.HEAVY_PARTICLE : sand,
        FluxState.FLOATY_PARTICLE : red
    }

    flux_display.fill(black)

    for loc, particle in state.particle_map.items():
        pygame.draw.rect(flux_display, particle_colors[particle], [loc[0], loc[1], 1, 1])

    fps_str = "%.1f" % fps
    fps_surface = st_font.render(fps_str, True, white)
    fps_rect = fps_surface.get_rect()
    fps_rect.bottom = state.height - 1
    fps_rect.left = 0

    flux_display.blit(fps_surface, fps_rect)

    return

if __name__ == "__main__":
    pygame.init()
    display_width = 640
    display_height = 480

    flux_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('FluxSim')

    st_font = pygame.font.Font(None, 16)

    master_clock = pygame.time.Clock()

    state = FluxState(display_width, display_height, 1)

    state.add_particle_rect(FluxState.HEAVY_PARTICLE, (100, 0), 100, 50)
    state.add_particle_rect(FluxState.STATIC_PARTICLE, (125, 200), 50, 3)
    state.add_particle_rect(FluxState.FLOATY_PARTICLE, (100, 300), 100, 50)

    while handle_pygame_events():
        render(state, flux_display, master_clock.get_fps())
        pygame.display.update()
        master_clock.tick(60)
        update_world(state)
