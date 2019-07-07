#!/usr/bin/python3

import pygame
import random
import copy
import sys

black = (0, 0, 0)
white = (255, 255, 255)
red = (155, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
sand = (204, 204, 0)

st_font = None

def swap_kv(dc):
    outval = {}
    for k, v in dc.items():
        outval[v] = k
    return outval

class FluxState:
    EMPTY_PARTICLE = 0
    STATIC_PARTICLE = 1
    HEAVY_PARTICLE = 2
    FLOATY_PARTICLE = 3

    particle_colors = {
        EMPTY_PARTICLE : black,
        STATIC_PARTICLE : white,
        HEAVY_PARTICLE : sand,
        FLOATY_PARTICLE : red
    }

    particle_colors_by_color = swap_kv(particle_colors)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.particle_map = {}

    def from_surface(surf):
        (surf_w, surf_h) = surf.get_size()
        state = FluxState(surf_w, surf_h)
        for x in range(0, surf_w):
            for y in range(0, surf_h):
                # get (r, g, b) at this x, y location
                pixel_color = tuple(surf.get_at((x, y)))[0:3]
                if pixel_color in FluxState.particle_colors_by_color:
                    type = FluxState.particle_colors_by_color[pixel_color]
                    state.add_particle(type, (x, y))
        return state

    # loc is an x, y tuple
    def add_particle(self, type, loc):
        self.assert_loc(loc)
        if type == self.EMPTY_PARTICLE:
            if loc in self.particle_map:
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
    new_particles = {}

    def loc_empty(loc):
        return state.check_loc(loc) and not ((loc in state.particle_map) or (loc in new_particles))

    klist = list(state.particle_map.keys())

    for ogloc in klist:
        ptype = state.particle_map[ogloc]
        new_loc = ogloc

        if ptype != FluxState.STATIC_PARTICLE:
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

        new_particles[new_loc] = state.particle_map[ogloc]
        state.particle_map.pop(ogloc)

    state.particle_map = new_particles

    return

def render(state, flux_display, fps):
    flux_display.fill(black)

    for loc, particle in state.particle_map.items():
        flux_display.set_at((loc[0], loc[1]), FluxState.particle_colors[particle])

    fps_str = "%.1f" % fps
    fps_surface = st_font.render(fps_str, True, white)
    fps_rect = fps_surface.get_rect()
    fps_rect.bottom = state.height - 1
    fps_rect.left = 0

    flux_display.blit(fps_surface, fps_rect)

    return

if __name__ == "__main__":
    pygame.init()

    if len(sys.argv) == 1:
        state = FluxState(200, 200)
        state.add_particle_rect(FluxState.HEAVY_PARTICLE, (50, 0), 50, 50)
        state.add_particle_rect(FluxState.STATIC_PARTICLE, (60, 100), 25, 3)
        #state.add_particle_rect(FluxState.FLOATY_PARTICLE, (50, 150), 50, 50)
    elif len(sys.argv) == 2:
        state = FluxState.from_surface(pygame.image.load(sys.argv[1]))
    else:
        raise RuntimeError("Bad argument count (got {})".format(len(sys.argv)-1))

    flux_display = pygame.display.set_mode((state.width, state.height))
    pygame.display.set_caption('FluxSim')

    st_font = pygame.font.Font(None, 16)

    master_clock = pygame.time.Clock()

    while handle_pygame_events():
        render(state, flux_display, master_clock.get_fps())
        pygame.display.update()
        master_clock.tick(1000)
        update_world(state)
