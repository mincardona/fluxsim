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
        assert_loc(loc)
        if type == EMPTY_PARTICLE and (loc in self.particle_map):
            self.particle_map.pop(loc)
        else:
            self.particle_map[loc] = type

    def remove_particle(self, loc):
        assert_loc(loc)
        old = self.particle_map.get(loc, EMPTY_PARTICLE)
        self.add_particle(EMPTY_PARTICLE, loc)
        return old

    def move_particle(self, src, dst):
        assert_loc(src)
        assert_loc(dst)
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

if __name__ == "__main__":
    pygame.init()
    display_width = 640
    display_height = 480

    flux_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('FluxSim')

    master_clock = pygame.time.Clock()

    state = FluxState(display_width, display_height, 1)

    while handle_pygame_events():
        update_world(state, 1000000/60)
        pygame.display.update()
        master_clock.tick(60)
