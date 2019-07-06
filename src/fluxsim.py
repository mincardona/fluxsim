import pygame


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

# game state and microseconds elapsed
def update_world(state, us):
    return

def render(state, flux_display):
    particle_colors = {
        FluxState.EMPTY_PARTICLE : (255, 255, 255),
        FluxState.STATIC_PARTICLE : (0, 0, 0),
        FluxState.HEAVY_PARTICLE : (0, 255, 0),
        FluxState.FLOATY_PARTICLE : (255, 0, 0)
    }

    flux_display.fill((255, 255, 255))

    for loc, particle in state.particle_map.items():
        pygame.draw.rect(flux_display, particle_colors[particle], [loc[0], loc[1], 1, 1])

    return

if __name__ == "__main__":
    pygame.init()
    display_width = 640
    display_height = 480

    flux_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('FluxSim')

    master_clock = pygame.time.Clock()

    state = FluxState(display_width, display_height, 1)
    state.add_particle(3, (0, 0))
    state.add_particle(3, (5, 5))

    while handle_pygame_events():
        update_world(state, 1000000/60)
        render(state, flux_display)
        pygame.display.update()
        master_clock.tick(60)
