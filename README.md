# fluxsim
Fluid particle simulator using PyGame

```
usage: fluxsim.py [-h] [-p] [-i IMAGE] [-o OUTPUT_IMAGE]

Simulate particles

optional arguments:
  -h, --help            show this help message and exit
  -p, --prerender       prerender the scene
  -i IMAGE, --image IMAGE
                        image to use for initialization
  -o OUTPUT_IMAGE, --output-image OUTPUT_IMAGE
                        filename of prerendered output GIF
```

The simulation can be initialized with an image created using an image editor
or other program. Most common formats are supported. In your input image, set
pixels to the following colors to place different particle types:

| (r, g, b)       | Particle Type |
------------------|----------------
| (0, 0, 0)       | Empty space   |
| (255, 255, 255) | Static particle |
| (204, 204, 0)   | Sand particle |
| (155, 0, 0)     | Floaty particle |

If no input image is specified, a default demo is used.

### Pre-rendering

The simulation can either be rendered in real-time, or prerendered with the
`-p` flag. A prerendered scene produces a 60 FPS GIF file. By default the output
filename is `out.gif`, but this can be overridden with the `-o` flag. A
real-time scene renders at up to 60 FPS using pygame.
